from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

"""from django.http import HttpResponse
   def about(request):	 
        return HttpResponse('<h1> Blog About </h1>')

posts=[ <dummy data>
		{"author":"Captain Jack Sparrow",
		"title":"This is the tale of cjs",
		"content":"He's a jolly good fellow",
		"date_posted":"25th Feb 2021"
		},

		{"author":"Salazar",
		"title":"bla bla bla bla",
		"content":"lorem ipsum",
		"date_posted":"28th Feb 2021"
		}
]

def home(request):
	context = {
				"posts":models.Post.objects.all
				# We called all our Post objects "posts"
	}
	return render(request, 'blog/home.html',context)"""


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"  # by default it searches for <app>/<model>_<viewtype>.html
    context_object_name = "posts"  # by default the Post(model) objects are named objectlist
    # we can either change the object name or change the name of object variables in templates
    ordering = ['-date_posted']
    paginate_by = 4

class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_query_set(self):
    	user = get_object_or_404(User, username = self.kwargs.get("username"))
    	return Post.objects.filter(author=user).order_by('-date_posted')
    	# order by not working

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    """ Here we are overriding the parent class method of form_valid.
    We are setting the author = the current logged in user.By overriding it,
    we are ensuring that the author gets set before it runs anyway"""


class PostUpdateView( LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


""" The UserPassesTestMixin runs the test_func() and verifies whether the current user
is the author of the post """


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    return render(request, 'blog/about.html', {"title": "About"})
