from django.urls import path

from webapp.views import IndexView, AnnouncementView, CommentDeleteView, UpdateAnnouncementView, DeleteAnnouncementView, \
    CreateAnnouncementView, CommentCreateView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('announcement/<int:pk>/', AnnouncementView.as_view(), name='announcement_view'),
    path('announcement/<int:pk>/update/', UpdateAnnouncementView.as_view(), name="announcement_update"),
    path('announcement/<int:pk>/delete/', DeleteAnnouncementView.as_view(), name="announcement_delete"),
    path('announcement/add/', CreateAnnouncementView.as_view(), name="announcement_create"),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),
    path('announcement/<int:pk>/add_comment', CommentCreateView.as_view(), name='comment_create'),
]
