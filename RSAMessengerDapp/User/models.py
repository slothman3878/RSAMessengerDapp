from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from eth_account import Account

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("User must have a username")

        acct = Account.create()        

        user = self.model(
            username = username,
            address = acct.address,
            eth_key = acct.key.hex(),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()

    username = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=42, unique=True, default=None)
    eth_key = models.CharField(max_length=66, unique=True, default=None)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return self.address
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

# While currently the Key model does use a ForeignKey field, for now we are assuming there is one unique key for each user.
class Key(models.Model):
    public_key = models.TextField()
    private_key = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_registered = models.BooleanField(default=False)