from .errors import ProcessError, ApplicationError
import db
# from . import activity
from db import errors as db_errors

PERMISSIONS = {
    'admin': [
        'add_user',
        'create_events',
        'view_data',
        'add_datasources'
    ],
    'manager': [
        'create_events',
        'view_data',
        'add_datasources'
    ],
    'analyst': [
        'view_data',
    ]
    }

BILLING_ACCOUNT_STATUS = [
    'trial',
    'suspended',
    'pending',
    'paid'
    ]

STATUS_CREATE_WORKSPACE_ALLOWED = [
    'trial',
    'paid',    
    ]

MODEL_NAME = 'Workspace'
MODEL_FIELDS = ['name','workspace_id','colour','cts']

def get_role_name(workspace_id, role=None, role_name=None):
    if role:
        return str(workspace_id) + '__' + str(role)
    if role_name:
        ws_id, role = role_name.split('__')
        if ws_id == workspace_id:
            return role


def _get_billing_account_id(user_id):
    try:
        billing_account = db.read_single_row('BillingAccount',['id','status'],{'user_id':user_id})
        if billing_account['status'] not in STATUS_CREATE_WORKSPACE_ALLOWED:
            raise ProcessError
        return billing_account['id']
    except db.errors.NoRowFound:
        raise
        # return db.create('BillingAccount',{'user_id':user_id}) # return id

def _create_group(group_name):
    from django.contrib.auth.models import Group
    return Group.objects.create(name=group_name).id

def _update_group_permissions_workspace(group_name, workspace_id, permissions):
    from guardian.shortcuts import assign_perm
    from django.contrib.auth.models import Group
    group = Group.objects.get(name=group_name)
    from db import models
    ws = models.Workspace.objects.get(workspace_id=workspace_id)
    for perm in permissions:
        assign_perm(perm, group, ws)

def _update_group_add_member(group_name, user_id):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group
    group = Group.objects.get(name=group_name)
    user = get_user_model().objects.get(id=user_id)
    user.groups.add(group)

def read_user_permissions(user_id, workspace_id):
    from django.contrib.auth import get_user_model
    from guardian.shortcuts import get_group_perms
    from db import models
    user = get_user_model().objects.get(id=user_id)
    ws = models.Workspace.objects.get(workspace_id=workspace_id)
    return [k for k in get_group_perms(user, ws).all()]

def read_user_role(user, workspace_id):
    from db import models
    from guardian.shortcuts import get_groups_with_perms
    ws = models.Workspace.objects.get(workspace_id=workspace_id)
    groups = get_groups_with_perms(ws)
    return [group for group in groups if user in group.user_set.all()]

def _add_roles(workspace_id):
    for role in PERMISSIONS:
        role_name = get_role_name(workspace_id, role=role)
        _create_group(role_name)
        _update_group_permissions_workspace(role_name, workspace_id, PERMISSIONS[role])

def _add_admin(workspace_id, user_id):
    add_user(workspace_id, user_id, 'admin')

def create_group(workspace_id, name, auto_generated=False):
    from . import _group
    return _group.create(workspace_id, name, auto_generated)

def delete_group(workspace_id, group_id):
    from . import _group
    return _group.delete(workspace_id, group_id)

def update_group(workspace_id, group_id, platform_id, dimension_id, mapping):
    from . import _group
    return _group.update(workspace_id, group_id, platform_id, dimension_id, mapping)    

def list_groups(workspace_id):
    from . import _group
    return _group.list_bases(workspace_id)    

def _add_channel_grouping(workspace_id):
    group_name = 'Channel'
    return create_group(workspace_id, group_name, True), group_name

# def read():
#     return db.read('Workspace',['workspace_id','name'])

def update_accounts(platform_id, credentials_id, workspace_id, user_id, accounts):
    account_ids = []
    for account in accounts:
        account_id = account[0]
        account_name = account[1]
        try:
             account_ids.append( db.create('PlatformAccount',{
                'workspace_id': workspace_id,
                'platform_id': platform_id,
                'account_id': account_id,
                'name': account_name,
                'user_id': user_id,
                }))
        except db.errors.DuplicateEntry:
            db.update('PlatformAccount',{
                'workspace_id': workspace_id,
                'platform_id': platform_id,
                'account_id': account_id,
                 },{
                'name': account_name,
                'active': True,
                'user_id': user_id,
                     })
    return account_ids

def get_accounts(fields,filters):
    if not fields:
        fields = [
            'account_id',
            'name',
            'active',
            ]
    if not filters:
        filters = {}
    if 'active' not in filters:
        filters['active'] = True
    return db.read('PlatformAccount',fields,filters)

    
def set_platform_defaults(platform_id, workspace_id):
    from . import _default_setup
    group_id, group_name = _add_channel_grouping(workspace_id)
    # _default_setup.add_default_columns(platform_id, workspace_id)
    _default_setup.update_channel_group(platform_id, workspace_id, group_id, group_name, get_accounts(None, {'platform_id':platform_id, 'workspace_id': workspace_id}))
    
# def get_data_query(workspace_id, platform_id, metrics, dimensions, user_id, date_range=None):

    query_id = db.create('GetDataQuery',{
        'workspace_id': workspace_id,
        'platform_id': platform_id,
        'metrics': metrics,
        'dimensions': dimensions,
        'steps': 0,
        'user_id': user_id,
        })
    
    from . import _get_data
    from . import platform
    p = platform.get(fields=['overall'],platform_id=platform_id)[0]
    p_filters = {'workspace_id': workspace_id}
    if not p['overall']:
        p_filters['platform_id']=platform_id
    steps, config = _get_data.query(query_id, workspace_id, platform_id, metrics, dimensions, get_accounts(['platform_id','account_id','user_id'],p_filters),date_range)
    db.update(
        'GetDataQuery',
        {
            'query_id': query_id,
            },
        {
            'steps': steps,
            'config': config,
            }
    )
    if not steps:
        raise ApplicationError()
    return {'query_id':query_id}

# def _validate_dataview_workspace(dataview_id, workspace_id):
    db.read_single_row('View',['dataview_id'],{'dataview_id':dataview_id, 'workspace_id': workspace_id})

# def get_dataview_query(workspace_id, dataview_id, metrics, dimensions, date_range, user_id):
    _validate_dataview_workspace(dataview_id, workspace_id)
    from . import _get_data
    import re
    start,end = ['-'.join([k.split('/')[2],k.split('/')[1],k.split('/')[0]]) for k in date_range.split('-')]
    schema_name = db.read_single_row_by_pk('View', dataview_id, ['schema_name'])['schema_name']
    dims = [{'name': k['name'], 'value': re.sub(r'[^A-Za-z0-9_ ]+', '', k['name']).replace(' ','_').lower()} for k in dimensions]
    mets = [{'name': k['name'], 'value': re.sub(r'[^A-Za-z0-9_ ]+', '', k['name']).replace(' ','_').lower()} for k in metrics]
    config = {
        'schema_name': schema_name, 
        'start': start,
        'end': end, 
        'dimensions': dims, 
        'metrics': mets, 
        'database': 'wk'+workspace_id,
        'dataview_id': dataview_id,
        'columns': [k['name'] for k in dimensions+metrics]
        }
    query_id = db.create('GetDataQuery',{
        'workspace_id': workspace_id,
        'platform_id': '0e20c3c2-5cce-49e1-9546-138cdfe6b2ff',
        'metrics': metrics,
        'dimensions': dimensions,
        'steps': 2,
        'user_id': user_id,
        'config': config,
        })
    _get_data.dataview_query(query_id, config)
    return {'query_id':query_id} 

    
# def get_query_response(query_id):
    steps = db.read_single_row_by_pk('GetDataQuery', query_id, ['steps'])['steps']
    from . import _get_data
    query_data = _get_data.get_query_status(query_id, steps)
    return query_data

# def list_dataviews(workspace_id):
    from . import users
    views =  db.read('View',['dataview_id','name','created_by_id','platform_id','schema_name'],{'workspace_id':workspace_id})
    for view in views:
        view['created_by'] = users.get(view['created_by_id'])['name']
        columns = db.read('ColumnView',['ui_name','is_dimension','col_id'],{'dataview_id':view['dataview_id']})
        view['columns'] = []
        for column in columns:
            col_detail = db.read_single_row_by_pk('AllColumn',column['col_id'],['t'])
            view['columns'].append({
                'name': column['ui_name'],
                't': col_detail['t'],
                'category': 'Dimension' if column['is_dimension'] else 'Metric',
                'col_id': column['col_id'],
                })
        try:
            view_details = db.read_single_row_by_pk('DataViewStatus',view['dataview_id'],['nrows', 'n_days'])
            view.update(view_details)
        except db.errors.NoRowFound:
            view['nrows'] = 0
            view['n_days'] = 0
    return views

# def add_platform(workspace_id, platform_id, no_oauth_data, redirect_uri, user_id):
    from . import platform, credentials
    is_oauth2 = platform.is_oauth2(platform_id)
    #if not is_oauth2:
    #    parsed_data = platform.parse_no_oauth_data(platform_id, no_oauth_data)
    #    credentials.update(parsed_data['credentials'], platform_id, workspace_id, user_id, is_oauth2)
    return {}
    
def add_account(workspace_id, platform_id, no_oauth_data, account_id, account_name, user_id):
    from . import platform, credentials, _column
    is_oauth2 = platform.is_oauth2(platform_id)
    if is_oauth2:
        accounts = [(account_id,account_name)]
    elif not is_oauth2:
        parsed_data = platform.parse_no_oauth_data(platform_id, no_oauth_data)
        accounts = [parsed_data['account']]
        credentials.update(parsed_data['credentials'], platform_id, workspace_id, user_id, is_oauth2, accounts[0][0])
    credentials_id = credentials.get_id(platform_id ,workspace_id,user_id, is_oauth2, accounts[0][0])
    account_ids = update_accounts(platform_id, credentials_id, workspace_id, user_id, accounts)
    set_platform_defaults(platform_id, workspace_id)
    # account_credentials = credentials.get(platform_id ,workspace_id,user_id, is_oauth2)['credentials']
    # try: 
    #     from fetl.v1 import account_custom_metrics
    #     for account in accounts:
    #         account_id = account[0]
    #         creds = credentials.get(platform_id ,workspace_id,user_id, is_oauth2, account_id)['credentials']
    #         custom_metrics = account_custom_metrics(platform.get_api(platform_id),account_id,creds)
    #         for custom_metric in custom_metrics:
    #             if len(custom_metric)!=2:
    #                 _column.add_custom_columns_to_WorkspaceEntityAttributes(account['platform_id'],account['account_id'],custom_metric[0],[custom_metric[1]],'text')
    #                 continue
    #             _column.add_custom_metric(platform_id,account_id,custom_metric[0],custom_metric[1])
    # except:
    #     pass
    return account_ids

def list_platforms(workspace_id):
    accounts = db.read(
        'PlatformAccount',[
            'platform_id',
            ],
        {
            'active':True,
            'workspace_id': workspace_id,
        })
    platforms = set(k['platform_id'] for k in accounts)
    from . import platform
    overall_id = platform.get(fields=['platform_id'],overall=True)[0]['platform_id']
    platforms.add(overall_id)
    
    #workspace_columns = db.read('ColumnWorkspace',['platform_id'],{'workspace_id':workspace_id})
    #workspace_columns_platforms = set([k['platform_id'] for k in workspace_columns])
    # from . import platform
    # non_blend_platforms = set([k['platform_id'] for k in platform.get(blend=False)])
    # workspace_columns_platforms_blend = workspace_columns_platforms - non_blend_platforms
    #platforms.update(workspace_columns_platforms)
    return list(platforms)

# def _default_analytic_columns(platform_id, workspace_id):
    from . import _column, platform
    workspace_accounts = get_accounts(['account_id','platform_id'], {'workspace_id': workspace_id})
    workspace_platforms = list(set([k['platform_id'] for k in workspace_accounts]))
    non_blended_platforms = [k['platform_id'] for k in platform.get(overall=False)]
    analytic_platforms = [k for k in non_blended_platforms if platform.is_analytic(k)]
    platform_default_metrics = []
    for p in workspace_platforms:
        if p not in analytic_platforms:
            continue
        platform_name = platform.get(fields=['name'],platform_id=p)[0]['name']
        p_columns = _column.list_platform(p)
        p_columns = [k for k in p_columns if k['t']==_column.T_VALUE['metric_additive']]
        platform_accounts = [k for k in workspace_accounts if k['platform_id']== p]
        for account in platform_accounts:
            p_columns += _column.list_account_custom_metric(p, account['account_id'])
        for c in p_columns:
            c['category'] = platform_name
        platform_default_metrics += p_columns
    return platform_default_metrics

# def list_custom_columns(workspace_id, platform_id):
    from v3 import platform, _column
    p = platform.get(fields=['overall'],platform_id=platform_id)[0]
    platform_accounts = get_accounts(['account_id','platform_id'], {'workspace_id': workspace_id, 'platform_id': platform_id}) # empty list for overall
    columns = _column.list_workspace_custom(platform_id, workspace_id)
    for c in columns:
        if c['t'] == 0:
            c['category'] = 'Dimension'
        if c['t'] in (1,2):
            c['category'] = 'Metric'        
    for account in platform_accounts:
        cm_columns = _column.list_account_custom_metric(account['platform_id'], account['account_id'])
        for c in cm_columns:
            c['category'] = 'CustomMetric'
        columns += cm_columns
    if not p['overall']:
        return columns
    return columns + _default_analytic_columns(platform_id, workspace_id)

# def get_credentials(workspace_id):
    data = db.read_single_row_by_pk('WorkspaceCredentials',workspace_id,['password'])
    data['user'] = 'wk'+workspace_id
    data['database'] = 'wk'+workspace_id
    billing_account_id = db.read_single_row_by_pk('Workspace',workspace_id,['billing_account_id'])['billing_account_id']
    try:
        ip_address = db.read_single_row_by_pk('BillingAccountServer',billing_account_id,['ip_address'])['ip_address']
        data['host'] = ip_address
    except db.errors.NoRowFound:
        data['host'] = ''
    return data

# def add_destination(workspace_id, destination_id):
    db.delete('WorkspaceDestination', {'workspace_id':workspace_id})
    try:
        db.create(
            'WorkspaceDestination',
            {
                'workspace_id': workspace_id,
                'destination_id': destination_id,
                }
        )
    except db.errors.DuplicateEntry:
        raise

# def list_destinations(workspace_id):
    d = db.read('WorkspaceDestination',['destination_id'],{'workspace_id':workspace_id})
    return [k['destination_id'] for k in d]

# def _add_dataview_table(workspace_id, view_id, dimensions, metrics, name, fetch_data):
    billing_account_id = db.read_single_row('Workspace',['billing_account_id'],{'workspace_id':workspace_id})["billing_account_id"]
    try:
        ip_address = db.read_single_row_by_pk('BillingAccountServer',billing_account_id,['ip_address'])['ip_address']
    except db.errors.NoRowFound:
        return
    import os
    import yaml
    import psycopg2
    import re
    from django.conf import settings
    with open(os.path.join(settings.BASE_DIR,'appei.yaml'), 'r') as f:
        appei_yaml = yaml.load(f, Loader=yaml.SafeLoader)
    appei_yaml['IP_ADDRESS'] = ip_address
    appei_yaml['DBNAME'] = 'wk'+workspace_id
    cols = ','.join(['date date']+[re.sub(r'[^A-Za-z0-9_ ]+', '', k['name']).replace(' ','_').lower()+' text' for k in dimensions if k['name']!='Date']+[re.sub(r'[^A-Za-z0-9_ ]+', '', k['name']).replace(' ','_').lower()+' numeric' for k in metrics])
    schema_name = re.sub(r'[^A-Za-z0-9_ ]+', '', name).replace(' ','_').lower()
    try:
        conn = psycopg2.connect("dbname={WEBHOOKS_DB_NAME} host={IP_ADDRESS} port={WEBHOOKS_DB_PORT} user={WEBHOOKS_DB_USER} password={WEBHOOKS_DB_PASSWORD}".format(**appei_yaml))
        cursor = conn.cursor()
        entry_q = f"""insert into public.dataviews (dbname,tablename,dataview_id) values ('wk{workspace_id}','{schema_name}','{view_id}') on conflict do nothing;"""
        cursor.execute(entry_q)
        conn.commit()
        cursor.close()
        conn.close()
    except:
        return
    _create_database(workspace_id, billing_account_id)
    try:
        conn = psycopg2.connect("dbname={DBNAME} host={IP_ADDRESS} port={WEBHOOKS_DB_PORT} user={WEBHOOKS_DB_USER} password={WEBHOOKS_DB_PASSWORD}".format(**appei_yaml))
        cursor = conn.cursor()
        q = f"""CREATE TABLE public.{schema_name} ({cols});; GRANT SELECT ON public.{schema_name} to "wk{workspace_id}";"""
        cursor.execute(q)
        conn.commit()
        cursor.close()
        if fetch_data:
            import petl
            import pandas as pd
            col_list = [re.sub(r'[^A-Za-z0-9_ ]+', '', k['name']).replace(' ','_').lower() for k in dimensions+metrics]
            if 'date' not in col_list:
                col_list =['date']+col_list
            df = pd.DataFrame(fetch_data,columns=col_list)
            data = petl.fromdataframe(df)
            petl.todb(data,conn, schema_name, schema='public')
        conn.close()
    except:
        return




# def create_dataview(workspace_id, name, platform_id, metrics, dimensions, user_id, view_type_id, fetch_data=None):
    from . import billing
    n_days = billing.get_historical_days(view_type_id)
    if len([k['name'] for k in dimensions+metrics])>len(set([k['name'] for k in dimensions+metrics])):
        raise ProcessError
    try:
        import re
        if len(str(name))>50:
            name = str(name)[:50]
        view_id = db.create(
            'View', {
                'workspace_id': workspace_id,
                'name': name,
                'created_by_id': user_id,
                'active': True,
                'platform_id': platform_id,
                'schema_name': re.sub(r'[^A-Za-z0-9_ ]+', '', name).replace(' ','_').lower(),
                'historical_days': n_days,
                'view_type_id': view_type_id
                }
            )
        from . import _column
        _column.add_view_columns(view_id, metrics, dimensions, workspace_id)
        credentials = get_credentials(workspace_id)
        from . import _get_data
        from . import platform
        p = platform.get(fields=['overall'],platform_id=platform_id)[0]
        p_filters = {'workspace_id': workspace_id}
        if not p['overall']:
            p_filters['platform_id']=platform_id
        _get_data.dataview(workspace_id, platform_id, metrics, dimensions, get_accounts(['platform_id','account_id','user_id'],p_filters), view_id, name)
        config = {'dataview': {"metrics": metrics, "dimensions": dimensions, "name": name, "dataview_id": view_id}, 'destination': {'destinations': [], 'credentials': credentials}}
        _get_data.add_destination(config)
        _add_dataview_table(workspace_id, view_id, dimensions, metrics, name, fetch_data)
        # activity.create_dataview(user_id, workspace_id, view_id, view_type_id)
        return view_id
    except db.errors.DuplicateEntry:
        return create_dataview(workspace_id, name+name[0], platform_id, metrics, dimensions, user_id, view_type_id)

# def _remove_dataview_table(workspace_id, view_id):
    billing_account_id = db.read_single_row('Workspace',['billing_account_id'],{'workspace_id':workspace_id})["billing_account_id"]
    try:
        ip_address = db.read_single_row_by_pk('BillingAccountServer',billing_account_id,['ip_address'])['ip_address']
    except db.errors.NoRowFound:
        return
    import os
    import yaml
    import psycopg2
    import re
    from django.conf import settings
    with open(os.path.join(settings.BASE_DIR,'appei.yaml'), 'r') as f:
        appei_yaml = yaml.load(f, Loader=yaml.SafeLoader)
    appei_yaml['IP_ADDRESS'] = ip_address
    appei_yaml['DBNAME'] = 'wk'+workspace_id
    try:
        schema_name = db.read_single_row_by_pk('AllViews', view_id, ['schema_name'])['schema_name']
        conn = psycopg2.connect("dbname={WEBHOOKS_DB_NAME} host={IP_ADDRESS} port={WEBHOOKS_DB_PORT} user={WEBHOOKS_DB_USER} password={WEBHOOKS_DB_PASSWORD}".format(**appei_yaml))
        cursor = conn.cursor()
        entry_q = f"""update public.dataviews set active=False where dataview_id='{view_id}';"""
        cursor.execute(entry_q)
        conn.commit()
        cursor.close()
        conn.close()
        conn = psycopg2.connect("dbname={DBNAME} host={IP_ADDRESS} port={WEBHOOKS_DB_PORT} user={WEBHOOKS_DB_USER} password={WEBHOOKS_DB_PASSWORD}".format(**appei_yaml))
        cursor = conn.cursor()
        q = f"""DROP TABLE public.{schema_name};"""
        cursor.execute(q)
        conn.commit()
        cursor.close()
        conn.close()
    except:
        return

# def delete_dataview(user_id, workspace_id, dataview_id):
    d = db.read_single_row('View', ['view_type_id','name','schema_name'], {'dataview_id':dataview_id, 'workspace_id':workspace_id})
    view_type_id = d['view_type_id']
    _remove_dataview_table(workspace_id,dataview_id)
    db.update('View',{'dataview_id':dataview_id, 'workspace_id':workspace_id},{'active':False, 'name': "-".join([d['name'],dataview_id])[0:50], 'schema_name': "_".join([d['schema_name'],dataview_id])[0:50]})
    db.delete('Metric', {'workspace_id': workspace_id, 'dataview_id': dataview_id})
    # activity.delete_dataview(user_id, workspace_id, dataview_id, view_type_id)
    return dataview_id

# def update_destination(workspace_id):
    config = {}
    destinations = list_destinations(workspace_id)
    credentials = get_credentials(workspace_id)
    config['destination'] = {'destinations': destinations, 'credentials': credentials}
    from . import _get_data
    return _get_data.add_destination(config)



def delete_accounts(workspace_id, accounts):
    for account in accounts:
        db.delete(
            'PlatformAccount',
            {
                'workspace_id': workspace_id,
                'platformaccount_id': account,
                }
            )
    # set_platform_defaults(platform_id, workspace_id)
        
                
def list_all_users(workspace_id):
    from django.contrib.auth import get_user_model
    workspace_users=[]
    for role in PERMISSIONS:
        group_name = get_role_name(workspace_id, role=role, role_name=None)
        users = get_user_model().objects.filter(groups__name = group_name)
        workspace_users = workspace_users + [k.id for k in users]
    return workspace_users

def list_users(workspace_id):
    from django.contrib.auth import get_user_model
    workspace_users = []
    for role in PERMISSIONS:
        group_name = get_role_name(workspace_id, role=role, role_name=None)
        users = get_user_model().objects.filter(groups__name = group_name)
        for user in users:
            user_data = {'name':user.name, 'email':user.email, 'icon':user.icon}
            user_data['role'] = role
            user_data['user_id'] = user.id
            workspace_users.append(user_data)
    return workspace_users

def _add_team_member(workspace_id, user_id):
    team_id = db.read_single_row_by_pk('Workspace',workspace_id,['billing_account_id'])['billing_account_id']
    try:
        db.create('TeamMember',{
            'team_id': team_id,
            'user_id': user_id,
            })
    except db.errors.DuplicateEntry:
        pass

def _remove_team_member(workspace_id, user_id):
    team_id = db.read_single_row('Workspace',['billing_account_id'],{'workspace_id':workspace_id})["billing_account_id"]
    from . import users
    w_ids = users.get_user_workspaces(user_id)
    team_workspaces = db.read('Workspace',['workspace_id'],{'billing_account_id':team_id,"workspace_id__in":w_ids})
    if len(team_workspaces) > 0:
        return
    db.delete('TeamMember',{'user_id':user_id,'team_id':team_id})

def add_user(workspace_id, user_id, role):
    _update_group_add_member(get_role_name(workspace_id, role), user_id)
    _add_team_member(workspace_id, user_id)
    return {'user_id':user_id}

def delete_user(workspace_id, user_id):
    from django.contrib.auth import get_user_model
    user = get_user_model().objects.get(id=user_id)
    groups = read_user_role(user, workspace_id)
    for group in groups:
        group.user_set.remove(user)
    _remove_team_member(workspace_id, user_id)
    return {}

def update_user(workspace_id, user_id, role):
    delete_user(workspace_id, user_id)
    add_user(workspace_id, user_id, role)
    return {'user_id':user_id}
    

# def _add_default_destination(workspace_id):
    from django.conf import settings
    destination_id = settings.DEFAULT_DESTINATION_ID
    add_destination(workspace_id, destination_id)

# def _create_database(workspace_id, billing_account_id):
    try:
        ip_address = db.read_single_row_by_pk('BillingAccountServer',billing_account_id,['ip_address'])['ip_address']
    except db.errors.NoRowFound:
        return
    password = db.read_single_row_by_pk('WorkspaceCredentials',workspace_id,['password'])['password']
    import os
    import yaml
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    from psycopg2 import sql
    from django.conf import settings
    with open(os.path.join(settings.BASE_DIR,'appei.yaml'), 'r') as f:
        appei_yaml = yaml.load(f, Loader=yaml.SafeLoader)
    appei_yaml['IP_ADDRESS'] = ip_address
    appei_yaml['DBNAME'] = 'wk'+workspace_id
    try:
        conn = psycopg2.connect("dbname={WEBHOOKS_DB_NAME} host={IP_ADDRESS} port={WEBHOOKS_DB_PORT} user={WEBHOOKS_DB_USER} password={WEBHOOKS_DB_PASSWORD}".format(**appei_yaml))
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        dbname = sql.Identifier(f'wk{workspace_id}')
        create_q = sql.SQL("CREATE DATABASE {};").format(dbname)
        user_q =  sql.SQL("CREATE USER {} with password "+f"'{password}'"+";").format(dbname)
        cursor.execute(create_q)
        cursor.execute(user_q)
        cursor.close()
        conn.close()
        conn = psycopg2.connect("dbname={DBNAME} host={IP_ADDRESS} port={WEBHOOKS_DB_PORT} user={WEBHOOKS_DB_USER} password={WEBHOOKS_DB_PASSWORD}".format(**appei_yaml))
        cursor = conn.cursor()
        q = f"""REVOKE ALL ON DATABASE "wk{workspace_id}" FROM public; GRANT CONNECT ON DATABASE "wk{workspace_id}" to "wk{workspace_id}"; GRANT USAGE ON SCHEMA public to "wk{workspace_id}"; ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO "wk{workspace_id}";"""
        cursor.execute(q)
        conn.commit()
        cursor.close()
        conn.close()
    except:
        return



def _default_workspace_setup(workspace_id, user_id):
    # db.create('WorkspaceCredentials',{'workspace_id':workspace_id})
    # db.create('WebhookKey',{'workspace_id':workspace_id})
    _add_roles(workspace_id)
    # _add_default_destination(workspace_id)
    _add_admin(workspace_id, user_id)
    _add_channel_grouping(workspace_id)
    # from . import _overall
    # _overall.add_default_blend(workspace_id)

def default_workspace_setup(workspace_id, user_id):
    _default_workspace_setup(workspace_id, user_id)

def create(name, colour, user_id):
    try:
        billing_account_id = _get_billing_account_id(user_id)
    except db.errors.NoRowFound:
        return {"success":False, "message":"Not authorized to create workspace"}
    try:
        workspace_id = db.create(
            'Workspace',{
                'name':name,
                'billing_account_id': billing_account_id,
                'colour': colour,
            }
        )
        _default_workspace_setup(workspace_id, user_id)
        # _create_database(workspace_id, billing_account_id)
        # activity.create_workspace(user_id, workspace_id)
        return {"workspace_id" : workspace_id, "name" : name, "success" : True, "colour": colour}
    except db.errors.DuplicateEntry:
        return create(name+name[0], colour, user_id)

# def _delete_database(workspace_id):
    billing_account_id = db.read_single_row('Workspace',['billing_account_id'],{'workspace_id':workspace_id})["billing_account_id"]
    try:
        ip_address = db.read_single_row_by_pk('BillingAccountServer',billing_account_id,['ip_address'])['ip_address']
    except db.errors.NoRowFound:
        return
    import os
    import yaml
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    from psycopg2 import sql
    from django.conf import settings
    with open(os.path.join(settings.BASE_DIR,'appei.yaml'), 'r') as f:
        appei_yaml = yaml.load(f, Loader=yaml.SafeLoader)
    appei_yaml['IP_ADDRESS'] = ip_address
    appei_yaml['DBNAME'] = 'wk'+workspace_id
    try:
        conn = psycopg2.connect("dbname={WEBHOOKS_DB_NAME} host={IP_ADDRESS} port={WEBHOOKS_DB_PORT} user={WEBHOOKS_DB_USER} password={WEBHOOKS_DB_PASSWORD}".format(**appei_yaml))
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        dbname = sql.Identifier(f'wk{workspace_id}')
        create_q = sql.SQL("DROP DATABASE {};").format(dbname)
        user_q =  sql.SQL("DROP USER {} ;").format(dbname)
        cursor.execute(create_q)
        cursor.execute(user_q)
        cursor.close()
        conn.close()
    except:
        return

# def delete(user_id, workspace_id):
    _delete_database(workspace_id)
    # activity.delete_workspace(user_id, workspace_id)
    # db.create('WorkspaceDelete',{'workspace_id':workspace_id})
    return db.update('Workspace',{'workspace_id':workspace_id},{'active':False})
    
# def get_dimension_data(workspace_id, platform_id, dimension_id):
    from . import credentials, platform
    raw_accounts = get_accounts(['user_id','account_id'],{'platform_id':platform_id, 'workspace_id':workspace_id})
    accounts = []
    creds = {}
    for acc in raw_accounts:
        a = {'account_id': acc['account_id']}
        a['credential_id'] = credentials.get_id(platform_id,workspace_id,acc['user_id'],platform.is_oauth2(platform_id), a['account_id'])['credentials_id']
        accounts.append(a)
        cred_id = a['credential_id']
        if cred_id not in creds:
            creds[cred_id] = credentials.get_by_id(cred_id)['credentials']
    from . import _column, platform
    dim = _column.get_config({'col_id':dimension_id,'name':'name'}, workspace_id)[platform_id]['api_name']
    api = platform.get_api(platform_id)
    import fetl.v1
    return fetl.v1.get_dimension_data(api, accounts, creds, dim)

def update(workspace_id, name, color):
    try:
        db.update(
            'Workspace',
            {
                'workspace_id': workspace_id,
            },
            {
                'name':name,
                'colour': color,
            },
        )
        return {'workspace_id':workspace_id, 'name':name, 'color': color, 'success':True}
    except db.errors.DuplicateEntry:
        return {"message":"Please select a different name"}

# def read_dataview(dataview_id, user_id):
    source_workspace_id = db.read_single_row_by_pk('View', dataview_id, ['workspace_id'])['workspace_id']
    user_permissions = read_user_permissions(user_id, source_workspace_id)
    if 'view_data' not in user_permissions:
        raise ProcessError
    from . import dataview
    return dataview.read(dataview_id)

# def copy_dataview(workspace_id, source_dataview_id, name, user_id, view_type_id):
    dv = read_dataview(source_dataview_id, user_id)
    return create_dataview(workspace_id, name, dv['platform_id'], dv['metrics'], dv['dimensions'], user_id, view_type_id)    

# def create_metric(workspace_id, data, user_id):
    from . import _metric
    return _metric.create(workspace_id, data, user_id)

# def list_metric(workspace_id):
    from . import _metric
    return _metric.get(workspace_id)

# def delete_metric(workspace_id, metric_id, user_id):
    from . import _metric
    return _metric.delete(workspace_id, metric_id)

# def create_alert(workspace_id, data, user_id):
    from . import _alert
    return _alert.create(workspace_id, data, user_id)

# def list_alert(workspace_id):
    from . import _alert
    return _alert.get(workspace_id)

# def delete_alert(workspace_id, alert_id, user_id):
    from . import _alert
    return _alert.delete(workspace_id, alert_id)

# def list_webhook_key(workspace_id):
    key = ''
    try:
        key = db.read_single_row_by_pk('WebhookKey',workspace_id,['key'])['key']
    except db.errors.NoRowFound:
        key = 'No key found'
    platforms = db.read('WebhookSource',['platform_id','name','icon','webhook_name', 'link'])
    return {'key': key, 'platforms': platforms}

# def list_webhook_pings(workspace_id, platform_id):
    config = list_webhook_key(workspace_id)
    webhook_key = config['key']
    if not webhook_key:
        return {'pings':[]}
    webhoook_sources = [k['webhook_name'] for k in config['platforms'] if k['platform_id']==platform_id]
    if not webhoook_sources:
        return {'pings':[]}
    webhoook_source = webhoook_sources[0]
    import os
    import yaml
    import psycopg2
    import psycopg2.extras
    from django.conf import settings
    import datetime
    import json
    with open(os.path.join(settings.BASE_DIR,'appei.yaml'), 'r') as f:
        appei_yaml = yaml.load(f, Loader=yaml.SafeLoader)
    q = f"select ts,payload from webhooks where tool='{webhoook_source}' and key='{webhook_key}' order by ts desc limit 5"
    try:
        conn = psycopg2.connect("dbname={WEBHOOKS_DB_NAME} host={WEBHOOKS_DB_HOST} port={WEBHOOKS_DB_PORT} user={WEBHOOKS_DB_USER} password={WEBHOOKS_DB_PASSWORD}".format(**appei_yaml))
        cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cursor.execute(q)
        data = list(cursor)
        cursor.close()
        conn.close()
    except:
        data=[]
    def get_time_str(ts):
        cts = datetime.datetime.now()
        ts = datetime.datetime.strptime(str(ts)[:19],"%Y-%m-%d %H:%M:%S")
        diff_secs = (cts - ts).seconds
        if diff_secs <60:
            return f'{diff_secs} seconds ago'
        elif diff_secs < 3600: 
            return f'{int(diff_secs/60)} minutes ago'
        elif diff_secs < 86400:
            return f'{int(diff_secs/3600)} hours ago'
        else:
            return f'{int(diff_secs/86400)} days ago'

    result = [[get_time_str(k.ts), json.dumps(k.payload)]for k in data]
    return {'pings': result}

# def create_aisensy_workspace(user_id):
    try:
        billing_account_id = _get_billing_account_id(user_id)
    except db.errors.NoRowFound:
        billing_account_id = db.create('BillingAccount',{'user_id':user_id})['billing_account_id']
    try:
        create("AiSensy CTWA", "#4D4242", user_id)
    except Exception as e:
        pass



# def get_metric_data(workspace_id, metric_id, user_id, date_range):
    start,end = ['-'.join([k.split('/')[2],k.split('/')[1],k.split('/')[0]]) for k in date_range.split('-')]
    import datetime
    import pandas as pd
    from . import _metric
    start_date  = datetime.datetime.strptime(start,"%Y-%m-%d")
    end_date = datetime.datetime.strptime(end,"%Y-%m-%d")
    dates = []
    while end_date>=start_date:
        dates.append([start_date.strftime("%Y-%m-%d"),1])
        start_date = start_date + datetime.timedelta(days=1)
    df2 = pd.DataFrame(dates,columns=['Date','Row Count'])
    metric = _metric.get_by_id(metric_id)
    dataview_id = metric['dataview_id']
    from fetl.v1 import read_file
    df = read_file(f'dataview_{dataview_id}/final.txt')
    df = df[df['Date']>=start][df['Date']<=end]
    df[metric['name']], aggregate = _metric.get_dataview_metric(df,metric)
    df = df.groupby(['Date']).sum(numeric_only=True)[metric['name']]
    final_df = df2.set_index('Date').join(df).reset_index()
    final_df = final_df.fillna(0)
    return final_df[['Date',metric['name']]].values.tolist(), aggregate






