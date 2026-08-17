import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_ticket_pdf(
    booking_id: int, 
    username: str, 
    room_name: str,
    time_start: str | datetime,
    time_end: str | datetime
) -> bytes:
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    if isinstance(time_start, str):
        time_start = datetime.fromisoformat(time_start)
    if isinstance(time_end, str):
        time_end = datetime.fromisoformat(time_end)

    formatted_date = time_start.strftime("%Y-%m-%d")
    formatted_time = f"{time_start.strftime('%H:%M')} - {time_end.strftime('%H:%M')}"

    p.setFont("Helvetica-Bold", 18)
    p.setFillColor(colors.HexColor("#2C3E50"))
    p.drawString(100, 750, "Booking Confirmed!")

    p.setStrokeColor(colors.HexColor("#BDC3C7"))
    p.setLineWidth(1)
    p.line(100, 735, 500, 735)

    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    
    p.drawString(100, 700, f"Booking ID: #{booking_id}")
    p.drawString(100, 680, f"User: {username}")
    p.drawString(100, 660, f"Room: {room_name}")
    p.drawString(100, 640, f"Date: {formatted_date}")
    p.drawString(100, 620, f"Time: {formatted_time}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer.getvalue()