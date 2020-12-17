from django.forms import ModelForm
from django.shortcuts import render,redirect
from home.mixins import ValidateLinkMixin, ValidateFileMixin
from django.contrib import messages
from home.models import PostLink
from .models import Qimage,QuestionBank
import bleach
from django.core.validators import ProhibitNullCharactersValidator

class QuestionBankForm(ModelForm,ValidateLinkMixin, ValidateFileMixin):
    def __init__(self,*args, type=None, request=None,  **kwargs):
        self.type = type
        self.request = request

        super().__init__(*args, **kwargs)
        null = ProhibitNullCharactersValidator()
        print(null)
        self.fields['question'].validators.remove(null)
        self.fields['answer'].validators.remove(null)

    def save(self, commit=True ):
        if not self.type:
            messages.error(self.request, 'Not a valid form', extra_tags=self.request.user.email)
            return redirect('mcq:qa')
        saveobj = super().save(commit=False)
        if saveobj:
            if self.request.user.is_authenticated:
                saveobj.user = self.request.user

            if not self.cleaned_data['tag']:
                print('hello')
                messages.error(self.request, 'kindly enter tag', extra_tags=self.request.user.email)
                return redirect('mcq:qa')

            print('reached before save')
            if self.type == 'mcq':
                saveobj.mcq = True
            elif self.type == 'qa':
                saveobj.qa = True
            elif self.type == 'flashcard':
                saveobj.flashcard = True
            else:
                pass
            try:
                question = bleach.clean(self.request.POST.get('question'), strip=True)
                saveobj.question = question
                answer = bleach.clean(self.request.POST.get('answer'), strip=True)
                saveobj.answer = answer
            except:
                messages.error(self.request, 'Enter question!!.', extra_tags=self.request.user.email)
                return redirect('mcq:qa')



            if commit:
                saveobj.save()
            [saveobj.tag.add(i) for i in self.cleaned_data['tag']]
            linkdict = self.clean_links()
            if linkdict:
                if linkdict['linkobj']:
                    [saveobj.links.add(i) for i in linkdict['linkobj']]

            self.save_image(saveobj)
            return saveobj
        else:
            messages.error(self.request, 'Unable to save.', extra_tags=self.request.user.email)
            return redirect('mcq:qa')

    def save_image(self, saveobj):
        filedict = self.clean_file(['qimage', 'aimage'])
        print(filedict)

        if filedict:
            if filedict['qimage']:
                try:
                    image_question = Qimage.objects.create(image=filedict['qimage'])
                    image_question.qimage = True
                    image_question.qinstance = saveobj
                    image_question.save()
                except:
                    print('unable to save image')
            if filedict['aimage']:
                try:
                    image_question = Qimage.objects.create(image=filedict['aimage'])
                    image_question.aimage = True
                    image_question.qinstance = saveobj
                    image_question.save()
                except:
                    print('unable to save image')
            return print('saved image successfully')
        else:
            return print('no file to save')

    class Meta:
        model = QuestionBank
        exclude = ['user', 'date', 'flashcard', 'qa', 'mcq']

