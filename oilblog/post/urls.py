from django.urls import path
from .views import IndexView,index
app_name = 'post'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('', index, name='index')
]
