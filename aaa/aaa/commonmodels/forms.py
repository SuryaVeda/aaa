from django.forms import ModelForm
from .mixins import ValidateFileMixin, ValidateLinkMixin, ValidateTextMixin, ValidateDetailsMixin
from .models import *
from django.contrib import messages


class CreatePostForm(ModelForm, ValidateTextMixin, ValidateLinkMixin, ValidateFileMixin,ValidateDetailsMixin):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = Post
        fields = []

    def save(self, commit=True):
        post_heading = self.clean_text(['post_heading'])
        if not post_heading['post_heading']:
            messages.error(self.request, 'Kindly enter heading', extra_tags=self.request.user.email)
            return False

        saveobj = Post.objects.create(user = self.request.user, post_heading= post_heading['post_heading'])
        print(saveobj.post_heading)
        print(saveobj.pk)
        post_details = self.clean_details()
        print(post_details)
        if post_details:
            for i in post_details['details']:
                try:
                    x = Details.objects.create(detail_heading=i[0], text=i[1])
                    saveobj.post_details.add(x)
                except:
                    messages.error(self.request, 'Unable to save post details', extra_tags=self.request.user.email)

        post_links = self.clean_links()
        if post_links:
            for i in post_links['links']:
                try:
                    x = PostLink.objects.create(link_name=i[0], link=i[1])
                    saveobj.post_links.add(x)
                except:
                    messages.error(self.request, 'Unable to save post details', extra_tags=self.request.user.email)

        post_files = self.clean_file(['image', 'pdf'])
        for img in post_files['image']:
            if img:
                x = FileAdd.objects.create(file=img, is_image = True)
                saveobj.post_files.add(x)
        for file in post_files['pdf']:
            if file:
                x = FileAdd.objects.create(file=file)
                saveobj.post_files.add(x)
        try:
            post_tags = [Tag.objects.get(tag_name = i) for i in list(self.request.POST.get('tags'))]
            [saveobj.post_tags.add(i) for i in post_tags]
        except:
            messages.error(self.request, 'error in saving tags', extra_tags=self.request.user.email)
        saveobj.save()
        return saveobj