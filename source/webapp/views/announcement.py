from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.http import urlencode
from django.db.models import Q

from webapp.forms import SimpleSearchForm, AnnouncementForm
from webapp.models import Announcement


class IndexView(ListView):
    model = Announcement
    template_name = "announcement/index.html"
    context_object_name = "announcements"
    ordering = "id"
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            title_out = Announcement.objects.filter(Q(title__icontains=self.search_value))
            description_out = Announcement.objects.filter(Q(description__icontains=self.search_value))
            if title_out:
                return title_out.filter(status__exact='published')
            elif description_out:
                return description_out.filter(status__exact='published')
        return Announcement.objects.filter(status__exact='published').order_by("-created_at")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form

        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class AnnouncementView(DetailView):
    template_name = 'announcement/detail.html'
    model = Announcement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        announcement = self.object
        comments = announcement.comments_anc.order_by('-created_at')
        context['comments'] = comments
        return context


class CreateAnnouncementView(LoginRequiredMixin, CreateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:announcement_view', kwargs={'pk': self.object.pk})


class UpdateAnnouncementView(PermissionRequiredMixin, UpdateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement/update.html'
    permission_required = 'webapp.change_announcement'

    def has_permission(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('webapp:announcement_view', kwargs={'pk': self.object.pk})


class DeleteAnnouncementView(PermissionRequiredMixin, DeleteView):
    model = Announcement
    context_object_name = 'announcement'
    template_name = 'announcement/delete.html'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_announcement'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        announcement = get_object_or_404(Announcement, pk=pk)
        announcement.status = "for deletion"
        announcement.save()
        return announcement

    def has_permission(self):
        return self.get_object().author == self.request.user
