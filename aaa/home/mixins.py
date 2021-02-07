from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import bleach
from django.contrib import messages
from .models import *
from accounts.models import Profile,User,ProfileDetail, Work, Degree, MedicalCollege
from home.models import PostLink, Tag



class GeneralContextMixin:
    def get_context_data(self, **kwargs):
        context ={}
        context['tag_speciality'] = list(Tag.objects.filter(is_speciality=True))

        return context

class ValidateLinkMixin:
    def clean_links(self):
        new_name = []
        new_links = []
        name = self.request.POST.getlist('link_name')
        url = self.request.POST.getlist('link')
        if len(name) != len(url):
            return False
        validator = URLValidator()
        if url:
            for i in url:
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
                    return False
        if name:
            for i in name:
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
        newdic['linkobj'] = []
        for i in new_tuple:
            try:
                newdic['linkobj'].append(PostLink.objects.create(link_name=i[0], link= i[1] ))
            except Exception as e:
                pass
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
        valid_extensions = ['jpeg', 'png', 'jpg', 'pdf', 'docx', 'pptx', 'JPG', 'JPEG', 'PNG']
        newdict={}
        if imagelist:
            for i in imagelist:
                img = self.request.FILES.get(i)
                if not img:
                    messages.error(self.request, '{0} not entered'.format(img))
                    continue
                print(img.name.split('.'))
                if len(img.name.split('.')) > 2:
                    messages.error(self.request, 'enter valid file')
                    continue
                else:
                    if (img.name.split('.')[1]).lower() in valid_extensions:
                        print((img.name.split('.')[1]).lower() )
                        print('yes file has valid extension')
                        if self.validate_image_size(img):
                            newdict[i] = img
                        else:
                            messages.error(self.request, 'file size greater than 25mb')
                            continue
                    else:
                        messages.error(self.request, 'enter valid file with valid extension')
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




class DetailFormMixin:
    def save_detail_prof_form(self):
        a = self.myprofile.list_heading()
        heading = {}
        for head in a:
            try:
                heading['value'] = bleach.clean(self.request.POST.get(head), strip=True)
                heading['name']=head
            except:
                continue

        if heading['value'] and heading['name']:
            detobj = self.myprofile.get_details()
            for detail in detobj:
                if detail.heading == heading['name']:
                    detail.details = heading['value']
                    detail.save()
                else:
                    continue
            self.myprofile.save()

        else:
            messages.error(self.request, 'kindly fill the text field of form')
            return False


class WorkFormMixin:
    def save_work_form(self):
        position = bleach.clean(self.request.POST.get('position'), strip=True)
        hospital = bleach.clean(self.request.POST.get('hospital'), strip=True)
        if position and hospital:
            try:
                hospobj = MedicalCollege.objects.get(name=hospital)
                try:
                    workobj = Work.objects.get(position=position, hospital=hospobj, is_current=True)
                except:
                    workobj = Work.objects.create(position=position, hospital=hospobj, is_current=True)
                try:
                    self.myprofile.work.add(workobj)
                    self.myprofile.save()
                except:
                    return workobj
            except:
                hospobj = MedicalCollege.objects.create(name=hospital)
                workobj = Work.objects.create(position=position, hospital=hospobj, is_current=True)
                try:
                    self.myprofile.work.add(workobj)
                    self.myprofile.save()
                except:
                    return workobj
            return True

        else:
            messages.error(self.request, 'kindly fill the Hospital name or position in form')
            return False




class DegreeFormMixin:
    def save_degree_form(self):
        degreetag = self.request.POST.getlist('degreetag')
        college = self.request.POST.getlist('college')
        mname=[]
        taglist = []
        for i in degreetag:
            try:
                myTag = Tag.objects.get(name=i, is_degree=True)
                taglist.append(myTag)

            except:
                messages.error(self.request, 'Kindly enter valid tag')
                return False
        for i in college:
            i1 = bleach.clean(i, strip=True)
            if i1:
                try:
                    mypersonal = MedicalCollege.objects.get(name=i1)
                    mname.append(mypersonal)
                except:
                    mypersonal = MedicalCollege.objects.create(name=i1)
                    mypersonal.save()
                    mname.append(mypersonal)
            else:
                messages.error(self.request, 'kindly fill the medical college name form' )
                return False


        if len(mname)!=len(taglist):
            messages.error(self.request, 'kindly fill both the college name and qualification')
            return False
        new_tuple = list(zip(taglist, mname))
        print(new_tuple)
        degreelist = []
        for i in new_tuple:

            try:
                degreeobj = Degree.objects.get(name=i[0], college=i[1])
            except:
                degreeobj = Degree.objects.create( name=i[0], college=i[1])
                degreeobj.save()
            try:
                self.myprofile.degree.add(degreeobj)
                self.myprofile.save()
            except:
                degreelist.append(degreeobj)

        if degreelist:
            return degreelist
        else:
            return True





class PersonalFormMixin(ValidateFileMixin):
    def validate_personal_form(self, name, nationality, imagelist):
        if name:
            new_name = bleach.clean(name, strip=True)
        if nationality:
            new_nation = bleach.clean(nationality, strip=True)
        imagedict = self.clean_file(imagelist)

        new_dic = {}
        new_dic['name']=new_name
        new_dic['nationality']=new_nation
        print(imagedict)
        try:
            new_dic['profilepic'] = imagedict['profileimage']
            new_dic['backgroundpic'] = imagedict['backgroundimage']
        except:
            pass

        return new_dic
    def save_personal_form(self):

        name = self.request.POST.get('name')

        nationality = self.request.POST.get('nationality')
        if name and nationality:
            personaldic = self.validate_personal_form(name, nationality, ['profileimage', 'backgroundimage'])
        else:
            messages.error(self.request, 'kindly enter both the fields')
            return False



        try:
            a = self.myprofile
            a.name = personaldic.get('name')
            a.nationality = personaldic.get('nationality')
            try:
                if personaldic.get('profilepic'):
                    a.profilepic = personaldic.get('profilepic')
                if personaldic.get('backgroundpic'):
                    a.backgroundpic = personaldic.get('backgroundpic')
            except:
                pass
            a.save()
        except:
            pass

        return True

class ContactFormMixin:
    def validate_contact_form(self, name, url, phone):
        new_name = []
        new_links = []
        if phone:
            try:
                int(phone)
            except ValueError:
                messages.error(self.request, 'kindly enter only numbers in phone number')
                return False
        else:
            print('no phone no entered')
        validator = URLValidator()
        if url:
            for i in url:
                if i:
                    try:
                        validator(i)
                        new_links.append(i)
                    except ValidationError:
                        print('url not valid')
                        messages.error(self.request, 'Kindly enter valid Url ')
                        return True
                else:
                    print('no url entered')
        if name:
            for i in name:
                if i:
                    bleach.clean(i, strip=True)
                    new_name.append(i)
                else:
                    i = 'link address'
                    new_name.append(i)

        new_tuple = list(zip(new_name, new_links))
        newdic = {}
        newdic['links'] = new_tuple
        newdic['phone'] = phone
        print(newdic)
        return newdic
    def save_contact_form(self):

        linkName = self.request.POST.getlist('link_name')
        linkUrl = self.request.POST.getlist('link')
        if len(linkName) != len(linkUrl):
            messages.error(self.request, 'kindly enter name or url')
            return False
        phone = self.request.POST.get('phone')
        contactdic = self.validate_contact_form(linkName, linkUrl, phone)
        try:
            if contactdic.get('links'):
                self.myprofile.links.clear()
                for i in contactdic.get('links'):
                    try:
                        PostLink.objects.filter(link=i[1], link_name=i[0]).delete()
                    except:
                        pass
                    a = PostLink.objects.create(user=self.request.user, link=i[1], link_name=i[0])
                    self.myprofile.links.add(a)
                    self.myprofile.save()
            else:
                pass
            if contactdic.get('phone'):
                self.myprofile.phone = contactdic.get('phone')
                self.myprofile.save()
            else:
                pass
        except:
            pass
        return True
