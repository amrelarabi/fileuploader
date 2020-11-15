from sqlite3 import IntegrityError
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from uploader.forms import *
from django.urls import reverse_lazy
from django.views import generic
from .forms import MemberCreationForm
from .models import File
from django.conf import settings
from django.http import HttpResponse, Http404


@login_required
def dashboard(request):
    return render(request, 'uploader/dashboard.html')


class Myfiles(ListView):
    template_name = 'uploader/my_files.html'

    def get_queryset(self):
        return File.objects.filter(author=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Myfiles, self).dispatch(request, *args, **kwargs)


@login_required
def download_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, file.file.path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    if file.author == request.user:
        file.delete()
        return redirect('my_files')
    else:
        messages.add_message(request, messages.ERROR, 'You are not allowed to delete this file')
        return redirect('my_files')


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.author = request.user
            form.save()
            messages.add_message(request, messages.SUCCESS, 'File uploaded successfully')
            return redirect('my_files')
        else:
            messages.add_message(request, messages.ERROR, 'Your request could not be completed')

    if request.method == 'GET':
        form = FileForm()
        context = {
            'form': form
        }
        return render(request, 'uploader/upload_file.html', context=context)


class SignUp(generic.CreateView):
    form_class = MemberCreationForm
    success_url = reverse_lazy('login')
    template_name = 'uploader/signup.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        messages.add_message(self.request, messages.SUCCESS, 'You have successfully signed up')
        return super().form_valid(form)


def login_view(request):
    if request.method == 'GET':
        form = MemberLoginForm()
        context = {'form': form}
        return render(request, 'uploader/login.html', context=context)
    if request.method == 'POST':
        form = MemberLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.add_message(request, messages.ERROR, 'Email address or password is incorrect')
                return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, 'Your request could not be completed')
            return redirect('login')


@login_required
def edit_account(request):
    if request.method == 'GET':
        form_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = EditProfileForm(form_data)
        context = {'form': form}
        return render(request, 'uploader/edit_account.html', context=context)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = get_object_or_404(Member, pk=request.user.id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            if request.FILES:
                if user.avatar:
                    user.avatar.delete()
                user.avatar = request.FILES['avatar']
            user.save()

            messages.add_message(request, messages.SUCCESS, 'Your account was updated successfully')

            return redirect('edit_account')
        else:
            messages.add_message(request, messages.ERROR, 'Your request could not be completed')
            return redirect('edit_account')


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")
