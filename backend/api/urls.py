from django.urls import path
from .views import SummarizeView, EmailView

urlpatterns = [
    path('summarize/', SummarizeView.as_view()),
    path('email/', EmailView.as_view()),
]
