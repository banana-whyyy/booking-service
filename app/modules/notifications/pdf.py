import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_ticket_pdf(booking_id: int, user_email: str, room_name: str) -> bytes:
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, 750, "Бронирование подтверждено!")

    p.setFont("Helvetica", 12)
    p.drawString(100, 710, f"ID Брони: #{booking_id}")
    p.drawString(100, 690, f"Пользователь: {user_email}")
    p.drawString(100, 670, f"Переговорка: {room_name}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer.getvalue()