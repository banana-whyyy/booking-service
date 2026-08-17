from app.celery_config import celery_app 
from .pdf import generate_ticket_pdf

@celery_app.task(bind=True, max_retries=3)
def process_booking_notification(self, payload: dict):
    pdf_bytes = generate_ticket_pdf(
        booking_id=payload["booking_id"],
        username=payload["username"],
        room_name=payload["room_name"],
        time_start=payload["time_start"],
        time_end=payload["time_end"]
    )

    # В реальном проекте отправляется Email:
    # send_email(
    #     to=payload["user_email"], 
    #     subject="Ваш билет забронирован"
    # )

    # Для тестов просто выводим размер сгенерирована файла в лог
    pdf_size_kb = len(pdf_bytes) / 1024
    
    print(f"[CELERY WORKER] Ticket generated for booking #{payload['booking_id']} ({pdf_size_kb:.2f} KB)")
    
    return f"Ticket generated successfully ({pdf_size_kb:.2f} KB)"

