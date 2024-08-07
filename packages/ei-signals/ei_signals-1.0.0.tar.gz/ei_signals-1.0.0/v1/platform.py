import db
from . import errors

def get_api(platform_id):
    return db.read_single_row_by_pk('Platform', platform_id, ['api'])['api']

def get(fields=None,**platform_filters):
    if not fields:
        fields = ['platform_id','name']
    return db.read('AllPlatform', fields, platform_filters)

# def get_columns(platform_filters, column_filters):
#     from . import _column
#     platforms = get(**platform_filters)
#     columns = []
#     for p in platforms:
#         columns += _column.list_platform(p['platform_id'], column_filters)
#     return columns

# def get_default_channel_mapping(platform_id):
#     mapping_rows = db.read(
#         'ChannelFieldDefaultMap',[
#             'mapped_platform_id',
#             'value',
#             ],
#         {
#             'platform_id':platform_id,
#             })
#     platforms = get()
#     platform_name = {k['platform_id']:k['name'] for k in platforms}
#     return {k['value']: platform_name[k['mapped_platform_id']] for k in mapping_rows}

# def is_advertising(platform_id):
#     try:
#         db.read_single_row('PlatformAdvertising',['platform_id'],{'platform_id':'platform_id'})
#         return True
#     except db.errors.NoRowFound:
#         return False

# def is_analytic(platform_id):
#     try:
#         db.read_single_row('PlatformAnalytic',['platform_id'],{'platform_id':platform_id})
#         return True
#     except db.errors.NoRowFound:
#         return False

def is_oauth2(platform_id):
    try:
        db.read_single_row('PlatformOauth2',['platform_id'],{'platform_id':platform_id})
        return True
    except db.errors.NoRowFound:
        return False
    
def parse_no_oauth_data(platform_id, no_oauth_data):
    fields = db.read('PlatformNoOauthField',['field_name','account_id', 'account_name','credentials'],{'platform_id':platform_id})
    cred_fields = [k['field_name'] for k in fields if k['credentials']]
    account_id = [k['field_name'] for k in fields if k['account_id']][0]
    account_name = [k['field_name'] for k in fields if k['account_name']][0]
    credentials = {k:no_oauth_data[k] for k in cred_fields}
    account = (no_oauth_data[account_id],no_oauth_data[account_name])
    return {'credentials':credentials, 'account':account}

def get_authorization_url(user_id, platform_id, ui_redirect):
    import uuid
    state = uuid.uuid4()
    auth_params = db.read_single_row('PlatformOauth2',['client_id','client_secret','redirect_uri','options'], {'platform_id':platform_id})
    import fetl.v1
    api = get_api(platform_id)
    authorization_url = fetl.v1.get_authorization_url(api, state, auth_params)
    state = fetl.v1.get_state_from_authorization_url(api, authorization_url,state)
    return authorization_url, state


def _verify_state(params, user_id, platform_id, session_state):
    import fetl.v1
    print('verify state')
    api = get_api(platform_id)
    state = fetl.v1.get_state(api, params)
    state_verified = False
    if not state == session_state:
        raise errors.InvalidRequest()

def _generate_credentials(params, platform_id, user_id):
    auth_params = db.read_single_row_by_pk('PlatformOauth2',platform_id,['client_id','client_secret','options','redirect_uri'])
    api = get_api(platform_id)
    import fetl.v1
    new_credentials = fetl.v1.generate_credentials(api, params, auth_params)
    print(new_credentials, user_id)
    if 'error' in new_credentials:
        raise errors.InvalidRequest()
    from . import credentials
    credentials.update(new_credentials, platform_id, None, user_id, True, None)
    return {'success': True}
    
def generate_credentials(params, user_id, platform_id, session_state):
    _verify_state(params, user_id, platform_id, session_state)
    response = _generate_credentials(params, platform_id, user_id)

def get_accounts(platform_id, workspace_id, user_id):
    from . import credentials
    p_details = db.read_single_row_by_pk('Platform',platform_id,['account_list','api'])
    if not p_details['account_list']:
        return []
    try:
        cred_id = credentials.get_id(platform_id ,workspace_id,user_id, is_oauth2(platform_id), None)['credentials_id']
    except db.errors.NoRowFound:
        return []
    import fetl.v1
    creds = credentials.get_by_id(cred_id)['credentials']
    accounts = fetl.v1.get_accounts(p_details['api'], creds)
    return accounts

# def get_overall_platform():
#     return db.read_single_row('PlatformOverall',['platform_id'])['platform_id']

# def is_overall(platform_id):
#     return platform_id == get_overall_platform()

# def is_blend(platform_id):
#     pass

# def get_email(platform_id, user_id):
#     if not is_oauth2(platform_id):
#         return ''
#     if is_oauth2(platform_id):
#         from . import credentials
#         credentials_id = credentials._get_oauth2_credentials(platform_id, user_id)['credentials_id']
#         email = db.read_single_row('PlatformOauth2Email', ['email'], {'credentials_id': credentials_id})["email"]
#         return email
