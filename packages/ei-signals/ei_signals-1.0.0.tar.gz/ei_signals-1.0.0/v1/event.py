import db
import logging
logger = logging.getLogger(__name__)


def event_logs(workspace_id):
    try:
        response = []
        data = db.read('WorkspaceEvent',['name','id'],{'workspace_id':workspace_id})
        for d in data:
            temp_logs = {}
            logs = db.read('WorkspaceEventLog',['ts','count'],{'event_id':d['id']})
            for log in logs:
                log['ts'] = log['ts'].date()
                if log['ts'] in temp_logs:
                    temp_logs[log['ts']] += log['count'] 
                else:
                    temp_logs[log['ts']] = log['count']
            for key in temp_logs:
                response.append({'event_id':d['id'],'name':d['name'],'ts':key.strftime('%m/%d/%Y'), 'count':temp_logs[key]})         
        return {'success':True, 'data':response}
    except Exception as e:
        logger.error(e, exc_info=True)
        return {'success':False,'message':'error occured'}