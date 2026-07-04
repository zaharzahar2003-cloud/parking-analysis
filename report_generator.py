from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf_report(history_rows):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    pdf_path = f'static/report_{timestamp}.pdf'

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "📊 Отчёт по анализу загруженности парковки ТЦ")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Дата генерации: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    y -= 20
    c.drawString(50, y, f"Всего записей: {len(history_rows)}")
    y -= 30

    if history_rows:
        total_vehicles = sum(row[2] for row in history_rows)
        avg_vehicles = total_vehicles / len(history_rows) if history_rows else 0
        c.drawString(50, y, f"Всего автомобилей обнаружено: {total_vehicles}")
        y -= 20
        c.drawString(50, y, f"Средняя загруженность: {avg_vehicles:.1f} авто/кадр")
        y -= 30

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Время")
    c.drawString(200, y, "Файл")
    c.drawString(350, y, "Автомобилей")
    y -= 15

    c.setFont("Helvetica", 9)
    for row in history_rows[:50]:
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 9)
        timestamp_str = row[0][:16] if row[0] else '—'
        c.drawString(50, y, timestamp_str)
        c.drawString(200, y, (row[1] or '—')[:20])
        c.drawString(350, y, str(row[2]))
        y -= 14

    c.save()
    return pdf_path