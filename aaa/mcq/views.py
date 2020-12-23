from django.shortcuts import render,redirect
from django.views.generic import TemplateView, CreateView
from django.views import View
from .models import Qimage, QuestionBank
from .forms import QuestionBankForm
from django.http import JsonResponse
import json
from django.http import HttpResponse
# Create your views here.
from django.contrib import messages
from home.models import Tag

class McqView(TemplateView):
    template_name = 'mcq/basepage.html'
    questionbank = {i.pk:i.get_questions for i in Tag.objects.all().prefetch_related()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if kwargs['pk']:
                pk = int(kwargs['pk'])

                tag = Tag.objects.get(pk=int(pk))
                context['tag'] = tag

                context['questionbank'] = list(McqView.questionbank[pk].filter(mcq=True))[0:15]
                context['flashcards'] = list(McqView.questionbank[pk].filter(flashcard=True))[0:15]
                context['cases'] = list(McqView.questionbank[pk].filter(qa=True))[0:15]

        except:
            print('some error')
            context['general'] = True

        context['tag_speciality'] = Tag.objects.filter(is_speciality=True)
        return context



def refresh_questions_view():
    McqView.questionbank = {i.pk:i.get_questions for i in Tag.objects.all().prefetch_related()}
    return redirect('/home/{0}'.format('NEET SS'))


def delete_question_view(request,pk):
    x = refresh_questions_view()
    if pk and request.user.is_authenticated:
        try:
            x = QuestionBank.objects.get(pk = pk)
            if x.user == request.user or request.user.is_admin:
                x.delete()
                x = refresh_questions_view()
                print(x.status_code)
                return JsonResponse({'success': x.url}, safe=False)
            else:
                messages.error(request, 'not a valid user', extra_tags=request.user.email)

                print(x.status_code)
                return JsonResponse({"success": x.url}, safe=False)
        except:
            messages.error(request, 'post is not present in database', extra_tags=request.user.email)
            return JsonResponse({"success": x.url}, safe=False)
    else:
        messages.error(request, 'select valid post', extra_tags=request.user.email)

        return JsonResponse({"success": x.url}, safe=False)


class GetQuestions(View):

    def get(self, request, *args, **kwargs):
        print('get request')
        if request.GET.get('type') and request.GET.get('tag'):
            if request.GET.get('type')=='mcq':
                print('i am here')
                posts = list(McqView.questionbank[int(request.GET.get('tag'))].filter(mcq=True))
                index = kwargs['index']
                try:
                    index = int(index)
                except:
                    print('enter integer')
                    return redirect('mcq:qa')
                newposts = posts[index:index + 15]
                print(newposts)

                html = [((render(self.request, 'home/getquestions.html',
                                 {'user': self.request.user, 'post': i})).content).decode('utf-8') for i in newposts]
                print(html)

                return JsonResponse(html, safe=False)
            if request.GET.get('type') == 'flashcard':
                print('i am here')
                posts = list(McqView.questionbank[int(request.GET.get('tag'))].filter(flashcard=True))
                index = kwargs['index']
                try:
                    index = int(index)
                except:
                    print('enter integer')
                    return redirect('mcq:qa')
                newposts = posts[index:index + 15]
                print(newposts)

                html = [((render(self.request, 'home/getquestions.html',
                                 {'user': self.request.user, 'post': i})).content).decode('utf-8') for i in newposts]
                print(len(html))
                return JsonResponse(html, safe=False)
        else:
            print(request.GET.get('tag'))
            return redirect('home:home')


class CreateQuestion(CreateView):
    template_name = 'mcq/qbankform.html'
    form_class = QuestionBankForm
    success_url = '/mcq/refreshquestions'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request)
        kwargs.update(self.kwargs)
        print(kwargs)
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        k = self.get_form_kwargs()
        context['type'] = k['type']
        return context
