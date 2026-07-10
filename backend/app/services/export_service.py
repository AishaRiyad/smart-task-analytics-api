import csv
from io import BytesIO, StringIO
from typing import Iterable

from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.db.models import Task


def export_tasks_to_csv(tasks: Iterable[Task]) -> bytes:
    text_buffer = StringIO()

    writer = csv.writer(text_buffer)

    writer.writerow([
        "ID",
        "Title",
        "Description",
        "Completed",
        "Completion Time",
        "Created At",
        "Updated At",
    ])

    for task in tasks:
        writer.writerow([
            task.id,
            task.title,
            task.description or "",
            task.completed,
            task.completion_time or "",
            task.created_at.isoformat() if task.created_at else "",
            task.updated_at.isoformat() if task.updated_at else "",
        ])

    return text_buffer.getvalue().encode("utf-8-sig")


def export_tasks_to_excel(tasks: Iterable[Task]) -> bytes:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Tasks"

    worksheet.append([
        "ID",
        "Title",
        "Description",
        "Completed",
        "Completion Time",
        "Created At",
        "Updated At",
    ])

    for task in tasks:
        worksheet.append([
            task.id,
            task.title,
            task.description or "",
            task.completed,
            task.completion_time,
            task.created_at.isoformat() if task.created_at else "",
            task.updated_at.isoformat() if task.updated_at else "",
        ])

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    return output.getvalue()


def export_tasks_to_pdf(tasks: Iterable[Task]) -> bytes:
    output = BytesIO()

    pdf = canvas.Canvas(output, pagesize=A4)
    page_width, page_height = A4

    y_position = page_height - 50

    pdf.setTitle("Task Report")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y_position, "Task Report")

    y_position -= 35
    pdf.setFont("Helvetica", 10)

    for task in tasks:
        if y_position < 80:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y_position = page_height - 50

        title = task.title[:60]
        status = "Completed" if task.completed else "Pending"

        pdf.drawString(50, y_position, f"ID: {task.id}")
        y_position -= 15

        pdf.drawString(50, y_position, f"Title: {title}")
        y_position -= 15

        pdf.drawString(50, y_position, f"Status: {status}")
        y_position -= 15

        pdf.drawString(
            50,
            y_position,
            f"Completion Time: {task.completion_time or 'N/A'}"
        )
        y_position -= 25

    pdf.save()
    output.seek(0)

    return output.getvalue()