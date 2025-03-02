from celery import shared_task
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

@shared_task
def create_user_profile(user_id):
    """Create a UserProfile for a newly created user."""
    user = User.objects.get(id=user_id)
    UserProfile.objects.get_or_create(user=user)

@shared_task
def save_user_profile(user_id):
    """Save the UserProfile associated with a user."""
    user = User.objects.get(id=user_id)
    if hasattr(user, 'profile'):
        user.profile.save()