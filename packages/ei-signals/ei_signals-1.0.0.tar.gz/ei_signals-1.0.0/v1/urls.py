from django.urls import path
from v1 import views

app_name = 'v1'

urlpatterns = [
    # path('login/',views.login, name= 'login'),
    path('logout/',views.logout, name='logout'),
    path('me/', views.userinfo , name = 'userinfo'),
    path('shopify/me/', views.shopify_userinfo, name='shopify_userinfo'),
    path('google_login/', views.google_login, name = 'google_login'),
    path('google_login_redirect/', views.google_login_redirect, name = 'google_login_redirect'),
    path('workspace/<workspace_id>/get_event_logs/', views.get_event_logs, name='get_event_logs'),
    path('get_auth_token/',views.generate_auth_token, name='generate_auth_token'),
    path('authorize/<platform_id>/', views.oauth2_initiate, name = 'oauth2_initiate'),
    path('oauth2_callback_redirect/<platform_id>/', views.oauth2_callback_redirect, name = 'oauth2_callback_redirect'),
    path('authorized_platforms/', views.authorized_platforms, name = 'authorized_platforms'),
    path('workspace/<workspace_id>/add_account/', views.add_workspace_account, name = 'add_account'),
    path('workspace/<workspace_id>/list_accounts/', views.list_workspace_accounts, name = 'list_workspace_accounts'),
    path('workspace/<workspace_id>/delete_accounts/', views.delete_workspace_accounts, name = 'delete_workspace_accounts'),
    path('workspace/<workspace_id>/list_platform_accounts/', views.list_platform_accounts, name = 'list_platform_accounts'),
    path('otp_login/', views.otp_login, name="otp_login"),
    path('verify_otp/', views.verify_otp, name='verify_otp'),

]