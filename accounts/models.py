from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class UserManager(BaseUserManager):
    # Define a model manager for User model with no username field

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        # Create and save a User with the given email and password
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # Create and save a regular User with the given email and password
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        # Create and save a SuperUser with the given email and password
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    USERNAME_FIELD = 'email'
    # changes email to unique and blank to false
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
     # removes email from REQUIRED_FIELDS
    REQUIRED_FIELDS = []


    gender = models.CharField(max_length=1, 
                              null=True, blank=True,
                              choices=[('1', 'M.'), ('2', 'Mme'), ('3', 'Autre')])
    birthdate = models.DateField(null=True, blank=True)

    objects = UserManager()

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'auth_user'


class UserPaymentProfile(models.Model):
    CHOICES = (
        ('S', 'Stripe'),
        ('P', 'Paypal'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    
    service = models.CharField(max_length=1, 
                              null=True, blank=True,
                              default='S',
                              choices=CHOICES)
    # STRIPE / PAYPAL customer id
    customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    class Meta:
        # NOTE: unique_together does not work with sqlite
        verbose_name_plural = 'User__PaymentProfile'
        unique_together = (
            ('user', 'service',),
        )

    def __str__(self):
        return self.user.username