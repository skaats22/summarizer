from django.urls import path
from .views import SummarizeView, EmailView

urlpatterns = [
    path('summarize/', SummarizeView.as_view(), name='summarize'),
    path('email/', EmailView.as_view(), name='email'),
]
