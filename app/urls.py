from django.urls import path


from app.views import LoginClassView, RegisterView, HomeView, LogoutView

urlpatterns = [
    path('accounts/login/', LoginClassView.as_view(), name="login"),
    path('accounts/register/', RegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),  
    path('', HomeView.as_view(), name="home"),
]