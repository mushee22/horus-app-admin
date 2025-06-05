from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.db.models import FileField
from utils.file_cleanup import delete_file

def get_file_fields(model):
    """
    Returns a list of FileField instances from the model.
    """
    return [f.name for f in model._meta.get_fields() if isinstance(f, FileField)]

@receiver(pre_save)
def auto_delete_old_files_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return  
    for field_name in get_file_fields(sender):
        old_file = getattr(old_instance, field_name)
        new_file = getattr(instance, field_name)
        if old_file and new_file and old_file != new_file:
            delete_file(old_file)

@receiver(pre_delete)
def auto_delete_files_on_delete(sender, instance, **kwargs):
    for field_name in get_file_fields(sender):
        field_file = getattr(instance, field_name)
        if field_file:
            delete_file(field_file)            