# sales/tasks.py
from celery import shared_task
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.files import File
import os

@shared_task
def generate_invoice_pdf(invoice_id):
    from .models import Invoice
    invoice = Invoice.objects.get(id=invoice_id)
    order = invoice.order

    pdf_path = f'invoices/invoice_{invoice_id}.pdf'
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, f"Invoice for Order {order.id}")
    c.drawString(100, 730, f"Customer: {order.customer.username}")
    c.drawString(100, 710, f"Total: ${invoice.total_amount}")
    c.drawString(100, 690, f"Due Date: {invoice.due_date}")
    c.showPage()
    c.save()

    with open(pdf_path, 'rb') as pdf_file:
        invoice.pdf_file.save(f'invoice_{invoice_id}.pdf', File(pdf_file))
    os.remove(pdf_path)

# sales/views.py
from .tasks import generate_invoice_pdf

class InvoiceViewSet(viewsets.ModelViewSet):
    # ... existing code ...
    def perform_create(self, serializer):
        invoice = serializer.save()
        generate_invoice_pdf.delay(invoice.id)