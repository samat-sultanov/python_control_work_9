from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DeleteView, CreateView
from django.urls import reverse

from webapp.forms import UserCommentForm
from webapp.models import Comment, Announcement


class CommentDeleteView(DeleteView):
    model = Comment

    def has_perm(self):
        return self.get_object().author == self.request.user

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:announcement_view', kwargs={'pk': self.object.announcement.pk})


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = UserCommentForm
    model = Comment
    template_name = 'comment/create.html'

    def form_valid(self, form):
        announcement = get_object_or_404(Announcement, pk=self.kwargs.get('pk'))
        if self.request.user != announcement.author:
            author = self.request.user
            form.instance.author = author
            form.instance.announcement = announcement
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:announcement_view', kwargs={'pk': self.object.announcement.pk})
