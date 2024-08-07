from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.contrib import auth
from django.core.exceptions import PermissionDenied

import uuid

def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions
def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False

class BaseUserManager(models.Manager):
    # use_in_migrations = True

    def _create_user(self, **kwargs):
        """
        Create and save a user with the given name, email, and email_type.
        """
        if not kwargs['email']:
            raise ValueError('The email must be set')
        email = self.normalize_email(kwargs.pop('email'))
        user, created = self.model.objects.update_or_create(
            email=email,
            defaults = kwargs
        )        
        # email = self.normalize_email(email)
        # name = self.model.normalize_username(name)
        return user

    def create_user(self, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_active', True)
        # extra_fields.setdefault('is_superuser', False)
        return self._create_user(**kwargs)

    # def create_superuser(self, username, email, password, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Superuser must have is_staff=True.')
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')

    #     return self._create_user(username, email, password, **extra_fields)

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email

    # def make_random_password(self, length=10,
    #                          allowed_chars='abcdefghjkmnpqrstuvwxyz'
    #                                        'ABCDEFGHJKLMNPQRSTUVWXYZ'
    #                                        '23456789'):
    #     """
    #     Generate a random password with the given length and given
    #     allowed_chars. The default value of allowed_chars does not have "I" or
    #     "O" or letters and digits that look similar -- just to avoid confusion.
    #     """
    #     return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class User(models.Model):
    id = models.CharField(primary_key = True,default = uuid.uuid4, max_length=255)
    name = models.CharField(max_length=254)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=12)#phone validator
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    shopify_user = models.BooleanField(default=False)
    # ui_options = models.JSONField(default = get_user_ui_option)
    icon = models.TextField(max_length=255, default='', null=True)
    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'email'
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    cts = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )

    objects = BaseUserManager()
    def __str__(self):
        return "{} ({})".format(self.name,self.email)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use simlar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)
    
    def set_unusable_password(self):
        self.is_staff=False
        self.is_active=True
        return False
    
    def get_username(self):
        return self.name

