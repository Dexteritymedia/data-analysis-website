import io

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, View, ListView, UpdateView, DeleteView, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import Http404

from .forms import FileForm, SignUpForm
from .models import File

import pandas as pd
import pygwalker as pyg

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)

        return super(RegisterView, self).form_valid(form)


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f"Welcome {username}!!!")
            return redirect("home")
        else:
            messages.info(request, f"Account does not exist please sign up or check your account details")
    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_page(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")

def homepage(request):
    if request.user.is_authenticated:
        files = File.objects.filter(user=request.user).order_by('-uploaded_at')
        #files = File.objects.all()
        return render(request, 'homepage.html', {'files': files,})
    else:
        return redirect('login')

    
def data_analysis(request, file, slug):
    if request.user.is_authenticated:
        file = get_object_or_404(File, id=file, slug=slug)
        print(file.id)
        if file.user != request.user:
            raise Http404
        all_users_files = File.objects.filter(user=request.user).exclude(id=file.id).order_by('-uploaded_at')
        data = file.file.path
        df = pd.read_csv(data)
        print(df)
        data_analysis = mark_safe(pyg.to_html(df))
    return render(request, 'analysis_page.html', {'users_files':all_users_files, 'data_analysis': data_analysis})



class FileUpload(LoginRequiredMixin, View):
    template_name = 'upload_csv_file.html'
    form_class = FileForm

    def get(self, request):
        form = self.form_class(request.GET)

        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = File()
            file.file_description = form.cleaned_data.get('file_description')
            file.file = form.cleaned_data.get('file')
            file.user = request.user
            file.save()
            return redirect('data-analysis', file.id, file.slug)

        context = {'form': form}
        return render(request, self.template_name, context)


@login_required
def file_form_upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FileForm()
    return render(request, 'upload_csv_file.html', {
        'form': form
    })



class CsvUploader(TemplateView):
    template_name = 'campaign/csv_uploader.html'

    def post(self, request):
        context = {
            'messages':[]
        }

        csv = request.FILES['csv']
        csv_data = pd.read_csv(
            io.StringIO(
                csv.read().decode("utf-8")
            )
        )

        """
        Make sure the headings in the csv file correspond with
        the model field name i.e name is name while Name isn't the
        same with name an error will occur
        """

        for record in csv_data.to_dict(orient="records"):
            try:
                AdCopy.objects.create(
                    name = record['name'],
                    email = record['email'],
                    product = record['product'],
                    ad_copy = record['ad_copy'],
                    description = record['description']
                )
                #return HttpResponse("Csv file successfully Uploaded")
                context['success'] = "Csv file successfully Uploaded"

            except Exception as e:
                context['exceptions_raised'] = e
                print(context['exceptions_raised'])
                
        return render(request, self.template_name, context)


"""
def chatbot_page(request, session_id):
    #check if user is authenticated
    if request.user.is_authenticated:
        session = get_object_or_404(ChatBotSession, id=session_id)
        if session.user != request.user:
            raise Http404

        if request.method == 'POST':
            #get user input from the form
            user_input = request.POST.get('userInput')
            tone = request.POST.get('tone')
            language = request.POST.get('language')
            bot_response = generate_ai_response(tone, language, user_input)
            #bot_response = generate_ai_response(user_input)

            chatbot = ChatBot.objects.get_or_create(
                chat_session=session,
                message=user_input,
                bot_response=bot_response,
                feedback=False,
                date=timezone.now(),
            )
            return redirect(request.META['HTTP_REFERER'])
        else:
            #retrieve all messages belong to logged in user
            get_history = ChatBot.objects.filter(chat_session=session).order_by('-id')
            context = {'session':session, 'get_history':get_history}
            return render(request, 'index.html', context)
    else:
        return redirect("home")


def post(self, request):
    form = DetailForm(request.POST, request.FILES, initial={'user': request.user.id})
    if form.is_valid():
        form.save()
        return redirect('user')


    context = {'form': form}
    return render(request, self.template_name, context)
"""
