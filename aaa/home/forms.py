from django.forms import ModelForm
from django import forms
from .models import Post, Tag, Comment


class Custommmf(forms.ModelMultipleChoiceField):
    def label_from_instance(self, tag):
        return  '%s' % tag.name

class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['tag','heading', 'img', 'content', 'pdf_name', 'pdf']

    tag = Custommmf(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['heading'].widget.attrs['placeholder'] = 'Post heading/Question/title'
        self.fields['tag'].widget.attrs['placeholder'] = 'Tags'
        self.fields['pdf_name'].widget.attrs['placeholder'] = 'name of pdf'
        self.fields['content'].widget = forms.Textarea(attrs={'rows': 4, 'cols': 15})
        self.fields['content'].widget.attrs['placeholder'] = 'Content of post/mcq/answer'



