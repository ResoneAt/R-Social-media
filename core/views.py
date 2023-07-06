from django.shortcuts import render
from django.views.generic import View
from posts.models import PostModel
from .forms import SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class HomePageView(LoginRequiredMixin, View):
    def get(self, request):
        post = PostModel.objects.all().order_by('-created_at')
        if request.GET.get('search'):
            post = post.filter(body__icontains=request.GET['search'])
        search = SearchForm
        return render(request, 'core/home.html',
                      {'post': post,
                       'search_form': search})
