from django.urls import path

from log.views import LogsListView

app_name = "log"

urlpatterns = [path("log", LogsListView.as_view(), name="logs-list")]
