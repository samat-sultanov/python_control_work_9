from django import forms
from django.forms import widgets

from webapp.models import Announcement, Comment


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Search',
                             widget=widgets.TextInput(attrs={'class': "form-control w-25"}))


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['picture', 'title', 'description', 'category', 'price']


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
