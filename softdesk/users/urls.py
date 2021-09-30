from django.conf.urls import url
from .views import CreateUserAPIView, authenticate_user

urlpatterns = [
    url('signup/', CreateUserAPIView.as_view()),
    url('login/', authenticate_user),
]
