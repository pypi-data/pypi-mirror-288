from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.http import JsonResponse
from guardian.decorators import permission_required_or_403
from login_required import login_not_required
from django.views.decorators.http import require_http_methods
from . import errors
import db


# Create your views here.


# @login_not_required
# @require_http_methods(["POST"])
# def login(request):
#     request.session['referrer'] = request.GET.get('s','')
#     try:
#         from . import google_login
#         token_type = request.POST['token_type']
#         token = request.POST['token']
#         user = google_login.login_user(token_type, token,request)
#         return JsonResponse({})
#     except Exception as e:
#         # logger.error(e, exc_info=True)
#         raise Exception('Login Error')

@login_not_required
@require_http_methods([ "GET"])
def google_login(request):
    request.session['referrer'] = request.GET.get('s','')
    redirect_uri = request.GET.get('r')
    host = request.build_absolute_uri('/')[:-1]
    from . import google_login
    authorization_url, state = google_login.get_authorization_url(redirect_uri, host)
    # print(authorization_url, host)
    return HttpResponseRedirect(authorization_url)

@login_not_required
@require_http_methods([ "GET"])
def google_login_redirect(request):
    from . import google_login
    try:
        redirect_uri = google_login.get_user_id(dict(request.GET),request)
        return HttpResponseRedirect(redirect_uri)
    except errors.InvalidRequest:
        return Http404()
    
@require_http_methods(["POST"])
def logout(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return JsonResponse({'success':True, 'data':{}})    

@require_http_methods(["POST"])
def userinfo(request):
    from . import users
    data = users.get(request.user.id)
    response = JsonResponse({'success':True, 'data':data})
    response.set_cookie("_ei_sd",request.get_host(),domain=".easyinsights.ai")
    return response

@require_http_methods(['POST'])
def shopify_userinfo(request):
    id_token = request.GET.get('id_token')
    shop = request.GET.get('shop')
    from . import shopify_login
    data = shopify_login.get_user_info(request, id_token, shop)
    if data is None:
        from django.http import HttpResponseServerError
        return HttpResponseServerError()
    return JsonResponse({'success':True, 'data':data})
    
@require_http_methods(['GET'])
def get_event_logs(request, workspace_id):
    from . import event
    response = event.event_logs(workspace_id)
    return JsonResponse(response)

@require_http_methods(['GET'])
def generate_auth_token(request):
    import db
    token = db.create('AuthToken',{'user_id':request.user.id})
    print(token, request.user.id)
    return JsonResponse({'success':True, 'token':token})

@login_not_required
@require_http_methods([ "GET"])
def oauth2_initiate(request, platform_id):
    from . import platform
    redirect_uri = request.GET.get('r')
    token = request.GET.get('token') #for shopify auth initiation
    print(token)
    user = request.user
    if token:
        from django.contrib.auth import login
        from django.utils import timezone
        import db
        data = db.read_single_row('AuthToken',['user','expire'],{'id':token})
        print(type(data['expire']))
        if data['expire']< timezone.now():
            return JsonResponse({})
        user = data['user']
        print(user)
        login(request, user, 'user.auth.AuthBackend')
    authorization_url, state = platform.get_authorization_url(user.id, platform_id, redirect_uri)
    request.session['oauth2_state'] = {'state': str(state), 'ui_redirect': redirect_uri}
    response = HttpResponseRedirect(authorization_url)
    return response

@login_not_required
@require_http_methods(["GET"])
def oauth2_callback_redirect(request, platform_id):
    print('callback started')
    params = request.GET.dict()
    print(request.user)
    oauth2_state = request.session.pop('oauth2_state')
    ui_redirect = oauth2_state['ui_redirect']
    print(oauth2_state, ui_redirect)
    if 'error' in params:
        return HttpResponseRedirect(ui_redirect)
    from . import platform
    try:
        platform.generate_credentials(params, request.user.id, platform_id, oauth2_state['state'])
    except errors.InvalidRequest:

        return Http404()
    return HttpResponseRedirect(ui_redirect)

@require_http_methods([ "GET"])
def authorized_platforms(request):
    from . import users
    data = users.get_authorized_platforms(request.user.id)
    return JsonResponse({'success':True, 'data':data})
    
@permission_required_or_403('db.add_datasources', (db.models.Workspace, 'workspace_id', 'workspace_id'))
@require_http_methods([ "POST"])
def add_workspace_account(request, workspace_id):
    # check
    from . import workspace
    import json
    body = json.loads(request.body)
    platform_id, no_oauth_data, account_id, name = body['platform_id'], body['no_oauth_data'], body['account_id'], body['account_name']
    data = workspace.add_account(workspace_id, platform_id, no_oauth_data, account_id, name, request.user.id)
    # if not reverse_etl.segment_exists(workspace_id,platform_id):
    #     reverse_etl.create_default_segments(workspace_id, platform_id)
    return JsonResponse({'success':True,'data':data})



@permission_required_or_403('db.view_data', (db.models.Workspace, 'workspace_id', 'workspace_id'))
@require_http_methods([ "GET"])
def list_workspace_accounts(request, workspace_id):
    from . import workspace
    fields = [
            'platformaccount_id',
            'name',
            'platform_id',
            ]
    data = workspace.get_accounts(fields,{'workspace_id': workspace_id})
    return JsonResponse({'success':True, 'data':data})


@permission_required_or_403('db.add_datasources', (db.models.Workspace, 'workspace_id', 'workspace_id'))
@require_http_methods([ "POST"])
def delete_workspace_accounts(request, workspace_id):
    from . import workspace
    import json
    body = json.loads(request.body)
    data = workspace.delete_accounts(workspace_id, body['accounts'])
    return JsonResponse({'success':True, 'data':data})


@permission_required_or_403('db.view_data', (db.models.Workspace, 'workspace_id', 'workspace_id'))
@require_http_methods([ "GET"])
def list_platform_accounts(request, workspace_id):
    from . import platform
    platform_id = request.GET.get("p")
    data = platform.get_accounts(platform_id, workspace_id, request.user.id)
    # email = platform.get_email(platform_id, request.user.id)
    return JsonResponse({'success':True, 'data':data})


@login_not_required
@require_http_methods('POST')
def otp_login(request):
    from . import otp_login
    import json
    data = json.loads(request.body)
    response = otp_login.send_email(data['email'],request)
    return JsonResponse(response)

@login_not_required
@require_http_methods('POST')
def verify_otp(request):
    from . import otp_login
    import json
    data = json.loads(request.body)
    response  = otp_login.verify(data, request)
    return JsonResponse(response)
