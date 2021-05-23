from django import forms
from .models import Tutorial
# from taggit.forms import TagField, TagWidget

class VideoForm(forms.ModelForm):
    # tags = TagField()
    class Meta:
        model = Tutorial
        fields = ['title', 'desc', 'tags', 'video_link', 'department']
        # widgets = {
        #     'tags': TagWidget(),
        # }
        # fields = ['title', 'desc', 'video_link', 'department']