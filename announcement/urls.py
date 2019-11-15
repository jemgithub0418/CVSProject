from django.urls import path
from .views import AnnouncementListView, AnnouncementDetailView

urlpatterns = [
    path('', AnnouncementListView, name='announcements-page'),
    path('<int:id>/', AnnouncementDetailView, name='announcement-details'),
]
