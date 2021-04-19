from django.urls import path
from .views import TestsView, TestView


app_name = 'polls_service'


urlpatterns = [
    path('tests/<int:test_id>', TestView.as_view(), name='test'),     
    path('tests/', TestsView.as_view(), name='tests'),
]
