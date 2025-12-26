from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

# Signal handler to automatically create a UserProfile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a UserProfile instance when a new User is saved.
    This ensures every user has an associated profile from the start.
    
    Args:
        sender: The User model class
        instance: The actual User instance being saved
        created: Boolean indicating if this is a new User
    """
    if created:
        UserProfile.objects.create(user=instance)

# Signal handler to save the UserProfile when the User is updated
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Saves the associated UserProfile when a User instance is saved.
    If the profile doesn't exist, it creates one to ensure data consistency.
    
    Args:
        sender: The User model class
        instance: The actual User instance being saved
    """
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance) 