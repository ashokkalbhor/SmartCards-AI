import base64

import pytest

from app.services.web_scraping_service import WebScrapingService

# Minimal PDF saying "Hello PDF" (base64 encoded)
HELLO_PDF_BASE64 = (
    "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5k"
    "b2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFszIDAgUl0KL0NvdW50IDEKPj4K"
    "ZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovTWVkaWFCb3gg"
    "WzAgMCAyMDAgMTAwXQovQ29udGVudHMgNCAwIFIKL1Jlc291cmNlcyA8PAovRm9udCA8PAov"
    "RjEgNSAwIFIKPj4KPj4KPj4KZW5kb2JqCjQgMCBvYmoKPDwKL0xlbmd0aCA0MApzdHJlYW0K"
    "QlQKL0YxIDI0IFRmCjUwIDUwIFRkCihIZWxsbyBQREYpIFRqCkVUCmVuZHN0cmVhbQplbmRv"
    "YmoKNSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL05hbWUgL0YxCi9C"
    "YXNlRm9udCAvSGVsdmV0aWNhCj4+CmVuZG9iagp4cmVmCjAgNgowMDAwMDAwMDAgNjU1MzUg"
    "ZiAKMDAwMDAwMDEwIDAwMDAwIG4gCjAwMDAwMDA1MyAwMDAwMCBuIAowMDAwMDAxMDggMDAw"
    "MDAgbiAKMDAwMDAwMTc2IDAwMDAwIG4gCjAwMDAwMDIzMCAwMDAwMCBuIAp0cmFpbGVyCjw8"
    "Ci9Sb290IDEgMCBSCi9TaXplIDYKPj4Kc3RhcnR4cmVmCjI4NAolJUVPRg=="
)


def test_extract_pdf_text_success():
    service = WebScrapingService()
    data = base64.b64decode(HELLO_PDF_BASE64)
    text = service._extract_pdf_text(data)
    assert text is not None
    assert "Hello PDF" in text


def test_extract_pdf_text_handles_failure(monkeypatch):
    service = WebScrapingService()

    def raise_error(_):
        raise ValueError("bad pdf")

    monkeypatch.setattr("app.services.web_scraping_service.PdfReader", raise_error)

    assert service._extract_pdf_text(b"not real") is None
