# tasks.py
from celery import shared_task
from django.core.files import File
from django.core.files.storage import default_storage
from web.models import SubChapters
from .models import BackgroundTaskStatus
import os

@shared_task
def upload_subchapter_video_to_s3(subchapter_id, temp_path, background_task_id=None):
    try:
        print(f"Starting upload for subchapter ID: {subchapter_id} from {temp_path}")
        subchapter = SubChapters.objects.get(id=subchapter_id)
        task = BackgroundTaskStatus.objects.get(id=background_task_id) if background_task_id else None

        with default_storage.open(temp_path, 'rb') as f:
            django_file = File(f)
            filename = os.path.basename(temp_path)
            subchapter.video.save(filename, django_file, save=True)

        subchapter.save()
        default_storage.delete(temp_path)

        if task:
            task.status = 'completed'
            task.save()
            print(f"Upload completed for subchapter ID: {subchapter_id}")
        

    except Exception as e:
        # Optional: log error, mark failure
        if task:
            task.status = 'failed'
            task.save()
        else:
            print(f"Error uploading video for subchapter ID {subchapter_id}: {e}")
        
        print(f"Upload failed: {e}")
