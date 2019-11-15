from django.shortcuts import render, get_object_or_404
from .models import Announcement


def AnnouncementListView(request):
    announcements = Announcement.objects.all()
    context = {
        'announcements': announcements
    }
    return render(request, 'announcement/announcements.html', context)


def AnnouncementDetailView(request, id):

    announcement = get_object_or_404(Announcement, id=id)
    context = {
        'announcement': announcement,
    }

    return render(request, 'announcement/announcement_details.html', context)
