from django.urls import path
from . views import *
from django.contrib.auth.views import LogoutView
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    
    path('', TaskList.as_view(), name='tasks'),
    path('assignment/', TaskListAssignment.as_view(), name='tasksAssignment'),
    path('exam/', TaskListExam.as_view(), name='tasksExam'),
    path('quiz/', TaskListQuiz.as_view(), name='tasksQuiz'),
    path('project/', TaskListProject.as_view(), name='tasksProject'),
    path('other/', TaskListOther.as_view(), name='tasksOther'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),

    path('', views.index, name ='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)