from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostListView(ListView):
    model = post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date']
    paginate_by=5

class UserPostListView(ListView):
    model = post
    template_name='blog/user_posts.html'
    context_object_name='posts'
    ordering=['-date']
    paginate_by=5

    def get_queryset(self):
        user= get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date')



class PostDetailView(DetailView):
    model = post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin,LoginRequiredMixin, UpdateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        post=self.get_object()
        if(self.request.user==post.author):
            return True
        return False

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin,DeleteView):
    model = post
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if(self.request.user==post.author):
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})
