from user._verify_shopify_token import verify_shopify_jwt
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login

UserModel = get_user_model()

def create_team(user):
    from . import workspace, team, users
    teams = team.get_billing_account_id(user.id)
    if len(teams)>0:
        workspaces = users.list_team_workspaces(teams[0],user.id)
        return {'team_id':teams[0],'workspace_id':workspaces[0]['workspace_id']}
    create_team_response = team.create('team', user.id)
    if create_team_response['message']=='success':
        team_id = create_team_response['id']
    else:
        return None
    create_workspace_response = workspace.create(user.name,'',user.id)
    if create_workspace_response['success']:
        workspace_id = create_workspace_response['workspace_id']
    else:
        #remove billing account created
        return None
        # return JsonResponse({'success':False, 'message':create_workspace_response['message']})
    return {'team_id':team_id, 'workspace_id':workspace_id}

def get_user_info(request, token, shop):
    # token and shop will be used to setup ei-pixel and generate shopify offline access token
    data = create_team(request.user)
    return data
