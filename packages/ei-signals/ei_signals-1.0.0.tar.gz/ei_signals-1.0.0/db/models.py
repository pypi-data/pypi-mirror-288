from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models import JSONField
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid
from django.contrib.auth.models import Permission
import random
import string

# Create your models here.


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

class BillingAccount(models.Model):
    id = models.CharField(primary_key = True,default = uuid.uuid4, max_length=255)
    name = models.CharField(max_length=255, default='Team')
    user = models.OneToOneField(get_user_model(), models.CASCADE, related_name='billing') # could not be changed
    status = models.TextField(default='trial') # free_trial, active, pending, suspended
    max_workspaces = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    tz = models.CharField(max_length=255)
    cts = models.DateTimeField(default=timezone.now)
    realtime = models.BooleanField(default=False)

class Workspace(models.Model):
    workspace_id = models.CharField(primary_key = True,default = uuid.uuid4, max_length=255)
    billing_account = models.ForeignKey(BillingAccount, models.CASCADE)
    name = models.CharField(max_length=50)
    colour = models.CharField(max_length=255, default='')
    active = models.BooleanField(default=True)
    tz = models.CharField(max_length=255)
    cts = models.DateTimeField(default=timezone.now)
    objects = ActiveManager()

    class Meta:
        permissions = (
                ('add_user', 'Add User'),
                ('create_events', 'Create Events'),
                ('add_datasources', 'Add DataSources'),
                ('view_data', 'View Data'),
            )
        unique_together = [
            ('billing_account','name')
            ]
        
class Group(models.Model):
    group_id = models.CharField(primary_key = True,default = uuid.uuid4, max_length=255)
    workspace = models.ForeignKey(Workspace, models.CASCADE, related_name='group')
    name = models.CharField(max_length=100)
    normalized_name = models.CharField(max_length=100, null=True)
    auto_generated = models.BooleanField(default=False)
    blended = models.BooleanField(default=True)

    class Meta:
        # unique_together = ('workspace','name')
        unique_together = ('workspace','normalized_name')
# class SignupReferrer(models.Model):
#     user = models.ForeignKey(get_user_model(), models.CASCADE, related_name='referrer', primary_key=True)
#     referrer = models.TextField(max_length=255)

class SignupActivity(models.Model):
    id = models.CharField(primary_key = True,default = uuid.uuid4, max_length=255)
    user = models.ForeignKey(get_user_model(), models.CASCADE, related_name='signup_activity')
    cts = models.DateTimeField(default=timezone.now)


class UserLoginType(models.Model):
    id = models.CharField(primary_key = True,default = uuid.uuid4, max_length=255)
    user = models.ForeignKey(get_user_model(), models.CASCADE, related_name='login_type')
    login_type = models.CharField(max_length=255)
    cts = models.DateTimeField(default=timezone.now)

class GoogleLoginState(models.Model):
    state = models.CharField(max_length=255, primary_key=True)
    ui_redirect = models.TextField(max_length=255)
    cts = models.DateTimeField(default=timezone.now)

# class UserLogGA(models.Model):
#     id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=255)
#     user = models.CharField(max_length=255)
#     ga_id = models.CharField(max_length=255)

#     class Meta:
#         unique_together = ('user','ga_id')


class TeamMember(models.Model):
    team = models.ForeignKey(BillingAccount, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), models.CASCADE)

class WorkspaceEvent(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=255)
    cts = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=255)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    sync_config = models.CharField(max_length=255, default='ntd656rfuyjgbh')
    active = models.BooleanField(default=True)
    destination = models.CharField(max_length=255, default='kg6787yy5s54w3wrthg')
    config = models.JSONField()
    segment = models.CharField(max_length=255, default='stx5dcy6ug78yg')
    class Meta:
        unique_together = ('name','workspace')

class WorkspaceEventLog(models.Model):
    event = models.ForeignKey(WorkspaceEvent, on_delete=models.CASCADE)
    ts = models.DateTimeField(default=timezone.now)
    count = models.IntegerField()


class AllPlatform(models.Model):
    platform_id = models.CharField(default = uuid.uuid4, max_length=255, primary_key = True)
    name = models.CharField(max_length=255, unique=True)
    icon = models.CharField(max_length=255)
    blend = models.BooleanField(default=False)
    overall = models.BooleanField(default=False)
    column_json = models.CharField(max_length=255)
    app_only = models.BooleanField()
    app2_only = models.BooleanField()

class Platform(models.Model):
    platform = models.ForeignKey(AllPlatform,primary_key = True, on_delete=models.CASCADE)
    api = models.CharField(max_length=255, unique=True)
    account_list = models.BooleanField(default=False)

class PlatformOauth2(models.Model):
    platform = models.ForeignKey(Platform,primary_key = True, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)
    redirect_uri = models.CharField(max_length=150)
    options = models.JSONField(default=dict,null=True)


class Credentials(models.Model):
    credentials_id = models.CharField(primary_key = True,default = uuid.uuid4, max_length=255)
    credentials = models.JSONField(default=dict)

class PlatformOauth2Email(models.Model):
    credentials = models.ForeignKey(Credentials, on_delete=models.CASCADE, primary_key=True, related_name='oauth_user')
    email = models.EmailField()
    platform = models.ForeignKey(Platform, on_delete = models.CASCADE)
    active = models.BooleanField(default=True) # set active false in case of password reset by email, delete entry
    class Meta:
        unique_together = ('platform','email')

class PlatformUserOauth(models.Model):
    platform_user_oauth_id = models.CharField(primary_key = True,default = uuid.uuid4, max_length=255)
    credentials = models.ForeignKey(PlatformOauth2Email, on_delete=models.CASCADE, related_name='end_user')
    platform = models.ForeignKey(Platform, on_delete = models.CASCADE)
    user = models.ForeignKey(get_user_model(), models.CASCADE, related_name = 'oauth_user')
    class Meta:
        unique_together = ('platform','user')


class PlatformJson(models.Model):
    credentials = models.ForeignKey(Credentials, on_delete=models.CASCADE, primary_key=True)
    platform = models.ForeignKey(Platform, on_delete = models.CASCADE)
    workspace = models.ForeignKey(Workspace, models.CASCADE, related_name='no_oauth_credentials')

class PlatformAccount(models.Model):
    platformaccount_id = models.CharField(primary_key = True,default = uuid.uuid4, max_length=255)
    platform = models.ForeignKey(Platform, on_delete = models.CASCADE)
    workspace = models.ForeignKey(Workspace, models.CASCADE, related_name='account')
    # credentials = models.ForeignKey(Credentials, on_delete=models.SET_NULL, null=True)
    account_id = models.CharField(max_length=100) # act_12345, name, crm_table1
    user = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, related_name = 'platform_account')
    name = models.CharField(max_length=100) # Fb, table1 #automatically update daily based on API calls
    # custom_columns = models.JSONField(default=list)
    active = models.BooleanField(default=True)
    last_fetched = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('workspace','platform','account_id')


def expire_time():
    return timezone.now()+timezone.timedelta(seconds=300)
class AuthToken(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=255)
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    expire = models.DateTimeField(default=expire_time())

