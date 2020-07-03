from django.urls import path
from .views import IndexView,index,PostDetailView
app_name = 'post'

urlpatterns = [
    path('post', IndexView.as_view(), name='index'),
    path('', index, name='index'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
