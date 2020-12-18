from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import bleach
from django.contrib import messages
from commonmodels.models import PostLink


class ValidateLinkMixin:
    def clean_links(self):
        new_name = []
        new_links = []
        name = self.request.POST.getlist('link_name')
        url = self.request.POST.getlist('link')
        if len(name) != len(url):
            messages.error(self.request, 'kindly enter name or url')
            return False
        validator = URLValidator()
        if url:
            for i in list(url):
                if i:
                    try:
                        validator(i)
                        new_links.append(i)
                    except ValidationError:
                        print('url not valid')
                        messages.error(self.request, 'Kindly enter valid Url ')
                        return False
                else:
                    print('no url entered')
                    messages.error(self.request, 'Do not submit form with empty url field')
                    return False
        if name:
            for i in list(name):
                if i:
                    bleach.clean(i, strip=True)
                    new_name.append(i)
                else:
                    i = 'link address'
                    new_name.append(i)

        new_tuple = list(zip(new_name, new_links))
        newdic = {}
        if not new_tuple:
            return False

        newdic['links'] = new_tuple
        newdic['linkobj'] = [PostLink.objects.create(link_name = i[0], link = i[1]) for i in new_tuple]
        print(newdic)
        return newdic

class ValidateDetailsMixin:
    def clean_details(self):
        detail_heading = []
        post_text = []
        heading = self.request.POST.getlist('detail_heading')
        text = self.request.POST.getlist('text')
        if len(heading) != len(text):
            messages.error(self.request, 'kindly enter heading or text', extra_tags=self.request.user.email)
            return False
        if heading:
            for i in list(heading):
                try:
                    detail_heading.append(bleach.clean(i, strip=True))
                except:
                    detail_heading.append('')

        if list(text):
            for i in text:
                try:
                    post_text.append(bleach.clean(i, strip=True))
                except:
                    post_text.append('')
        if len(detail_heading) < 1 and detail_heading[0] == '':
            return False
        if len(post_text) < 1 and post_text[0] == '':
            return False
        new_tuple = list(zip(detail_heading, post_text))
        newdic = {}

        newdic['details'] = new_tuple
        print(newdic)
        return newdic


class ValidateTextMixin:
    def clean_text(self, namelist):
        text_dict = {}
        if namelist:

            for i in namelist:
                try:
                    text_dict[i] = bleach.clean(self.request.POST.get(i), strip=True)

                except:
                    text_dict[i] = ''
                    messages.error(self.request, 'enter valid text')
        return text_dict



class ValidateFileMixin:

    def clean_file(self, imagelist):
        valid_extensions = ['jpeg', 'png', 'jpg', 'pdf', 'docx', 'pptx']
        newdict={}
        if imagelist:
            for i in imagelist:
                newdict[i] = []
                img = self.request.FILES.getlist(i)
                print(img)
                if not img:
                    messages.error(self.request, '{0} not entered'.format(img))
                    continue

                for j in list(img):
                    print(j)

                    if len(j.name.split('.')) > 2:
                        messages.error(self.request, 'enter valid file')
                        continue
                    else:
                        if j.name.split('.')[1] in valid_extensions:
                            print('yes file has valid extension')
                            if self.validate_image_size(j):
                                newdict[i].append(j)
                            else:
                                messages.error(self.request, 'file size greater than 25mb')
                                continue
                        else:
                            messages.error(self.request, 'enter valid file')
                            continue
            return newdict




        else:
            return False

    def validate_image_size(self, a):
        if a.size / 1024 / 1024 > 25:
            messages.error(self.request, 'image size greater than 25 mb')
            return False
        else:
            return True



