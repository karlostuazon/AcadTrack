from django.shortcuts import render, redirect 
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm
from .forms import CreateUserForm

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django import template
from django.template.loader import get_template 
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    # Sends successfully logged in user to main task page 
    def get_success_url(self):
        return reverse_lazy('tasks')

#--INDEX FOR EMAIL--
def index(request):
    return render(request, 'templates/base/index.html', {'title':'index'})

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = CreateUserForm 
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        htmly = get_template('base/email_template.html')
        d = { 'username': username }
        subject, from_email, to = 'Welcome to AcadTrack!', 'your_email@gmail.com', email
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    # Does not allow logged in registered user to go to register page
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


# Class based view already looks for task_list.html template for us; Same with other class based views
class TaskList(LoginRequiredMixin, ListView):
    model = Task    
    # Changes the 'object_list' query set name to 'tasks'
    context_object_name = 'tasks'

    # Ensures the user only gets their own data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search_input'] = search_input
        
        return context

class TaskListAssignment(LoginRequiredMixin, ListView):
    model = Task    
    # Changes the 'object_list' query set name to 'tasks'
    context_object_name = 'tasks'

    # Ensures the user only gets their own data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user, category="Assignment")
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search_input'] = search_input
        
        return context

class TaskListExam(LoginRequiredMixin, ListView):
    model = Task    
    # Changes the 'object_list' query set name to 'tasks'
    context_object_name = 'tasks'

    # Ensures the user only gets their own data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user, category="Exam")
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search_input'] = search_input
        
        return context

class TaskListQuiz(LoginRequiredMixin, ListView):
    model = Task    
    # Changes the 'object_list' query set name to 'tasks'
    context_object_name = 'tasks'

    # Ensures the user only gets their own data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user, category="Quiz")
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search_input'] = search_input
        
        return context

class TaskListProject(LoginRequiredMixin, ListView):
    model = Task    
    # Changes the 'object_list' query set name to 'tasks'
    context_object_name = 'tasks'

    # Ensures the user only gets their own data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user, category="Project")
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search_input'] = search_input
        
        return context

class TaskListOther(LoginRequiredMixin, ListView):
    model = Task    
    # Changes the 'object_list' query set name to 'tasks'
    context_object_name = 'tasks'

    # Ensures the user only gets their own data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user, category="Other")
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search_input'] = search_input
        
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    #Allows you to change 'task_detail' to just 'task' for template name 
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task 
    context_object_name = 'task'
    fields = ['title', 'category', 'subject', 'description', 'files', 'due', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView, ListView):
    model = Task
    context_object_name = 'task'
    fields = ['title', 'complete', 'category', 'subject', 'description', 'files', 'due']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))

