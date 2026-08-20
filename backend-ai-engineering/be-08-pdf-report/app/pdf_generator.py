import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Frame, PageTemplate, BaseDocTemplate
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib import colors


class PDFReportGenerator:
    def __init__(self, output_dir: str, base_url: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.base_url = base_url.rstrip("/")
        
        # Colors
        self.primary_color = HexColor("#1a1a2e")
        self.accent_color = HexColor("#e94560")
        self.light_bg = HexColor("#f5f5f5")
        self.table_header_bg = HexColor("#16213e")
        self.table_row_alt = HexColor("#eaeaea")
        
        # Styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Title'],
            fontSize=28,
            leading=34,
            textColor=self.primary_color,
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            leading=18,
            textColor=HexColor("#666666"),
            spaceAfter=24,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            leading=20,
            textColor=self.primary_color,
            spaceBefore=18,
            spaceAfter=10,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderPadding=0,
        ))
        
        self.styles.add(ParagraphStyle(
            name='TableCell',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=12,
            fontName='Helvetica',
        ))
        
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=12,
            fontName='Helvetica-Bold',
            textColor=white,
        ))
        
        self.styles.add(ParagraphStyle(
            name='FooterText',
            parent=self.styles['Normal'],
            fontSize=8,
            leading=10,
            textColor=HexColor("#999999"),
            alignment=TA_CENTER,
        ))
    
    def generate_book_catalog_report(
        self,
        books: List[Dict[str, Any]],
        title: str = "Book Catalog Report",
        filters: Dict[str, Any] = None,
        stats: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate a book catalog PDF report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c if c.isalnum() else "_" for c in title).strip("_")
        filename = f"{safe_title}_{timestamp}.pdf"
        filepath = self.output_dir / filename
        
        # Create document
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=25*mm,
            title=title,
            author="FlyRank Report Generator"
        )
        
        # Build story
        story = []
        
        # Cover page
        story.extend(self._build_cover_page(title, filters, stats))
        story.append(PageBreak())
        
        # Summary statistics
        story.extend(self._build_summary_section(stats))
        story.append(PageBreak())
        
        # Book catalog table
        story.extend(self._build_catalog_table(books))
        
        # Build PDF
        doc.build(
            story,
            onFirstPage=self._add_page_number,
            onLaterPages=self._add_page_number
        )
        
        # Get file info
        file_size = filepath.stat().st_size
        
        # Count pages (approximate)
        page_count = self._estimate_page_count(books)
        
        return {
            "filename": filename,
            "filepath": str(filepath),
            "url": f"{self.base_url}/{filename}",
            "page_count": page_count,
            "file_size_bytes": file_size,
            "generated_at": datetime.now()
        }
    
    def _build_cover_page(self, title: str, filters: Dict, stats: Dict) -> List:
        """Build cover page elements."""
        elements = []
        
        # Spacer to push content down
        elements.append(Spacer(1, 60*mm))
        
        # Title
        elements.append(Paragraph(title, self.styles['ReportTitle']))
        elements.append(Spacer(1, 8*mm))
        
        # Decorative line
        elements.append(HRFlowable(
            width="60%",
            thickness=2,
            color=self.accent_color,
            spaceAfter=12*mm
        ))
        
        # Subtitle
        generated_date = datetime.now().strftime("%B %d, %Y at %H:%M UTC")
        elements.append(Paragraph(
            f"Generated on {generated_date}",
            self.styles['ReportSubtitle']
        ))
        elements.append(Spacer(1, 8*mm))
        
        # Filters applied
        if filters:
            filter_text = []
            if filters.get("category"):
                filter_text.append(f"Category: {filters['category']}")
            if filters.get("min_price") or filters.get("max_price"):
                price_range = []
                if filters.get("min_price"):
                    price_range.append(f"Min £{filters['min_price']:.2f}")
                if filters.get("max_price"):
                    price_range.append(f"Max £{filters['max_price']:.2f}")
                filter_text.append("Price: " + " - ".join(price_range))
            if filters.get("in_stock_only"):
                filter_text.append("In stock only")
            
            if filter_text:
                elements.append(Spacer(1, 10*mm))
                elements.append(Paragraph("Filters Applied:", self.styles['SectionHeader']))
                for f in filter_text:
                    elements.append(Paragraph(f"• {f}", self.styles['Normal']))
        
        # Stats summary
        if stats:
            elements.append(Spacer(1, 15*mm))
            elements.append(Paragraph("Quick Stats:", self.styles['SectionHeader']))
            stats_data = [
                ["Total Books", str(stats.get("total_books", 0))],
                ["Avg Price", f"£{stats.get('avg_price', 0):.2f}"],
                ["Price Range", f"£{stats.get('min_price', 0):.2f} - £{stats.get('max_price', 0):.2f}"],
            ]
            stats_table = Table(stats_data, colWidths=[60*mm, 40*mm])
            stats_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('TEXTCOLOR', (0, 0), (-1, -1), self.primary_color),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(stats_table)
        
        return elements
    
    def _build_summary_section(self, stats: Dict) -> List:
        """Build summary statistics section."""
        elements = []
        
        elements.append(Paragraph("Report Summary", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=1, color=self.accent_color, spaceAfter=8*mm))
        
        if stats:
            summary_text = (
                f"This report contains <b>{stats.get('total_books', 0)} books</b> "
                f"with an average price of <b>£{stats.get('avg_price', 0):.2f}</b>. "
                f"Prices range from <b>£{stats.get('min_price', 0):.2f}</b> to "
                f"<b>£{stats.get('max_price', 0):.2f}</b>."
            )
            elements.append(Paragraph(summary_text, self.styles['Normal']))
            elements.append(Spacer(1, 6*mm))
        
        return elements
    
    def _build_catalog_table(self, books: List[Dict]) -> List:
        """Build the book catalog table."""
        elements = []
        
        elements.append(Paragraph("Book Catalog", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=1, color=self.accent_color, spaceAfter=8*mm))
        
        # Table header
        headers = ["Title", "Category", "Price", "Rating", "Availability"]
        col_widths = [65*mm, 25*mm, 20*mm, 18*mm, 45*mm]
        
        # Prepare data rows
        data = [headers]
        for book in books:
            # Truncate long titles
            title = book.get("title", "")
            if len(title) > 45:
                title = title[:42] + "..."
            
            price = f"£{book.get('price_gbp', 0):.2f}" if book.get('price_gbp') else "N/A"
            rating = str(book.get('rating', '')) if book.get('rating') else "N/A"
            availability = book.get('availability', 'N/A')
            if len(availability) > 30:
                availability = availability[:27] + "..."
            category = book.get('category', 'N/A')
            if len(category) > 18:
                category = category[:15] + "..."
            
            data.append([
                Paragraph(title, self.styles['TableCell']),
                Paragraph(category, self.styles['TableCell']),
                Paragraph(price, self.styles['TableCell']),
                Paragraph(rating, self.styles['TableCell']),
                Paragraph(availability, self.styles['TableCell']),
            ])
        
        # Create table
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        # Style the table
        style_cmds = [
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), self.table_header_bg),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TEXTCOLOR', (0, 1), (-1, -1), black),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, self.table_row_alt]),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, self.accent_color),
            
            # Alignment
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),  # Price right-aligned
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),  # Rating centered
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        
        table.setStyle(TableStyle(style_cmds))
        elements.append(table)
        
        return elements
    
    def _estimate_page_count(self, books: List[Dict]) -> int:
        """Estimate page count based on book count."""
        # Rough estimate: ~35 books per page + cover + summary
        books_per_page = 35
        content_pages = max(1, (len(books) + books_per_page - 1) // books_per_page)
        return content_pages + 2  # +2 for cover and summary
    
    def _add_page_number(self, canvas, doc):
        """Add page numbers and footer to each page."""
        canvas.saveState()
        
        # Footer line
        canvas.setStrokeColor(HexColor("#dddddd"))
        canvas.setLineWidth(0.5)
        canvas.line(20*mm, 15*mm, A4[0] - 20*mm, 15*mm)
        
        # Page number
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(HexColor("#999999"))
        canvas.drawCentredString(A4[0] / 2, 10*mm, text)
        
        # Footer text
        footer_text = "FlyRank Report Generator | Confidential"
        canvas.drawCentredString(A4[0] / 2, 5*mm, footer_text)
        
        canvas.restoreState()


def generate_book_catalog_pdf(
    books: List[Dict],
    output_dir: str,
    base_url: str,
    title: str = "Book Catalog Report",
    filters: Dict = None,
    stats: Dict = None
) -> Dict[str, Any]:
    """Convenience function to generate a book catalog PDF."""
    generator = PDFReportGenerator(output_dir, base_url)
    return generator.generate_book_catalog_report(books, title, filters, stats)