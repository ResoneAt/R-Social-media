from django.shortcuts import render
from django.views.generic import View
from posts.models import PostModel, LikeModel
from .forms import SearchForm
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
# Create your views here.


class HomePageView(LoginRequiredMixin, View):
    def get(self, request):
        posts = PostModel.objects.all().order_by('-created_at')

        liked_posts = LikeModel.objects.filter(user=request.user, post__in=posts)
        liked_post_ids = liked_posts.values_list('post_id', flat=True)
        for post in posts:
            post.is_like = post.id in liked_post_ids

        if request.GET.get('search'):
            post = post.filter(body__icontains=request.GET['search'])
        search = SearchForm

        context = {
            'post': posts,
            'search_form': search
        }
        return render(request, 'core/home.html', context)
