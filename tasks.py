from typing import Optional
from celery import Celery, Task, shared_task
from flask import Flask
from library import Library

def init_tasks(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

@shared_task(ignore_result=False)
def ingest(
    tenant_id: str,
    author: Optional[str],
    subject: Optional[str]
):
    lib = Library(tenant_id=tenant_id)
    return lib.ingest(author=author, subject=subject)