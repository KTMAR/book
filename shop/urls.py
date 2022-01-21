from django.urls import path
from shop.views import MainView, SearchResultsView, RegistrationView, LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', MainView.as_view(), name='base'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]