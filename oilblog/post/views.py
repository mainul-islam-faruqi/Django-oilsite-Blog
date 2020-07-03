from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from django.shortcuts import (render,
                                get_object_or_404,
                                redirect,
                                reverse,
                                Http404)


from django.core.paginator import Paginator 
from .models import Post, Category, Comment, Author
# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'


def index(request):
    posts = Post.objects.all()
    recent = Post.objects.order_by('-timestamp')[0:30]
    # category = Category.objects.all()

    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'object_list': posts,
        'recent':recent,
        # 'category': category,
    }

    return render(request,
                  'index.html',
                  context)

class PostDetailView(DetailView):
    template_name = 'posts/post-detail.html'
    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = Post.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Post doesn't exist")
        return instance
