from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invoice
from .tasks import generate_invoice_pdf  # Create Celery task

@receiver(post_save, sender=Invoice)
def create_invoice_pdf(sender, instance, created, **kwargs):
    if created and not instance.pdf_file:
        generate_invoice_pdf.delay(instance.id)