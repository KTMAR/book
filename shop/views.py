from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from shop.models import Writer, Book, Genre, MediaType, Customer
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login


class MainView(View):

    def get(self, request, *args, **kwargs):
        book = Book.objects.all()
        writer = Writer.objects.all()

        context = {
            'books': book,
            'writers': writer,
        }
        return render(request, 'main_page1.html', context)


class SearchResultsView(ListView):
    model = Book
    template_name = 'search.html'

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(name__icontains=query) | Q(writer__name__icontains=query)

        )
        return object_list


class LoginView(View):
    """Инстациируем форму"""

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,

        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        # если че то не получилось при авторизации(не валидна)
        context = {
            'form': form,
        }
        return render(request, 'login.html', context)


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,

        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            """Что бы присвоить пассворд,нужно сначала сохранить юзера(new_user),а потом уже задать ему пароль"""
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            """Затем создаем покупателя"""
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            """Залогиним юзера"""
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)
