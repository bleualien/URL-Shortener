from django.db import models
from django.contrib.auth.models import User
from .utils import generate_short_key

class ShortURL(models.Model):
    original_url = models.URLField(max_length=500)
    short_key = models.CharField(max_length=15, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  
    clicks = models.IntegerField(default=0)             

    def save(self, *args, **kwargs):
        if not self.short_key:
            # We save first to get a unique ID from the DB
            super().save(*args, **kwargs)
            self.short_key = generate_short_key(self.id)
            # Update only the key to avoid recursion
            ShortURL.objects.filter(id=self.id).update(short_key=self.short_key)
        else:
            super().save(*args, **kwargs)