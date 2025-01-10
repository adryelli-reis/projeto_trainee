from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configuração do amviente do Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_trainee.settings')

# Instância do Celery
app = Celery('projeto_trainee')

# Usa o sistema de condifugração do Django para carregar configurações do Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carrega as tarefas de todos os apps Djangos configuradores
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')