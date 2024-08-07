import db


def _get_oauth2_credentials(platform_id, user_id):
    return db.read_single_row('PlatformUserOauth',['credentials_id'],{'platform_id':platform_id,'user_id':user_id})

def _get_noauth_credentials(platform_id, workspace_id, account_id):
    creds = db.read_single_row('PlatformJson',['credentials_id'],{'platform_id':platform_id,'workspace_id':workspace_id})
    creds['credentials_id'] = "__".join([creds['credentials_id'],str(account_id)])
    return creds

def get_id(platform_id ,workspace_id,user_id, is_oauth2, account_id):
    if is_oauth2:
        return _get_oauth2_credentials(platform_id, user_id)
    elif not is_oauth2:
        return _get_noauth_credentials(platform_id, workspace_id, account_id)
    # return db.read_single_row('Credentials',['credentials'],creds)

def get_by_id(credentials_id):
    split_creds = credentials_id.split("__")
    if len(credentials_id.split("__"))>1:
        cred_id, account_id = split_creds[0], "__".join(split_creds[1:])
    if len(credentials_id.split("__"))==1:
        cred_id, account_id = split_creds[0], None
    creds = db.read_single_row('Credentials',['credentials'],{'credentials_id':cred_id})
    if not account_id:
        return creds
    if not creds['credentials'].get(account_id):
        return creds
    return {'credentials': creds['credentials'][account_id]}

def get(platform_id ,workspace_id,user_id, is_oauth2, account_id):
    cred_id = get_id(platform_id ,workspace_id,user_id, is_oauth2, account_id)['credentials_id']
    return get_by_id(cred_id)

def _update(credentials_id, credentials):
    creds = get_by_id(credentials_id)['credentials']
    creds.update(credentials)
    db.update('Credentials',{'credentials_id':credentials_id},{'credentials':creds})

def _create(credentials):
    return db.create('Credentials',{
            'credentials':credentials,
            })

def _persist(model_name, unique_identifiers, credentials):
    try:
        cred_id = _get_existing_cred_id(model_name, unique_identifiers)
        _update(cred_id, credentials)
    except db.errors.NoRowFound:
        cred_id = _create(credentials)
        unique_identifiers.update({'credentials_id': cred_id})
        db.create(model_name, unique_identifiers)
    return cred_id    

def _get_existing_cred_id(model_name, unique_identifiers):
    return db.read_single_row(model_name,['credentials_id'], unique_identifiers)['credentials_id']

def _oauth2_manager(cred_id, user_id, platform_id):
    try:
        db.create('PlatformUserOauth',{'user_id':user_id,'credentials_id':cred_id, 'platform_id':platform_id})
    except db.errors.DuplicateEntry:
        db.update(
            'PlatformUserOauth',
            {
                'user_id': user_id,
                'platform_id': platform_id,
                },
            {
                'credentials': cred_id
                }
            )
    
def _update_oauth2(credentials, platform_id, user_id):
    print('inside oauth 2')
    oauth2_email = credentials['email']
    unique_identifiers = {
            'platform_id':platform_id,
            'email':oauth2_email,
            }
    model_name = 'PlatformOauth2Email'
    cred_id = _persist(model_name, unique_identifiers, credentials)
    _oauth2_manager(cred_id, user_id, platform_id)
    return cred_id

def _update_no_oauth(credentials, platform_id, workspace_id, account_id):
    unique_identifiers = {
            'platform_id':platform_id,
            'workspace_id':workspace_id,
            }
    model_name = 'PlatformJson'
    creds = {account_id: credentials}
    return _persist(model_name, unique_identifiers, creds)
    
def update(credentials, platform_id, workspace_id, user_id, oauth2, account_id):
    if oauth2:
        return _update_oauth2(credentials, platform_id, user_id)
    if not oauth2:
        return _update_no_oauth(credentials, platform_id, workspace_id, account_id)
