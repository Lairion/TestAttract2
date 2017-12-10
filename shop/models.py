from django.db import models
from datetime import date
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
# from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum
# Create your models here.

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        if self.first_name and self.last_name:
            return "%s %s." % (self.first_name, self.last_name[0].upper())
        return self.email


class SaleOrder(models.Model):
    """
    Description: Model Description
    """
    customer = models.ForeignKey(User, related_name="sale_order")
    who_confirmed = models.ForeignKey(
        User, related_name="who_confirmed", null=True, blank=True)
    date_order_confirm = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True)
    date_reserve = models.DateField(auto_now=False,
                                    auto_now_add=True,
                                    null=True,
                                    blank=True)

    confirmed = models.BooleanField(default=False)

    slug = models.SlugField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify("sale number")
        self.slug += "-" + str(self.id)
        super(SaleOrder, self).save(*args, **kwargs)

    def total(self):
        total = self.list_product.all().aggregate(Sum('amount_total'))
        return total["amount_total__sum"]

    def sale_confirm(self, u_admin):
        self.date_order_confirm = date.today()
        self.confirmed = True
        self.who_confirmed = u_admin
        self.save()

    def get_url(self):
        return reverse("shop:sale", kwargs={"slug": self.slug})

    def __str__(self):
        if self.confirmed:
            return str(self.id)
        else:
            return "New sale"

    class Meta:
        pass
