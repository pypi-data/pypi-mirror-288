from django.conf import settings
import logging

import db
from . import errors

logger = logging.getLogger(__name__)

def login_user(token_type, token,request):
    from django.contrib.auth import authenticate
    from django.contrib.auth import login as auth_login
    from . import shopify_login
    user = authenticate(token_type, token=token)
    if user is not None:
        auth_login(request, user)
    db.create('SignupActivity',{'user':user})
    # print(request.session.session_key)
    # referrer = request.session.get('referrer','')
    # try:
    #     db.create('SignupReferrer',{'user':user, 'referrer': referrer})
    # except db.errors.DuplicateEntry:
    #     pass
    # try:
    #     create_user_entry_log(user.id, request.COOKIES['_ga'])
    # except KeyError:
    #     pass
    # logger.debug("Logged in {}".format(str(user)))
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        db.create('UserLoginType',{'user_id':user.id, 'login_type': login_type})
        # if login_type.startswith('aisensy_'):
        #     from . import workspace
        #     workspace.create_aisensy_workspace(user.id)
    return user
    
def get_redirect_uri(host):
    # return '{}/api/v3/google_login_redirect/'.format(host)
    try:
        if settings.DEBUG:
            return 'http://127.0.0.1:8000/api/v1/google_login_redirect/'
        if not settings.DEBUG:
            return '{}/api/v1/google_login_redirect/'.format(host)
    except Exception as e:
        logger.error(e, exc_info=True)
        return

# http://localhost:8000/v3/google_login/?r=s
def get_authorization_url(ui_redirect, host):
    import uuid
    state = uuid.uuid4()
    import urllib.parse
    from urllib.parse import urlencode
    auth_url = 'https://accounts.google.com/o/oauth2/auth?'
    scopes = 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid'
    m = {
    'client_id' : settings.GOOGLEOPENID_CLIENT,
    'scope': scopes,
    'state': state,
    'redirect_uri' : get_redirect_uri(host),
    'prompt' : 'consent',
    'access_type':'offline',
    'response_type':'code'
    }
    query = urlencode(m)
    # urllib.parse.urlencode(query, doseq=False, safe='', encoding=None, errors=None, quote_via=quote_plus)
    authorization_url = auth_url + query
    db.create(
        'GoogleLoginState',{
            'state': state,
            'ui_redirect': ui_redirect,
            }
        )
    return authorization_url, state

def get_user_id(params,request):
    try:
        import requests
        state = params['state'][0]
        state_data = db.read('GoogleLoginState',['ui_redirect','cts'],{'state':state})[0]
        import datetime
        if datetime.datetime.now(datetime.timezone.utc) > state_data['cts']+datetime.timedelta(seconds=600):
            raise errors.InvalidRequest
        host = request.build_absolute_uri('/')[:-1]
        data = {
            'client_id' : settings.GOOGLEOPENID_CLIENT,
            'redirect_uri': get_redirect_uri(host),
            'code': params['code'],
            'client_secret': settings.GOOGLEOPENID_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            }
        token_url = 'https://oauth2.googleapis.com/token'
        r = requests.post(token_url, data=data)
        credentials = r.json()
        id_token = credentials['id_token']
        login_user('googleopenid',id_token,request)
        return state_data['ui_redirect']
    except Exception as e:
        logger.error(e, exc_info=True)
        return

# def create_user_entry_log(user_id, ga_id):
#     try:
#         db.create('UserLogGA', {'user':user_id,'ga_id':ga_id})
#     except db.errors.DuplicateEntry:
#         pass
#     return 