from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("delete/<int:pk>/", views.delete_url, name="delete_url"),
    path("<str:short_key>/", views.redirect_url, name="redirect"),
]
