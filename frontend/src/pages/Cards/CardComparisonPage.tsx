import React, { useState, useEffect, useRef } from 'react';
import { Search, Filter, Download, Info, AlertCircle, Loader2, CreditCard } from 'lucide-react';
import { cardMasterDataAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';

// Add html2canvas import for image generation
import html2canvas from 'html2canvas';

interface CardData {
  id: number;
  bank_name: string;
  card_name: string;
  display_name: string;
  joining_fee_display: string;
  annual_fee_display: string;
  annual_fee_waiver_spend: number | null;
  domestic_lounge_visits: number | null;
  lounge_spend_requirement: number | null;
  lounge_spend_period: string | null;
  categories: Record<string, string>;
  merchants: Record<string, string>;
  additional_info: string;
}

const CardComparisonPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [cardData, setCardData] = useState<CardData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showUserCards, setShowUserCards] = useState(true);
  const exportRef = useRef<HTMLDivElement>(null);
  const { user } = useAuth();

  // Fetch card comparison data
  useEffect(() => {
    const fetchCardData = async () => {
      try {
        setLoading(true);
        console.log(`Fetching comparison data with userCardsOnly: ${showUserCards}`);
        
        // First, let's check if user is authenticated
        try {
          const authResponse = await fetch('http://localhost:8000/api/v1/card-master-data/debug/user', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
          });
          const authData = await authResponse.json();
          console.log('Authentication debug:', authData);
        } catch (authErr) {
          console.error('Auth debug error:', authErr);
        }
        
        const data = await cardMasterDataAPI.getComparison(showUserCards);
        console.log(`Card comparison data fetched:`, {
          mode: showUserCards ? 'User Cards Only' : 'All Cards',
          totalCards: data.length,
          cards: data.map((card: CardData) => ({ id: card.id, name: card.display_name, bank: card.bank_name }))
        });
        setCardData(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching card data:', err);
        setError('Failed to load card comparison data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchCardData();
  }, [showUserCards]);

  // Helper function to get the color for a card based on bank
  const getCardColor = (bankName: string) => {
    const colors: Record<string, string> = {
      'SBI': 'bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800',
      'HDFC': 'bg-orange-50 border-orange-200 dark:bg-orange-900/20 dark:border-orange-800',
      'AXIS': 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800',
      'ICICI': 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800',
      'KOTAK': 'bg-purple-50 border-purple-200 dark:bg-purple-900/20 dark:border-purple-800',
    };
    return colors[bankName.toUpperCase()] || 'bg-gray-50 border-gray-200 dark:bg-gray-900/20 dark:border-gray-800';
  };

  // Helper function to get text color that contrasts well with card background
  const getCardTextColor = (bankName: string) => {
    // Use dark text for light backgrounds, light text for dark backgrounds
    return 'text-gray-900 dark:text-gray-100';
  };

  // Helper function to format lounge visits
  const formatLoungeVisits = (card: CardData) => {
    if (!card.domestic_lounge_visits) return '-';
    return `${card.domestic_lounge_visits} visits/year`;
  };

  // Helper function to format lounge spend requirement
  const formatLoungeSpends = (card: CardData) => {
    if (!card.lounge_spend_requirement) return '-';
    const amount = card.lounge_spend_requirement;
    const period = card.lounge_spend_period || 'quarter';
    return `₹${(amount / 1000).toFixed(0)}K/${period}`;
  };

  // Get all unique categories and merchants for the table headers
  const allCategories = Array.from(
    new Set(cardData.flatMap(card => Object.keys(card.categories)))
  );
  
  const allMerchants = Array.from(
    new Set(cardData.flatMap(card => Object.keys(card.merchants)))
  );

  // Filter cards based on search term and category
  const filteredCards = cardData.filter(card => {
    const matchesSearch = card.display_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         card.bank_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || 
                           Object.keys(card.categories).includes(selectedCategory) ||
                           Object.keys(card.merchants).includes(selectedCategory);
    return matchesSearch && matchesCategory;
  });

  // Get color for reward rate - highlight only the highest value(s) in each row
  const getCellColor = (value: string, rowValues: string[]) => {
    if (value === '-' || value === '') return '';
    
    // Get all numeric values in the row
    const numericValues = rowValues
      .map(v => v === '-' || v === '' ? 0 : parseFloat(v.replace(/[^0-9.]/g, '')))
      .filter(v => v > 0);
    
    if (numericValues.length === 0) return '';
    
    const maxValue = Math.max(...numericValues);
    const currentValue = parseFloat(value.replace(/[^0-9.]/g, ''));
    
    // Highlight only if this cell has the maximum value
    if (currentValue === maxValue && currentValue > 0) {
      return 'text-green-600 font-semibold bg-green-50 dark:bg-green-900/20 dark:text-green-400';
    }
    
    return '';
  };



  // Export table as image with branding
  const handleExport = async () => {
    if (!exportRef.current) return;

    try {
      // Show loading state
      const exportButton = document.querySelector('[data-export-button]') as HTMLButtonElement;
      const originalText = exportButton?.innerHTML;
      if (exportButton) {
        exportButton.innerHTML = '<Loader2 className="w-4 h-4 animate-spin" /> Generating...';
        exportButton.disabled = true;
      }



      // Get user information from useAuth hook
      const getUserDisplayName = () => {
        if (user?.first_name && user?.last_name) {
          return `${user.first_name} ${user.last_name}`;
        } else if (user?.first_name) {
          return user.first_name;
        } else if (user?.email) {
          return user.email.split('@')[0];
        }
        return 'Smart User';
      };

      const userName = getUserDisplayName();
      
      // Generate personalized tagline - random selection for fresh experience
      const getPersonalizedTagline = () => {
        const taglines = [
          "Used by those who read the fine print.",
          "Financially fluent.",
          "Because average isn't your style.",
          "Because you're not here to guess.",
          "Because smart isn't a feature — it's who you are.",
          "For those who optimize.",
          "You're not chasing points — you're winning them.",
          "Smart Money, Smart Choices! 💰",
          "Your Financial Journey Starts Here! 🚀",
          "Making Every Swipe Count! 💳",
          "Empowering Your Financial Freedom! ⭐",
          "Smart Cards, Smarter You! 🎯",
          "Your Path to Financial Success! 💎",
          "Building Wealth, One Card at a Time! 🏆",
          "Smart Decisions, Better Rewards! 🎉",
          "Your Financial Future is Bright! ✨",
          "Mastering the Art of Smart Spending! 🎨"
        ];
        
        // Random selection for fresh experience each time
        return taglines[Math.floor(Math.random() * taglines.length)];
      };

      const personalizedTagline = getPersonalizedTagline();

      // Create a temporary container for the export
      const tempContainer = document.createElement('div');
      tempContainer.style.position = 'absolute';
      tempContainer.style.left = '-9999px';
      tempContainer.style.top = '0';
      tempContainer.style.width = '1800px'; // Increased width to accommodate more cards
      tempContainer.style.backgroundColor = 'white';
      tempContainer.style.padding = '20px';
      tempContainer.style.fontFamily = 'Inter, system-ui, sans-serif';
      
      // Clone the table content
      const tableClone = exportRef.current.cloneNode(true) as HTMLElement;
      
      // Trim card names for image export (remove common words)
      const trimCardName = (cardName: string) => {
        return cardName
          .replace(/\b(Bank|Card|Credit|Premium|Co-branded|Co-brand|Standard|Signature|World|Select|Miles|Points|Smart|Plus|Pro|Ultra|Max|Prime|Infinite|Unlimited|Freedom|Liberty|Choice|Optimal|Best|Super|Mega|Grand|Royal|Imperial|Supreme|Ultimate|Exclusive|Premium|Deluxe|Luxury|Elite|Platinum|Gold|Silver|Bronze|Classic|Basic|Entry|Starter|Student|Youth|Senior|Women|Men|Family|Business|Corporate|Travel|Shopping|Dining|Fuel|Grocery|Entertainment|Lifestyle|Sports|Fitness|Health|Medical|Education|Technology|Digital|Online|Offline|Contactless|Chip|Magnetic|Virtual|Physical|Metal|Plastic|Carbon|Wood|Bamboo|Eco|Green|Sustainable|Organic|Natural|Pure|Simple|Easy|Quick|Fast|Instant|Immediate|Direct|Straight|Clear|Transparent|Honest|Fair|Just|Right|Good|Better|Best|Perfect|Ideal|Optimal|Optimum|Maximum|Minimum|Average|Normal|Regular|Standard|Basic|Simple|Easy|Convenient|Comfortable|Reliable|Secure|Safe|Protected|Guarded|Shielded|Covered|Insured|Guaranteed|Warranted|Assured|Confirmed|Verified|Validated|Authenticated|Certified|Approved|Authorized|Licensed|Registered|Official|Formal|Professional|Expert|Specialist|Master|Guru|Wizard|Genius|Brilliant|Smart|Intelligent|Clever|Wise|Sage|Scholar|Academic|Theoretical|Practical|Applied|Real|Actual|True|Genuine|Authentic|Original|Natural|Pure|Clean|Fresh|New|Modern|Contemporary|Current|Latest|Recent|Updated|Upgraded|Enhanced|Improved|Better|Superior|Excellent|Outstanding|Exceptional|Extraordinary|Amazing|Wonderful|Fantastic|Fabulous|Terrific|Great|Good|Nice|Fine|Okay|Alright|Acceptable|Satisfactory|Adequate|Sufficient|Enough|Plenty|Abundant|Rich|Wealthy|Prosperous|Successful|Thriving|Flourishing|Growing|Expanding|Developing|Progressing|Advancing|Moving|Going|Running|Working|Operating|Functioning|Performing|Acting|Doing|Making|Creating|Building|Constructing|Developing|Designing|Planning|Organizing|Managing|Controlling|Directing|Leading|Guiding|Helping|Supporting|Assisting|Aiding|Serving|Providing|Offering|Giving|Sharing|Contributing|Adding|Including|Involving|Engaging|Connecting|Linking|Joining|Combining|Merging|Integrating|Unifying|Uniting|Bringing|Taking|Getting|Receiving|Accepting|Welcoming|Embracing|Adopting|Following|Pursuing|Chasing|Seeking|Looking|Finding|Discovering|Exploring|Investigating|Researching|Studying|Learning|Understanding|Knowing|Realizing|Recognizing|Identifying|Naming|Calling|Referring|Mentioning|Discussing|Talking|Speaking|Communicating|Expressing|Showing|Displaying|Presenting|Demonstrating|Illustrating|Explaining|Describing|Defining|Clarifying|Simplifying|Making|Creating|Building|Developing|Designing|Planning|Organizing|Managing|Controlling|Directing|Leading|Guiding|Helping|Supporting|Assisting|Aiding|Serving|Providing|Offering|Giving|Sharing|Contributing|Adding|Including|Involving|Engaging|Connecting|Linking|Joining|Combining|Merging|Integrating|Unifying|Uniting|Bringing|Taking|Getting|Receiving|Accepting|Welcoming|Embracing|Adopting|Following|Pursuing|Chasing|Seeking|Looking|Finding|Discovering|Exploring|Investigating|Researching|Studying|Learning|Understanding|Knowing|Realizing|Recognizing|Identifying|Naming|Calling|Referring|Mentioning|Discussing|Talking|Speaking|Communicating|Expressing|Showing|Displaying|Presenting|Demonstrating|Illustrating|Explaining|Describing|Defining|Clarifying|Simplifying)\b/gi, '')
          .replace(/\s+/g, ' ')
          .trim();
      };
      
      // Apply card name trimming to the cloned table
      const cardNameElements = tableClone.querySelectorAll('th div:first-child');
      cardNameElements.forEach((element) => {
        if (element.textContent) {
          element.textContent = trimCardName(element.textContent);
        }
      });
      
      // Set fixed column widths for better layout
      const table = tableClone.querySelector('table') as HTMLElement;
      if (table) {
        table.style.width = '100%';
        table.style.tableLayout = 'fixed';
        
        // Set column widths
        const firstColumn = table.querySelector('th:first-child, td:first-child') as HTMLElement;
        if (firstColumn) {
          firstColumn.style.width = '200px';
          firstColumn.style.minWidth = '200px';
        }
        
        // Set other columns to equal width - dynamic approach
        const otherColumns = table.querySelectorAll('th:not(:first-child), td:not(:first-child)');
        const availableWidth = 1800 - 200 - 40; // Total width - first column - padding
        const cardCount = filteredCards.length;
        const columnWidth = cardCount > 0 ? `${availableWidth / cardCount}px` : '150px';
        
        console.log('Column width calculation:', {
          availableWidth,
          cardCount,
          columnWidth
        });
        
        otherColumns.forEach((col) => {
          const colElement = col as HTMLElement;
          colElement.style.width = columnWidth;
          colElement.style.minWidth = columnWidth;
          colElement.style.maxWidth = columnWidth;
        });
        
        // Apply table styling for better readability in image export
        table.style.borderCollapse = 'collapse';
        table.style.border = '1px solid #e0e0e0';
        
        // Style all cells with borders and padding
        const allCells = table.querySelectorAll('th, td');
        allCells.forEach((cell) => {
          const cellElement = cell as HTMLElement;
          cellElement.style.border = '1px solid #e0e0e0';
          cellElement.style.padding = '8px';
          cellElement.style.textAlign = 'center';
          cellElement.style.fontSize = '16px';
          cellElement.style.fontFamily = 'Inter, system-ui, sans-serif';
          cellElement.style.color = '#333333'; // Ensure dark text for visibility
        });
        
        // Style first column (Card Details) with light blue background
        const firstColumnCells = table.querySelectorAll('th:first-child, td:first-child');
        firstColumnCells.forEach((cell) => {
          const cellElement = cell as HTMLElement;
          cellElement.style.backgroundColor = '#e3f2fd';
          cellElement.style.fontWeight = 'bold';
          cellElement.style.textAlign = 'left';
          cellElement.style.color = '#333333'; // Ensure dark text on light blue background
        });
        
        // Style header row with dark blue background
        const headerRow = table.querySelector('thead tr');
        if (headerRow) {
          const headerCells = headerRow.querySelectorAll('th');
          headerCells.forEach((cell) => {
            const cellElement = cell as HTMLElement;
            cellElement.style.backgroundColor = '#1976d2';
            cellElement.style.color = 'white';
            cellElement.style.fontWeight = 'bold';
            cellElement.style.fontSize = '20px';
          });
        }
        
        // Style section headers (Spending Categories, Merchant Rewards) with light yellow background
        const sectionHeaders = table.querySelectorAll('td');
        sectionHeaders.forEach((cell) => {
          const cellElement = cell as HTMLElement;
          if (cellElement.textContent && (
            cellElement.textContent.includes('Spending Categories') ||
            cellElement.textContent.includes('Merchant Rewards') ||
            cellElement.textContent.includes('Card Details') ||
            cellElement.textContent.includes('Additional Info')
          )) {
            cellElement.style.backgroundColor = '#fff8e1';
            cellElement.style.fontWeight = 'bold';
            cellElement.style.fontSize = '18px';
            cellElement.style.color = '#333333'; // Ensure dark text on light yellow background
          }
        });


        

        
        // Apply alternating row colors for better readability
        const dataRows = table.querySelectorAll('tbody tr');
        dataRows.forEach((row, index) => {
          const rowElement = row as HTMLElement;
          const cells = rowElement.querySelectorAll('td');
          
          // Skip section header rows (they already have yellow background)
          const firstCell = cells[0];
          if (firstCell && (
            firstCell.textContent?.includes('Spending Categories') ||
            firstCell.textContent?.includes('Merchant Rewards') ||
            firstCell.textContent?.includes('Card Details') ||
            firstCell.textContent?.includes('Additional Info')
          )) {
            return; // Skip this row
          }
          
          // Apply alternating colors to data rows
          cells.forEach((cell) => {
            const cellElement = cell as HTMLElement;
            if (index % 2 === 0) {
              cellElement.style.backgroundColor = '#ffffff';
            } else {
              cellElement.style.backgroundColor = '#f8f9fa';
            }
            cellElement.style.color = '#333333'; // Ensure dark text on both white and gray backgrounds
          });
        });
        
        // Highlight highest values in each row with green background
        const highlightRows = table.querySelectorAll('tbody tr');
        highlightRows.forEach((row) => {
          const rowElement = row as HTMLElement;
          const cells = rowElement.querySelectorAll('td');
          
          // Skip section header rows and first column
          const firstCell = cells[0];
          if (firstCell && (
            firstCell.textContent?.includes('Spending Categories') ||
            firstCell.textContent?.includes('Merchant Rewards') ||
            firstCell.textContent?.includes('Card Details') ||
            firstCell.textContent?.includes('Additional Info')
          )) {
            return; // Skip this row
          }
          
          // Get all numeric values from the row (excluding first column)
          const numericValues: { value: number; cell: HTMLElement }[] = [];
          for (let i = 1; i < cells.length; i++) {
            const cell = cells[i] as HTMLElement;
            const text = cell.textContent?.trim() || '';
            
            // Extract percentage values (e.g., "5.0%", "10%", "1.5%")
            const percentageMatch = text.match(/(\d+(?:\.\d+)?)%/);
            if (percentageMatch) {
              const value = parseFloat(percentageMatch[1]);
              if (value > 0) { // Only consider positive values
                numericValues.push({ value, cell });
              }
            }
          }
          
          // Find the highest value(s)
          if (numericValues.length > 0) {
            const maxValue = Math.max(...numericValues.map(item => item.value));
            
            // Highlight all cells with the highest value
            numericValues.forEach(({ value, cell }) => {
              if (value === maxValue) {
                cell.style.backgroundColor = '#e8f5e8'; // Light green background
                cell.style.fontWeight = 'bold';
                cell.style.color = '#2e7d32'; // Dark green text
              }
            });
          }
        });
        
        // DEBUG: Log table structure
        console.log('=== EXPORT DEBUG ===');
        console.log('Total rows found:', table.querySelectorAll('tbody tr').length);
        
        // Special handling for Additional Info row - ensure all cells in that row have proper text color
        // This runs AFTER all other styling to override any previous font size settings
        const additionalInfoRows = table.querySelectorAll('tbody tr');
        console.log('Processing', additionalInfoRows.length, 'rows for Additional Info styling');
        
        additionalInfoRows.forEach((row, rowIndex) => {
          const rowElement = row as HTMLElement;
          const cells = rowElement.querySelectorAll('td');
          
          // Check if this is the Additional Info row - more robust detection
          const firstCell = cells[0];
          const isAdditionalInfoRow = firstCell && (
            firstCell.textContent?.includes('Additional Info') ||
            firstCell.textContent?.includes('additional_info') ||
            firstCell.textContent?.toLowerCase().includes('additional')
          );
          
          if (isAdditionalInfoRow) {
            console.log(`Found Additional Info row at index ${rowIndex}`);
            console.log('First cell text:', firstCell.textContent);
            console.log('Number of cells in this row:', cells.length);
            
            // Style all cells in the Additional Info row for better visibility
            cells.forEach((cell, cellIndex) => {
              const cellElement = cell as HTMLElement;
              const textLength = cellElement.textContent?.length || 0;
              
              console.log(`Cell ${cellIndex} text length:`, textLength);
              console.log(`Cell ${cellIndex} text:`, cellElement.textContent);
              
              // Fixed font size for better readability
              const fontSize = '16px';
              
              console.log(`Cell ${cellIndex} font size set to:`, fontSize);
              
              cellElement.style.color = '#000000'; // Force dark text for visibility
              cellElement.style.fontSize = fontSize; // Fixed font size
              cellElement.style.textAlign = 'left'; // Left align for better readability
              cellElement.style.fontWeight = 'normal'; // Normal weight for content
              cellElement.style.backgroundColor = '#fff8e1'; // Keep light yellow background
              
              console.log(`Cell ${cellIndex} styles applied:`, {
                color: cellElement.style.color,
                fontSize: cellElement.style.fontSize,
                backgroundColor: cellElement.style.backgroundColor
              });
            });
          }
        });
        
        console.log('=== END EXPORT DEBUG ===');
        
        // Fallback: If Additional Info row not found by name, look for rows with long text content
        let additionalInfoRowFound = false;
        additionalInfoRows.forEach((row, rowIndex) => {
          const rowElement = row as HTMLElement;
          const cells = rowElement.querySelectorAll('td');
          const firstCell = cells[0];
          
          if (firstCell && firstCell.textContent?.includes('Additional Info')) {
            additionalInfoRowFound = true;
          }
        });
        
        if (!additionalInfoRowFound) {
          console.log('Additional Info row not found by name, looking for rows with long text...');
          
          additionalInfoRows.forEach((row, rowIndex) => {
            const rowElement = row as HTMLElement;
            const cells = rowElement.querySelectorAll('td');
            
            // Check if any cell in this row has long text (typical of Additional Info)
            let hasLongText = false;
            cells.forEach((cell) => {
              const cellElement = cell as HTMLElement;
              const textLength = cellElement.textContent?.length || 0;
              if (textLength > 50) { // Long text threshold
                hasLongText = true;
              }
            });
            
            if (hasLongText) {
              console.log(`Found row ${rowIndex} with long text, applying Additional Info styling`);
              
              cells.forEach((cell, cellIndex) => {
                const cellElement = cell as HTMLElement;
                const textLength = cellElement.textContent?.length || 0;
                
                // Fixed font size for better readability
                const fontSize = '16px';
                
                cellElement.style.color = '#000000';
                cellElement.style.fontSize = fontSize;
                cellElement.style.textAlign = 'left';
                cellElement.style.fontWeight = 'normal';
                cellElement.style.backgroundColor = '#fff8e1';
                
                console.log(`Fallback styling applied to cell ${cellIndex}:`, {
                  textLength,
                  fontSize,
                  text: cellElement.textContent?.substring(0, 50) + '...'
                });
              });
            }
          });
        }
      }
      
      // Add branding header with personalized user info
      const brandingHeader = document.createElement('div');
      brandingHeader.style.cssText = `
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 2px solid #0284c7;
        font-family: 'Inter', system-ui, sans-serif;
      `;
      
      const currentDate = new Date().toLocaleDateString();
      
      // Left side - Brand info
      const brandSection = document.createElement('div');
      brandSection.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
          <div style="width: 32px; height: 32px; background: #0284c7; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">💳</div>
          <div>
            <div style="font-size: 20px; font-weight: bold; color: #1f2937;">UNGI SmartCards AI</div>
            <div style="font-size: 14px; color: #6b7280;">Credit Card Comparison Report</div>
          </div>
        </div>
        <div style="font-size: 14px; color: #6b7280; margin-top: 8px;">Generated on: ${currentDate}</div>
      `;
      
      // Right side - Personalized user info
      const userSection = document.createElement('div');
      userSection.style.cssText = `
        text-align: right;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 4px;
      `;
      userSection.innerHTML = `
        <div style="font-size: 18px; font-weight: 600; color: #1f2937; margin-bottom: 4px;">Hello, ${userName}! 👋</div>
        <div style="font-size: 14px; color: #0284c7; font-weight: 500; font-style: italic;">${personalizedTagline}</div>
        <div style="font-size: 12px; color: #6b7280; margin-top: 4px;">Your personalized comparison report</div>
      `;
      
      brandingHeader.appendChild(brandSection);
      brandingHeader.appendChild(userSection);
      

      
      // Add branding footer
      const brandingFooter = document.createElement('div');
      brandingFooter.style.cssText = `
        margin-top: 20px;
        text-align: center;
        font-size: 12px;
        color: #6b7280;
        font-family: 'Inter', system-ui, sans-serif;
      `;
      brandingFooter.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
          <div style="font-size: 12px; color: #6b7280;">© 2025 UNGI SmartCards AI. Every swipe, Optimized.</div>
          <div style="font-size: 11px; color: #9ca3af;">
            For personalized credit card recommendations and detailed capping information, visit: 
            <span style="color: #2563eb; font-weight: bold; text-decoration: underline; margin-left: 4px;">
              https://smartcards-ai-frontend.onrender.com/
            </span>
          </div>
        </div>
      `;
      
      // Assemble the export content
      tempContainer.appendChild(brandingHeader);
      tempContainer.appendChild(tableClone);
      tempContainer.appendChild(brandingFooter);
      
      // Add to DOM temporarily
      document.body.appendChild(tempContainer);
      
      // Generate image using html2canvas
      const canvas = await html2canvas(tempContainer, {
        background: '#ffffff',
        useCORS: true,
        allowTaint: true,
        logging: false,
      });
      
      // Remove temporary container
      document.body.removeChild(tempContainer);
      
      // Convert to blob and download
      canvas.toBlob((blob: Blob | null) => {
        if (blob) {
          const url = URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = `credit-card-comparison-${userName}-${new Date().toISOString().split('T')[0]}.png`;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          URL.revokeObjectURL(url);
        }
      }, 'image/png', 0.9);
      
    } catch (error) {
      console.error('Export failed:', error);
      alert('Failed to generate image. Please try again.');
    } finally {
      // Restore button state
      const exportButton = document.querySelector('[data-export-button]') as HTMLButtonElement;
      if (exportButton) {
        exportButton.innerHTML = '<Download className="w-4 h-4" /><span className="hidden sm:inline">Download Image</span><span className="sm:hidden">Download</span>';
        exportButton.disabled = false;
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="flex items-center justify-center h-64">
          <Loader2 className="w-8 h-8 animate-spin text-primary-600 dark:text-primary-400" />
          <span className="ml-2 text-gray-900 dark:text-white">Loading card comparison data...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
            <p className="text-red-600 dark:text-red-400 mb-4">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-2 sm:p-4">
      <div className="w-full">
        {/* Header */}
        <div className="mb-4 sm:mb-6">
          <h1 className="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-2">Credit Card Comparison</h1>
          <p className="text-sm sm:text-base text-gray-600 dark:text-gray-300">
            {showUserCards 
              ? "Compare your added cards to see which offers the best rewards and benefits" 
              : "Compare rewards, fees, and benefits across different credit cards"
            }
          </p>
          {!loading && (
            <div className="mt-2 text-xs sm:text-sm text-gray-500 dark:text-gray-400">
              {showUserCards 
                ? `Showing ${cardData.length} of your cards (${filteredCards.length} after filtering)`
                : `Showing ${cardData.length} total cards (${filteredCards.length} after filtering)`
              }
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-3 sm:p-4 mb-4 sm:mb-6 border border-gray-200 dark:border-gray-700">
          <div className="flex flex-col lg:flex-row gap-3 sm:gap-4 items-start lg:items-center justify-between">
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 flex-1 w-full">
              {/* Search */}
              <div className="relative flex-1 min-w-0">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search cards or banks..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent w-full bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 text-sm"
                />
              </div>

              {/* Category Filter */}
              <div className="relative flex-shrink-0">
                <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 w-4 h-4" />
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="pl-10 pr-8 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                >
                  <option value="all">All Categories</option>
                  {allCategories.map(category => (
                    <option key={category} value={category}>
                      {category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </option>
                  ))}
                  {allMerchants.map(merchant => (
                    <option key={merchant} value={merchant}>
                      {merchant.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </option>
                  ))}
                </select>
              </div>

              {/* User Cards Toggle */}
              <label className="flex items-center space-x-2 flex-shrink-0">
                <input
                  type="checkbox"
                  checked={showUserCards}
                  onChange={(e) => setShowUserCards(e.target.checked)}
                  className="rounded border-gray-300 dark:border-gray-600 text-primary-600 focus:ring-primary-500 dark:bg-gray-700"
                />
                <span className="text-xs sm:text-sm text-gray-700 dark:text-gray-300 whitespace-nowrap">
                  {showUserCards ? 'My Cards Only' : 'All Cards'}
                </span>
              </label>
            </div>

            {/* Export Button */}
            <button
              onClick={handleExport}
              className="flex items-center gap-2 px-3 sm:px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors text-sm whitespace-nowrap"
              data-export-button
            >
              <Download className="w-4 h-4" />
              <span className="hidden sm:inline">Download Image</span>
              <span className="sm:hidden">Download</span>
            </button>
          </div>
        </div>

        {filteredCards.length === 0 ? (
          <div className="text-center py-8 sm:py-12">
            <Info className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
            <p className="text-sm sm:text-base text-gray-600 dark:text-gray-300">
              {showUserCards 
                ? "You haven't added any cards yet. Add some cards from your dashboard to compare them here."
                : "No cards found matching your criteria."
              }
            </p>
            {showUserCards && (
              <button
                onClick={() => window.location.href = '/cards/add'}
                className="mt-4 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors text-sm"
              >
                Add Your First Card
              </button>
            )}
          </div>
        ) : (
          /* Comparison Table */
          <div ref={exportRef} className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
            {/* Branding Header - Only visible in exports */}
            <div className="hidden print:block p-4 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                    <CreditCard className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <div className="text-lg font-bold text-gray-900 dark:text-white">UNGI SmartCards AI</div>
                    <div className="text-sm text-gray-600 dark:text-gray-300">Credit Card Comparison Report</div>
                  </div>
                </div>
                <div className="text-sm text-gray-500 dark:text-gray-400">
                  Generated on: {new Date().toLocaleDateString()}
                </div>
              </div>
            </div>
            
            {/* Responsive table container */}
            <div className="overflow-x-auto">
              <table className="w-full text-xs sm:text-sm min-w-full">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
                    <th className="text-left p-2 sm:p-3 font-semibold sticky left-0 bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 min-w-[120px] sm:min-w-[150px] text-gray-900 dark:text-white z-10">
                      Card Details
                    </th>
                    {filteredCards.map((card) => (
                      <th key={card.id} className={`p-2 sm:p-3 text-center min-w-[100px] sm:min-w-[120px] border-r border-gray-200 dark:border-gray-700 ${getCardColor(card.bank_name)}`}>
                        <div className={`font-semibold ${getCardTextColor(card.bank_name)} text-xs sm:text-sm`}>{card.display_name}</div>
                        <div className={`text-xs mt-1 ${getCardTextColor(card.bank_name)} opacity-75`}>{card.bank_name}</div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {/* Basic Information */}
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <td className="p-2 sm:p-3 font-medium sticky left-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm z-10">Joining Fee</td>
                    {filteredCards.map((card) => (
                      <td key={card.id} className="p-2 sm:p-3 text-center border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm">{card.joining_fee_display}</td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <td className="p-2 sm:p-3 font-medium sticky left-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm z-10">Annual Fee</td>
                    {filteredCards.map((card) => (
                      <td key={card.id} className="p-2 sm:p-3 text-center border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm">{card.annual_fee_display}</td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <td className="p-2 sm:p-3 font-medium sticky left-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm z-10">Lounge Visits</td>
                    {filteredCards.map((card) => (
                      <td key={card.id} className="p-2 sm:p-3 text-center border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm">{formatLoungeVisits(card)}</td>
                    ))}
                  </tr>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <td className="p-2 sm:p-3 font-medium sticky left-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm z-10">Lounge Spends</td>
                    {filteredCards.map((card) => (
                      <td key={card.id} className="p-2 sm:p-3 text-center border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm">{formatLoungeSpends(card)}</td>
                    ))}
                  </tr>

                  {/* Categories */}
                  {allCategories.length > 0 && (
                    <>
                      <tr className="bg-primary-50 dark:bg-primary-900/20">
                        <td className="p-2 sm:p-3 font-semibold sticky left-0 bg-primary-50 dark:bg-primary-900/20 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm z-10" colSpan={filteredCards.length + 1}>
                        Spending Categories
                      </td>
                      </tr>
                      {allCategories.map((category) => (
                        <tr key={category} className="border-b border-gray-200 dark:border-gray-700">
                          <td className="p-2 sm:p-3 font-medium sticky left-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm z-10">
                            {category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                          </td>
                          {filteredCards.map((card) => {
                            const rowValues = filteredCards.map(c => c.categories[category] || '-');
                            return (
                              <td key={card.id} className={`p-2 sm:p-3 text-center border-r border-gray-200 dark:border-gray-700 text-xs sm:text-sm ${getCellColor(card.categories[category] || '-', rowValues)}`}>
                                {card.categories[category] || '-'}
                              </td>
                            );
                          })}
                        </tr>
                      ))}
                    </>
                  )}

                  {/* Merchants */}
                  {allMerchants.length > 0 && (
                    <>
                      <tr className="bg-green-50 dark:bg-green-900/20">
                        <td className="p-2 sm:p-3 font-semibold sticky left-0 bg-green-50 dark:bg-green-900/20 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm z-10" colSpan={filteredCards.length + 1}>
                        Merchant Rewards (Top 10 Popular)
                      </td>
                      </tr>
                      {allMerchants.map((merchant, index) => (
                        <tr key={merchant} className={`border-b border-gray-200 dark:border-gray-700 ${index < 3 ? 'bg-green-25 dark:bg-green-900/10' : ''}`}>
                          <td className="p-2 sm:p-3 font-medium sticky left-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm z-10">
                            <div className="flex items-center">
                              {index < 3 && <span className="text-yellow-500 mr-1">⭐</span>}
                              {merchant.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                            </div>
                          </td>
                          {filteredCards.map((card) => {
                            const rowValues = filteredCards.map(c => c.merchants[merchant] || '-');
                            return (
                              <td key={card.id} className={`p-2 sm:p-3 text-center border-r border-gray-200 dark:border-gray-700 text-xs sm:text-sm ${getCellColor(card.merchants[merchant] || '-', rowValues)}`}>
                                {card.merchants[merchant] || '-'}
                              </td>
                            );
                          })}
                        </tr>
                      ))}
                    </>
                  )}

                  {/* Additional Info */}
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <td className="p-2 sm:p-3 font-semibold sticky left-0 bg-yellow-50 dark:bg-yellow-900/20 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm z-10">Additional Info</td>
                    {filteredCards.map((card) => (
                      <td key={card.id} className="p-2 sm:p-3 text-xs text-center border-r border-gray-200 dark:border-gray-700 max-w-[100px] sm:max-w-[120px] text-gray-900 dark:text-white">
                        <div className="break-words">{card.additional_info || '-'}</div>
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
            {/* Branding Footer - Only visible in exports */}
            <div className="hidden print:block p-4 border-t border-gray-200 dark:border-gray-700 text-center">
              <div className="text-sm text-gray-500 dark:text-gray-400">
                © 2025 UNGI SmartCards AI. Every swipe, Optimized.
              </div>
              <div className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                For personalized credit card recommendations and detailed capping information, visit: https://smartcards-ai-frontend.onrender.com/
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CardComparisonPage; 