from django.urls import path
from .views import EmailView, QuoteView

app_name = 'contact'

urlpatterns = [
    path('email/', EmailView.as_view(), name='email'),
    path('request-quote/', QuoteView.as_view(), name='quote'),
]
