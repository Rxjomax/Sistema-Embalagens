# Ficheiro: logs/views.py

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import LogEntry

class LogEntryListView(LoginRequiredMixin, ListView):
    model = LogEntry
    template_name = 'logs/log_list.html'
    context_object_name = 'logs'
    paginate_by = 30  # Mostra 30 logs por página