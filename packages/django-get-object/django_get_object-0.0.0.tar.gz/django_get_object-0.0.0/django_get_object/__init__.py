def get_object(model,**kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        pass
