import pytest
from io import BytesIO
from pathlib import Path
from unittest.mock import Mock, MagicMock
from backend.core.services.cv_service import (
    allowed_resume_file, extract_text_from_pdf, extract_text_from_docx,
    extract_text_from_upload
)


class TestCvServiceExtraction:
    """Test CV/Resume text extraction."""
    
    def test_extract_text_from_pdf_success(self, monkeypatch, tmp_path):
        """Extract text from PDF."""
        # Create mock PDF reader
        mock_page = Mock()
        mock_page.extract_text.return_value = "PDF text content"
        
        mock_reader = Mock()
        mock_reader.pages = [mock_page]
        
        monkeypatch.setattr(
            "backend.core.services.cv_service.PdfReader",
            lambda x: mock_reader
        )
        
        pdf_path = str(tmp_path / "test.pdf")
        text = extract_text_from_pdf(pdf_path)
        
        assert text == "PDF text content"
    
    def test_extract_text_from_pdf_multiple_pages(self, monkeypatch, tmp_path):
        """Extract text from multi-page PDF."""
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page 1 text"
        
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Page 2 text"
        
        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2]
        
        monkeypatch.setattr(
            "backend.core.services.cv_service.PdfReader",
            lambda x: mock_reader
        )
        
        pdf_path = str(tmp_path / "test.pdf")
        text = extract_text_from_pdf(pdf_path)
        
        assert "Page 1 text" in text
        assert "Page 2 text" in text
    
    def test_extract_text_from_pdf_empty_page(self, monkeypatch, tmp_path):
        """Handle empty PDF pages."""
        mock_page = Mock()
        mock_page.extract_text.return_value = None  # Empty page
        
        mock_reader = Mock()
        mock_reader.pages = [mock_page]
        
        monkeypatch.setattr(
            "backend.core.services.cv_service.PdfReader",
            lambda x: mock_reader
        )
        
        pdf_path = str(tmp_path / "test.pdf")
        text = extract_text_from_pdf(pdf_path)
        
        assert text == ""
    
    def test_extract_text_from_docx_success(self, monkeypatch, tmp_path):
        """Extract text from DOCX."""
        mock_para1 = Mock()
        mock_para1.text = "Paragraph 1"
        
        mock_para2 = Mock()
        mock_para2.text = "Paragraph 2"
        
        mock_doc = Mock()
        mock_doc.paragraphs = [mock_para1, mock_para2]
        
        monkeypatch.setattr(
            "backend.core.services.cv_service.Document",
            lambda x: mock_doc
        )
        
        docx_path = str(tmp_path / "test.docx")
        text = extract_text_from_docx(docx_path)
        
        assert "Paragraph 1" in text
        assert "Paragraph 2" in text
    
    def test_extract_text_from_upload_pdf(self, monkeypatch, tmp_path):
        """Extract text detects PDF by extension."""
        monkeypatch.setattr(
            "backend.core.services.cv_service.extract_text_from_pdf",
            lambda x: "PDF extracted"
        )
        
        pdf_path = str(tmp_path / "test.pdf")
        text = extract_text_from_upload(pdf_path)
        
        assert text == "PDF extracted"
    
    def test_extract_text_from_upload_docx(self, monkeypatch, tmp_path):
        """Extract text detects DOCX by extension."""
        monkeypatch.setattr(
            "backend.core.services.cv_service.extract_text_from_docx",
            lambda x: "DOCX extracted"
        )
        
        docx_path = str(tmp_path / "test.docx")
        text = extract_text_from_upload(docx_path)
        
        assert text == "DOCX extracted"
    
    def test_extract_text_from_upload_unsupported(self, tmp_path):
        """Unsupported file type should return empty."""
        unsupported_path = str(tmp_path / "test.txt")
        text = extract_text_from_upload(unsupported_path)
        
        assert text == ""


class TestCvMailService:
    """Test mail service for CV/OTP."""
    
    def test_send_otp_email_structure(self, monkeypatch, app_context):
        """OTP email should have proper structure."""
        from backend.core.services.mail_service import send_otp_email
        
        mock_send = Mock()
        monkeypatch.setattr(
            "backend.core.services.mail_service.send_mail",
            mock_send
        )
        
        send_otp_email("user@example.com", "123456", "login")
        
        # Verify send_mail was called
        assert mock_send.called
        
        # Get call arguments
        call_args = mock_send.call_args
        subject = call_args[0][0]
        recipients = call_args[0][1]
        
        assert "OTP" in subject
        assert "đăng nhập" in subject or "login" in subject.lower()
        assert "user@example.com" in recipients
    
    def test_send_otp_email_register_purpose(self, monkeypatch, app_context):
        """OTP email for register should mention registration."""
        from backend.core.services.mail_service import send_otp_email
        
        mock_send = Mock()
        monkeypatch.setattr(
            "backend.core.services.mail_service.send_mail",
            mock_send
        )
        
        send_otp_email("user@example.com", "654321", "register")
        
        call_args = mock_send.call_args
        subject = call_args[0][0]
        
        assert "OTP" in subject
        assert "đăng ký" in subject or "register" in subject.lower()
    
    def test_send_otp_email_contains_code(self, monkeypatch, app_context):
        """OTP email should contain the code."""
        from backend.core.services.mail_service import send_otp_email
        
        mock_send = Mock()
        monkeypatch.setattr(
            "backend.core.services.mail_service.send_mail",
            mock_send
        )
        
        otp_code = "123456"
        send_otp_email("user@example.com", otp_code, "login")
        
        call_args = mock_send.call_args
        body = call_args[0][2]
        html = call_args[1]["html"] if "html" in call_args[1] else call_args[0][3]
        
        assert otp_code in body
        assert otp_code in html


class TestCvGeneration:
    """Test PDF generation from resume data."""
    
    def test_generate_pdf_basic_structure(self, monkeypatch, tmp_path):
        """Generate PDF should create file."""
        from backend.core.services.cv_service import generate_pdf_from_resume
        
        output_path = str(tmp_path / "output.pdf")
        
        # Mock canvas
        mock_canvas = Mock()
        monkeypatch.setattr(
            "backend.core.services.cv_service.canvas.Canvas",
            lambda x, pagesize: mock_canvas
        )
        
        data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890"
        }
        
        generate_pdf_from_resume(data, output_path)
        
        # Canvas should have been called
        assert mock_canvas.save.called
