from .errors import ProcessError, ApplicationError
import db
from db import errors as db_errors

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

def is_member(user_id, team_id):
    try:
        db.read_single_row('TeamMember',['user_id','team_id'],{'user_id':user_id, 'team_id':team_id})
        return True
    except (db.errors.MultipleRowsFound, db.errors.NoRowFound):
        return False

def _get_billing_account_id(user_id):
    try:
        billing_account = db.read_single_row('BillingAccount',['id','status'],{'user_id':user_id})
        if billing_account['status'] not in STATUS_CREATE_WORKSPACE_ALLOWED:
            raise ProcessError
        return billing_account['id']
    except db.errors.NoRowFound:
        raise
        # return db.create('BillingAccount',{'user_id':user_id}) # return id

def get_billing_account_id(user_id):
    try:
        return [_get_billing_account_id(user_id)]
    except db.errors.NoRowFound:
        return []

def update_team_name(team_id, team_name, user_id):
    from . import team
    team_owner = team.get_billing_account_id(user_id)   # list of teams in which user is an owner
    if team_id in team_owner:   # checks if team_id is present in list where you're an owner, if present update the team name 
        try:
            db.update('BillingAccount', {'id': team_id}, {'name': team_name})
            return {'id': team_id, 'name': team_name}
        except:
            return {'message': 'You are not authorized to change the team name.'}

def create(team_name, user_id):
    try:
        id = db.create('BillingAccount', {'name':team_name,'user_id':user_id, 'active':True})
        db.create('TeamMember',{'team_id':id, 'user_id':user_id})
        return {'message':'success','id':id}
    except Exception as e:
        return {'message':'error occured', 'error':e}
