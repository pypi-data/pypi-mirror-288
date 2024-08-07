import db
from db import errors as db_errors
from . import errors

def _mapping_to_ui(mapping, mapping_seq):
    return [[k,mapping[k]] for k in mapping_seq]

def _ui_to_mapping(mapping):
    m = {k[0]:k[1] for k in mapping}
    mapping_seq = [k[0] for k in mapping]
    return m, mapping_seq

def merge(old_mapping, new_mapping):
    o_keys = [k[0] for k in old_mapping]
    old_mapping += [[k,new_mapping[k]] for k in new_mapping if k not in o_keys]
    return old_mapping

def create(workspace_id, name, auto_generated=False):
    try:
        return db.create('Group',{
            'workspace_id': workspace_id,
            'name': name,
            'normalized_name': name.lower(),
            })
    except db_errors.DuplicateEntry:
        return db.read_single_row('Group',['group_id'],{
            'workspace_id': workspace_id,
            'normalized_name': name.lower(),
            })['group_id']

def delete(workspace_id, group_id):
    try:
        group = db.read_single_row('Group',['group_id'],{'group_id':group_id, 'workspace_id':workspace_id, 'auto_generated':False})
    except db.errors.NoRowFound:
        return group_id
    bases = db.read('GroupBase',['col_id'],{'group_id':group_id})
    col_ids = [k['col_id'] for k in bases]
    db.delete('AllColumn',{'col_id__in':col_ids})
    db.delete('Group',{'group_id':group_id, 'workspace_id':workspace_id})
    return group_id

def update(workspace_id, group_id, platform_id, dimension_id, mapping):
    base_mapping, base_mapping_seq = _ui_to_mapping(mapping)
    group = db.read_single_row_by_pk('Group',group_id,['workspace_id', 'name'])
    group_workspace_id = group['workspace_id']
    if not workspace_id == group_workspace_id:
        raise errors.InvalidRequest()
    from . import _column
    try:
        base = db.read_single_row('GroupBase',['col_id','base_dimension_id'],{'group_id':group_id, 'platform_id':platform_id})
        # if not _column.match(dimension_id, base['base_dimension_id']):
        #     raise errors.InvalidRequest()
        db.update('GroupBase',{'col_id':base['col_id']},{
            'mapping': base_mapping,
            'mapping_seq': base_mapping_seq,
            })
        return base['col_id']
    except db.errors.NoRowFound:
        column_id = _column.workspace_api(workspace_id, dimension_id)
        base_id = _column.workspace_group(workspace_id, platform_id, group_id, group['name'])
        from . import _overall
        _overall.check_group_column(group_id, group['name'], workspace_id)
        return db.create('GroupBase',{
            'group_id':group_id,
            'platform_id':platform_id,
            'base_dimension_id': column_id,
            'col_id':base_id,
            'mapping': base_mapping,
            'mapping_seq': base_mapping_seq,
        })

def list_bases(workspace_id, group_id=None):
    from . import _column
    f = {'workspace_id':workspace_id}
    if group_id:
        f['group_id'] = group_id
    groups = db.read('Group',['group_id','name'],f)
    bases = []
    for group in groups:
        all_bases = db.read(
            'GroupBase',
            ['group_id','platform_id','mapping','mapping_seq','base_dimension_id'],
            {'group_id':group['group_id']}
            )
        for base in all_bases:
            base.update(group)
            base['mapping'] = _mapping_to_ui(base['mapping'], base.pop('mapping_seq'))
            base['base_dimension_id'] = _column.workspace_api_inverse(base['base_dimension_id'], workspace_id)
            bases.append(base)
    return bases



    
