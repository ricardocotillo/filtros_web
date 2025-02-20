from django.urls import path
from .views import EmailView

app_name = 'contact'

urlpatterns = [
    path('email/', EmailView.as_view(), name='email'),
]
