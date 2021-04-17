from django.db import models
from User.models import User

# Create your models here.
# While currently the Key model does use a ForeignKey field, for now we are assuming there is one unique key for each user.
class Key(models.Model):
    public_key = models.TextField()
    private_key = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_main_key = models.BooleanField(default=False)