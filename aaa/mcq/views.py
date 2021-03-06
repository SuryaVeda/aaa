from django.shortcuts import render,redirect
from django.views.generic import TemplateView, CreateView, DetailView
from django.views import View
from .models import Qimage, QuestionBank
from .forms import QuestionBankForm
from django.http import JsonResponse
import json
from django.http import HttpResponse
# Create your views here.
from django.contrib import messages
from home.models import Tag
from home.decorators import staff_required

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
                questionbank = {i.pk:i.get_questions for i in Tag.objects.all().prefetch_related()}
                print(list(questionbank[pk].filter(flashcard=True))[0:15])
                context['questionbank'] = list(questionbank[pk].filter(mcq=True))[0:15]
                context['flashcards'] = list(questionbank[pk].filter(flashcard=True))[0:15]
                context['cases'] = list(questionbank[pk].filter(qa=True))[0:15]

        except:
            print('some error')
            context['general'] = True

        context['tag_speciality'] = Tag.objects.filter(is_speciality=True)
        return context

class QuestionDetail(TemplateView):
    template_name = 'mcq/basepage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            if kwargs['qpk']:
                pk = int(kwargs['qpk'])
                question = QuestionBank.objects.get(pk=pk)
                tag = Tag.objects.get(pk=question.get_subjects[0].pk)
                print(tag)
                context['tag'] = tag
                questionbank = {i.pk:i.get_questions for i in Tag.objects.all().prefetch_related()}
                if question.mcq:
                    context['questionbank'] = [question] + list(questionbank[pk].filter(mcq=True))[0:15]
                else:
                    context['questionbank'] = list(questionbank[pk].filter(mcq=True))[0:15]
                if question.flashcard:
                    context['flashcards'] = [question] + list(questionbank[pk].filter(flashcard=True))[0:15]
                else:
                    context['flashcards'] = list(questionbank[pk].filter(flashcard=True))[0:15]

                if question.qa:
                    context['cases'] = [question] + list(questionbank[pk].filter(qa=True))[0:15]
                else:
                    context['cases'] = list(questionbank[pk].filter(qa=True))[0:15]
        except:
            print('some error')
            context['general'] = True

        context['tag_speciality'] = Tag.objects.filter(is_speciality=True)
        return context
def refresh_questions_view():
    McqView.questionbank = {i.pk:i.get_questions for i in Tag.objects.all().prefetch_related()}
    return redirect('/home/{0}'.format('NEET-SS'))

@staff_required
def delete_question_view(request,pk):

    if request.method == 'POST':
        try:
            print(request.POST)
            redirect_url = request.POST.get('redirect_url')
            print(redirect_url)
            print('\n \n \n fuck \n \n\n')
            x = QuestionBank.objects.get(pk = pk)
            if x.user == request.user or request.user.is_admin:
                x.delete()
                return JsonResponse({'success': redirect_url}, safe=False)
            else:
                messages.error(request, 'not a valid user', extra_tags=request.user.email)
                return JsonResponse({"success": redirect_url.url}, safe=False)
        except:
            messages.error(request, 'post is not present in database', extra_tags=request.user.email)
            return JsonResponse({"success": redirect_url.url}, safe=False)
    else:
        messages.error(request, 'invalid request', extra_tags=request.user.email)

        return redirect('home:home')


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
