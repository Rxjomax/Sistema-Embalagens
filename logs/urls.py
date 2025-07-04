# Ficheiro: logs/urls.py

from django.urls import path
from .views import LogEntryListView

app_name = 'logs'

urlpatterns = [
    path('', LogEntryListView.as_view(), name='log_list'),
]