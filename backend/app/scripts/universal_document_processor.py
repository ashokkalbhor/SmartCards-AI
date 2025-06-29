import asyncio
import requests
import PyPDF2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import yaml
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import tempfile
import os
import re
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UniversalDocumentProcessor:
    def __init__(self, config_path: str = "app/data/config/document_sources.yaml"):
        self.config_path = Path(config_path)
        
        # Load configuration if exists
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = self._create_default_config()
            self._save_config()
        
        # Setup paths
        self.uploads_path = Path("app/data/documents/uploads")
        self.processed_path = Path("app/data/documents/processed")
        self.chunks_path = Path("app/data/documents/chunks")
        self.temp_path = Path("app/data/documents/temp")
        
        # Create directories
        for path in [self.uploads_path, self.processed_path, self.chunks_path, self.temp_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        # Setup Selenium (for dynamic web pages)
        self._setup_webdriver()
    
    def _create_default_config(self) -> Dict:
        """Create default configuration file"""
        return {
            "banks": {
                "hdfc": {
                    "name": "HDFC Bank",
                    "cards": [
                        {
                            "id": "regalia_gold",
                            "name": "HDFC Regalia Gold",
                            "documents": [
                                {
                                    "type": "pdf_url",
                                    "url": "https://www.hdfcbank.com/content/dam/hdfcbank/htdocs/pdfs/Terms-and-Conditions-Credit-Cards.pdf",
                                    "description": "Terms and Conditions",
                                    "document_category": "terms"
                                },
                                {
                                    "type": "web_page",
                                    "url": "https://www.hdfcbank.com/personal/pay/cards/credit-cards/regalia-gold",
                                    "description": "Features and Benefits",
                                    "document_category": "features",
                                    "scraping_config": {
                                        "selectors": [".card-features", ".benefits-section", ".reward-structure"],
                                        "exclude_selectors": [".navigation", ".footer", ".header"]
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        }
    
    def _save_config(self):
        """Save configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, indent=2)
    
    def _setup_webdriver(self):
        """Setup Selenium WebDriver for web scraping"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        self.chrome_options = chrome_options
    
    async def process_all_documents(self):
        """Process all documents from all configured sources"""
        print("🚀 Starting Universal Document Processing")
        print("=" * 50)
        
        total_processed = 0
        total_chunks = 0
        
        for bank_name, bank_config in self.config['banks'].items():
            print(f"\n🏦 Processing {bank_config['name']}")
            bank_stats = await self._process_bank_documents(bank_name, bank_config)
            total_processed += bank_stats['documents_processed']
            total_chunks += bank_stats['chunks_created']
        
        print(f"\n✅ Universal document processing completed!")
        print(f"📊 Summary: {total_processed} documents processed, {total_chunks} chunks created")
        
        return {
            "total_documents_processed": total_processed,
            "total_chunks_created": total_chunks
        }
    
    async def _process_bank_documents(self, bank_name: str, bank_config: Dict) -> Dict:
        """Process all documents for a specific bank"""
        documents_processed = 0
        chunks_created = 0
        
        for card in bank_config['cards']:
            card_id = card['id']
            card_name = card['name']
            
            print(f"\n💳 Processing {card_name}")
            
            for doc_config in card['documents']:
                try:
                    result = await self._process_single_document(
                        bank_name, card_id, card_name, doc_config
                    )
                    
                    if result['success']:
                        documents_processed += 1
                        chunks_created += result['chunks_count']
                    
                except Exception as e:
                    logger.error(f"Error processing document for {card_name}: {e}")
        
        return {
            "documents_processed": documents_processed,
            "chunks_created": chunks_created
        }
    
    async def _process_single_document(
        self, 
        bank_name: str, 
        card_id: str, 
        card_name: str, 
        doc_config: Dict
    ) -> Dict:
        """Process a single document based on its type"""
        doc_type = doc_config['type']
        doc_category = doc_config.get('document_category', 'general')
        
        try:
            print(f"  📄 Processing {doc_type}: {doc_config.get('description', 'No description')}")
            
            # Extract content based on source type
            if doc_type == "upload":
                content = await self._process_uploaded_document(doc_config)
            elif doc_type == "pdf_url":
                content = await self._process_pdf_url(doc_config)
            elif doc_type == "web_page":
                content = await self._process_web_page(doc_config)
            else:
                print(f"    ⚠️ Unsupported document type: {doc_type}")
                return {"success": False, "chunks_count": 0}
            
            if not content or len(content.strip()) < 100:
                print(f"    ❌ No meaningful content extracted")
                return {"success": False, "chunks_count": 0}
            
            # Create chunks
            chunks = await self._create_document_chunks(
                content, bank_name, card_id, card_name, doc_config
            )
            
            if not chunks:
                print(f"    ❌ No chunks created")
                return {"success": False, "chunks_count": 0}
            
            # Save chunks
            chunks_saved = await self._save_chunks(chunks, f"{bank_name}_{card_id}_{doc_category}")
            
            if chunks_saved:
                print(f"    ✅ Created {len(chunks)} chunks")
                return {"success": True, "chunks_count": len(chunks)}
            else:
                print(f"    ❌ Failed to save chunks")
                return {"success": False, "chunks_count": 0}
            
        except Exception as e:
            print(f"    ❌ Error processing document: {e}")
            logger.error(f"Error processing {doc_type} for {card_id}: {e}")
            return {"success": False, "chunks_count": 0}
    
    async def _process_uploaded_document(self, doc_config: Dict) -> Optional[str]:
        """Process manually uploaded documents"""
        file_path = Path(doc_config['file_path'])
        
        if not file_path.exists():
            print(f"    ⚠️ File not found: {file_path}")
            return None
        
        source_type = doc_config.get('source_type', 'pdf').lower()
        
        if source_type == 'pdf':
            return await self._extract_pdf_text_from_file(file_path)
        elif source_type in ['html', 'htm']:
            return await self._extract_html_text_from_file(file_path)
        elif source_type == 'txt':
            return await self._extract_text_from_file(file_path)
        elif source_type in ['docx', 'doc']:
            return await self._extract_docx_text_from_file(file_path)
        else:
            print(f"    ⚠️ Unsupported file type: {source_type}")
            return None
    
    async def _process_pdf_url(self, doc_config: Dict) -> Optional[str]:
        """Process PDF documents from URLs"""
        pdf_url = doc_config['url']
        
        try:
            print(f"    📥 Downloading PDF from: {pdf_url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(pdf_url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # Check if response is actually a PDF
            content_type = response.headers.get('content-type', '').lower()
            if 'pdf' not in content_type and not pdf_url.lower().endswith('.pdf'):
                print(f"    ⚠️ URL may not be a PDF: {content_type}")
            
            # Save to temporary file
            temp_filename = f"temp_pdf_{int(time.time())}.pdf"
            temp_path = self.temp_path / temp_filename
            
            with open(temp_path, 'wb') as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
            
            print(f"    📝 Extracting text from PDF...")
            
            # Extract text
            content = await self._extract_pdf_text_from_file(temp_path)
            
            # Cleanup
            try:
                temp_path.unlink()
            except:
                pass
            
            return content
            
        except Exception as e:
            print(f"    ❌ Error downloading/processing PDF: {e}")
            return None
    
    async def _process_web_page(self, doc_config: Dict) -> Optional[str]:
        """Process web pages (MITC pages)"""
        url = doc_config['url']
        scraping_config = doc_config.get('scraping_config', {})
        
        try:
            print(f"    🌐 Scraping web page: {url}")
            
            # Try requests first (faster), fallback to Selenium if needed
            content = await self._scrape_with_requests(url, scraping_config)
            
            if not content or len(content.strip()) < 200:
                print(f"    🔄 Requests failed, trying Selenium...")
                content = await self._scrape_with_selenium(url, scraping_config)
            
            return content
                
        except Exception as e:
            print(f"    ❌ Error scraping web page: {e}")
            return None
    
    async def _scrape_with_requests(self, url: str, config: Dict) -> Optional[str]:
        """Scrape static web pages using requests + BeautifulSoup"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            exclude_selectors = config.get('exclude_selectors', [])
            for selector in exclude_selectors:
                for element in soup.select(selector):
                    element.decompose()
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract content from specific selectors
            selectors = config.get('selectors', [])
            content_parts = []
            
            if selectors:
                for selector in selectors:
                    elements = soup.select(selector)
                    for element in elements:
                        text = element.get_text(separator=' ', strip=True)
                        if len(text) > 50:  # Only add substantial content
                            content_parts.append(text)
            
            if not content_parts:
                # Fallback: get main content
                main_selectors = ['main', '.main-content', '.content', 'article', '.card-details']
                for selector in main_selectors:
                    elements = soup.select(selector)
                    for element in elements:
                        text = element.get_text(separator=' ', strip=True)
                        if len(text) > 100:
                            content_parts.append(text)
                        break
                    if content_parts:
                        break
            
            if not content_parts:
                # Last resort: get body text
                body = soup.find('body')
                if body:
                    content_parts.append(body.get_text(separator=' ', strip=True))
            
            content = '\n\n'.join(content_parts)
            return self._clean_web_content(content)
            
        except Exception as e:
            logger.error(f"Error scraping with requests: {e}")
            return None
    
    async def _scrape_with_selenium(self, url: str, config: Dict) -> Optional[str]:
        """Scrape dynamic web pages using Selenium"""
        driver = None
        try:
            # Setup Chrome driver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chrome_options)
            
            driver.get(url)
            
            # Wait for specific element if configured
            wait_for = config.get('wait_for')
            if wait_for:
                wait = WebDriverWait(driver, 10)
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_for)))
                except:
                    pass  # Continue even if wait fails
            
            # Wait a bit more for dynamic content
            await asyncio.sleep(3)
            
            # Extract content
            selectors = config.get('selectors', [])
            content_parts = []
            
            if selectors:
                for selector in selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            text = element.text.strip()
                            if len(text) > 50:
                                content_parts.append(text)
                    except:
                        continue
            
            if not content_parts:
                # Fallback: get body text
                try:
                    body = driver.find_element(By.TAG_NAME, "body")
                    content_parts.append(body.text)
                except:
                    pass
            
            content = '\n\n'.join(content_parts)
            return self._clean_web_content(content)
            
        except Exception as e:
            logger.error(f"Error scraping with Selenium: {e}")
            return None
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def _clean_web_content(self, content: str) -> str:
        """Clean scraped web content"""
        if not content:
            return ""
        
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove navigation and common web elements
        noise_patterns = [
            r'Home\s*>\s*[\w\s]*>',  # Breadcrumbs
            r'Skip to [\w\s]*',       # Skip links
            r'Copyright.*\d{4}',      # Copyright notices
            r'All rights reserved',   # Rights notices
            r'Privacy Policy',        # Privacy links
            r'Terms of Use',          # Terms links
            r'Contact Us',            # Contact links
            r'Login\s*Register',      # Login/Register
        ]
        
        for pattern in noise_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # Remove repeated phrases
        lines = content.split('\n')
        cleaned_lines = []
        seen_lines = set()
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 10 and line not in seen_lines:
                cleaned_lines.append(line)
                seen_lines.add(line)
        
        return '\n'.join(cleaned_lines).strip()
    
    async def _extract_pdf_text_from_file(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num}: {e}")
                        continue
            
            return text.strip()
        except Exception as e:
            logger.error(f"Error reading PDF {file_path}: {e}")
            return ""
    
    async def _extract_html_text_from_file(self, file_path: Path) -> str:
        """Extract text from HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            return soup.get_text(separator=' ', strip=True)
        except Exception as e:
            logger.error(f"Error reading HTML {file_path}: {e}")
            return ""
    
    async def _extract_text_from_file(self, file_path: Path) -> str:
        """Extract text from plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            return ""
    
    async def _extract_docx_text_from_file(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        try:
            import docx
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error reading DOCX {file_path}: {e}")
            return ""
    
    async def _create_document_chunks(
        self, 
        content: str, 
        bank_name: str, 
        card_id: str, 
        card_name: str, 
        doc_config: Dict
    ) -> List[Dict]:
        """Create chunks from document content"""
        if not content or len(content.strip()) < 100:
            return []
        
        chunks = []
        chunk_size = 1000
        overlap = 200
        
        # Clean content
        content = self._clean_text_content(content)
        
        # Create base metadata
        base_metadata = {
            "bank": bank_name,
            "card_id": card_id,
            "card_name": card_name,
            "document_type": doc_config.get('document_category', 'general'),
            "source_type": doc_config['type'],
            "source_url": doc_config.get('url', ''),
            "source_file": doc_config.get('file_path', ''),
            "description": doc_config.get('description', ''),
            "processed_at": datetime.now().isoformat()
        }
        
        # Create chunks
        chunk_index = 0
        for i in range(0, len(content), chunk_size - overlap):
            chunk_text = content[i:i + chunk_size].strip()
            
            if len(chunk_text) < 100:  # Skip very short chunks
                continue
            
            chunk = {
                "id": f"{bank_name}_{card_id}_{doc_config['type']}_{chunk_index}",
                "content": chunk_text,
                "metadata": {
                    **base_metadata,
                    "chunk_index": chunk_index,
                    "chunk_start": i,
                    "chunk_end": min(i + chunk_size, len(content)),
                    "chunk_length": len(chunk_text)
                }
            }
            
            chunks.append(chunk)
            chunk_index += 1
        
        return chunks
    
    def _clean_text_content(self, content: str) -> str:
        """Clean and normalize text content"""
        if not content:
            return ""
        
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove special characters but keep essential punctuation
        content = re.sub(r'[^\w\s.,;:!?()%-₹]', ' ', content)
        
        # Remove multiple spaces
        content = re.sub(r' +', ' ', content)
        
        # Strip leading/trailing whitespace
        content = content.strip()
        
        return content
    
    async def _save_chunks(self, chunks: List[Dict], filename_prefix: str) -> bool:
        """Save chunks to JSON file"""
        try:
            filename = f"{filename_prefix}_chunks.json"
            file_path = self.chunks_path / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            logger.error(f"Error saving chunks: {e}")
            return False
    
    def add_document_source(
        self, 
        bank_name: str, 
        card_id: str, 
        card_name: str, 
        doc_config: Dict
    ):
        """Add a new document source to configuration"""
        if bank_name not in self.config['banks']:
            self.config['banks'][bank_name] = {
                "name": bank_name.title(),
                "cards": []
            }
        
        # Find or create card
        card_found = False
        for card in self.config['banks'][bank_name]['cards']:
            if card['id'] == card_id:
                card['documents'].append(doc_config)
                card_found = True
                break
        
        if not card_found:
            self.config['banks'][bank_name]['cards'].append({
                "id": card_id,
                "name": card_name,
                "documents": [doc_config]
            })
        
        # Save updated configuration
        self._save_config()


# Async function for easy usage
async def process_all_documents():
    """Convenience function to process all documents"""
    processor = UniversalDocumentProcessor()
    return await processor.process_all_documents()


if __name__ == "__main__":
    asyncio.run(process_all_documents()) 