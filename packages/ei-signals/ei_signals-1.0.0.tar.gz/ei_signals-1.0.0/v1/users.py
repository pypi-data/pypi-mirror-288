from django.contrib.auth import get_user_model

import db

def create(name, email, icon):
    return get_user_model().objects.create_user(name=name, email=email, icon=icon).id

def list_team_workspaces(team_id, user_id):
    # if not is_team_member(user_id, team_id):
    #     return []
    from . import team, users, workspace
    team_ids = team.get_billing_account_id(user_id) # list of teams corresponding to user
    from django.contrib.auth import get_user_model
    user = get_user_model().objects.get(id=user_id) # user corresponding to user_id
    workspace_filter = {'billing_account_id':team_id}
    if team_id not in team_ids:
        workspace_filter['workspace_id__in'] = users.get_user_workspaces(user_id) 
    workspace_details = db.read(workspace.MODEL_NAME, workspace.MODEL_FIELDS, workspace_filter)
    # for ws in workspace_details:
    #     ws["dataviews_count"] = len(db.read("View", [], {"workspace_id": ws["workspace_id"]}))
    #     ws["users_count"] = len(workspace.list_all_users(workspace_id=ws["workspace_id"]))
    #     try:
    #         ws["active_user_role"] = workspace.get_role_name(workspace_id=ws["workspace_id"], role=None, role_name=str(workspace.read_user_role(user=user, workspace_id=ws["workspace_id"])[0]))
    #     except IndexError as e:
    #         ws['active_user_role'] = "No Role"
    return workspace_details

def get(user_id):
    from django.contrib.auth import get_user_model
    user = get_user_model().objects.get(pk=user_id)
    teams = [{'id':k['team'].id, 'name':k['team'].name} for k in db.read('TeamMember',['team'],{'user_id':user_id})]
    from . import team
    team_owner = team.get_billing_account_id(user_id)
    team_owner_detail=[db.read_single_row('BillingAccount', ['id','name'], {'id': i}) for i in team_owner]
    workspaces = []
    if len(teams) >0:
        workspaces = list_team_workspaces(teams[0]['id'],user_id)
    # from . import stripe_util
    # billing_status = stripe_util.get_subscription_status(teams)
    return {'name':user.name,'email':user.email,'icon':user.icon, 'user_id':user_id, 'member': teams, 'owner': team_owner, 'owner_detail': team_owner_detail, 'workspaces':workspaces}

# def list_workspaces(user_id):
#     from django.contrib.auth import get_user_model
#     from guardian.shortcuts import get_objects_for_user
#     workspaces = []
#     user = get_user_model().objects.get(id=user_id)
#     user_ws = get_objects_for_user(user,'view_data',db.models.Workspace)
#     return user_ws

def get_user_workspaces(user_id):
    from django.contrib.auth import get_user_model
    from guardian.shortcuts import get_objects_for_user
    workspaces = []
    user = get_user_model().objects.get(id=user_id)
    return [k.workspace_id for k in get_objects_for_user(user,'view_data',db.models.Workspace)]
    
def get_workspaces(user_id):
    from django.contrib.auth import get_user_model
    from guardian.shortcuts import get_objects_for_user
    workspaces = []
    user = get_user_model().objects.get(id=user_id)
    user_ws = get_objects_for_user(user,'view_data',db.models.Workspace)
    for k in user_ws:
        data = {
            'id' : k.workspace_id,
            'name': k.name,
            'colour': k.colour,
            }
        workspaces.append(data)
    return workspaces

def get_authorized_platforms(user_id):
    from . import platform
    authorized_platforms = []
    all_platforms = platform.get(fields=['platform_id'])
    from . import credentials
    for p in all_platforms:
        p_id = p['platform_id']
        if not platform.is_oauth2(p_id):
            continue
        try:
            credentials.get_id(p_id ,None,user_id, True, None)
            authorized_platforms.append(p_id)
        except db.errors.NoRowFound:
            pass
    return authorized_platforms

def add_workspace_user(workspace_id, name, email, role):
    user_id = create(name, email, '')
    from . import workspace
    workspace.add_user(workspace_id, user_id, role)
    return {'user_id':user_id}
