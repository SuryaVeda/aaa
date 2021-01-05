from django.urls import path
from . import views
app_name = 'mcq'

urlpatterns = [

path('', views.McqView.as_view(), name = 'qa'),
path('<str:pk>', views.McqView.as_view(), name='subjectquestions'),
path('refreshquestions', views.refresh_questions_view, name='refreshq'),
path('createquestions/<str:type>', views.CreateQuestion.as_view(), name='createq'),
path('getnewquestions/<str:index>', views.GetQuestions.as_view(), name='getq'),
path('deletequestions/<int:pk>', views.delete_question_view, name = 'deleteq'),
path('question/<int:qpk>', views.QuestionDetail.as_view(), name = 'qdetail'),
]
