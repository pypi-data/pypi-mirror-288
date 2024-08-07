from . import errors

def _get_model(model):
    from . import models
    return getattr(models, model)

def read(model, fields, filters=None):
    _model = _get_model(model)
    if not filters:
        return [{f:getattr(k,f) for f in fields}  for k in _model.objects.all()]
    elif filters:
        return [{f:getattr(k,f) for f in fields}  for k in _model.objects.filter(**filters).all()]

def read_single_row(model, fields, filters=None):
    _model = _get_model(model)
    try:
        k = _model.objects.get(**filters)
        return {f:getattr(k,f) for f in fields}
    except _model.DoesNotExist:
        raise errors.NoRowFound
    except _model.MultipleObjectsReturned:
        raise errors.MultipleRowsFound

def create(model, field_values):
    from django.db import IntegrityError
    _model = _get_model(model)
    try:
        return str(_model.objects.create(**field_values).pk)
    except IntegrityError as e:
        raise errors.get_violation_type(e.__cause__)
        

def delete(model, filters):
    _model = _get_model(model)
    _model.objects.filter(**filters).all().delete()

def update(model, filters, update_values):
    from django.db import IntegrityError
    _model = _get_model(model)
    # print(_model._meta.pk.column)
    try:
        _model.objects.filter(**filters).update(**update_values)
    except IntegrityError as e:
        raise errors.get_violation_type(e.__cause__)
    
def read_single_row_by_pk(model, pk_value, fields):
    _model = _get_model(model)
    try:
        k = _model.objects.get(pk=pk_value)
        return {f:getattr(k,f) for f in fields}
    except _model.DoesNotExist:
        raise errors.NoRowFound
