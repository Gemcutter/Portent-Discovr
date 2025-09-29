from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime


def ExportToPDF(report_data, filename="Discovr_Report.pdf"):
  
    try:
        # Create PDF canvas
        pdf = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        # Title
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, height - 50, "Discovr Asset Report")

        # Timestamp
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, height - 70, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Content
        y_position = height - 100
        pdf.setFont("Helvetica", 12)
        for line in report_data:
            pdf.drawString(50, y_position, line)
            y_position -= 20
            if y_position < 50:  # Start a new page if space runs out
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y_position = height - 50

        # Save PDF
        pdf.save()
        print(f"Report exported successfully: {filename}")

    except Exception as e:
        print(f"Error exporting report: {e}")

    