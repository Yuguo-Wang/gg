from django.urls import path, include

from . import views

urlpatterns = [
    path('request/', views.make_request, name='make-ride-request'),
    path('my-rides/<str:mode>', views.display_my_rides, name='show-my-rides'),
    path('edit-request/<int:ride_id>', views.edit_request, name='edit-ride'),
    path('detail/<int:ride_id>/<str:mode>/<int:share_ride_id>/<str:back_url>', views.view_ride, name='view-ride'),
    path('open-for-driver/', views.open_rides_drive, name='open-rides-drive'),
    path('open-for-sharer/', views.open_rides_share, name='open-rides-share'),
    path('drive-ride/<int:ride_id>', views.drive_ride, name='drive-ride'),
    path('share-ride/<int:ride_id>/<int:share_ride_id>', views.share_ride, name='share-ride'),
    path('complete-ride/<int:ride_id>', views.complete_ride, name='complete-ride'),
    path('quit-ride/<int:ride_id>', views.quit_ride, name='quit-ride'),
]