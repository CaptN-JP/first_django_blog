from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from . import views, models
from .models import Post
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)


class Test_Urls(SimpleTestCase):
    """Testing all urls inside blog app"""

    def test_PostListView_url(self):
        url = reverse("blog-home")
        self.assertEquals(resolve(url).func.view_class, PostListView)

    def test_UserPostListView_url(self):
        url = reverse("user-posts", args=["r"])
        self.assertEquals(resolve(url).func.view_class, UserPostListView)

    def test_PostDetailView_url(self):
        url = reverse("post-detail", args=[1])
        self.assertEquals(resolve(url).func.view_class, PostDetailView)

    def test_PostCreateView_url(self):
        url = reverse("post-create")
        self.assertEquals(resolve(url).func.view_class, PostCreateView)

    def test_PostUpdateView_url(self):
        url = reverse("post-update", args=[1])
        self.assertEquals(resolve(url).func.view_class, PostUpdateView)

    def test_PostDeleteView_url(self):
        url = reverse("post-delete", args=[1])
        self.assertEquals(resolve(url).func.view_class, PostDeleteView)

    def test_about_url(self):
        url = reverse("blog-about")
        self.assertEquals(resolve(url).func, views.about)

    # print(resolve(url))  ... to know what it returns


# from django.test import TestCase, Client
# from django.urls import reverse, resolve
# import json
# from .models import Post
from django.contrib.auth.models import User
from django.utils import timezone
import json


class Test_setup(TestCase):

    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='jacob',
            email='jacob@…',
            password='top_secret'
        )

        print(f"username is {self.user.username}")

        self.post = Post.objects.create(
            title="title eg",
            content="content eg",
            author=self.user
        )
        #self.client.force_login(user=self.user)

    # class Test_basic_views(Test_setup):

    def test_PostListView_GET(self):
        response = self.client.get(reverse("blog-home"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/home.html")

    def test_about_GET(self):
        response = self.client.get(reverse("blog-about"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/about.html")

    def test_UserPostListView_GET(self):
        response = self.client.get(reverse("user-posts", args=[self.post.author]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/user_posts.html")

    def test_PostDetailView_GET(self):
        response = self.client.get(reverse("post-detail", args=[self.post.author.id]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")

    def test_PostUpdateView_GET(self):
        self.client.force_login(user=self.user) # behaving as authenticated user
        response = self.client.get(reverse("post-update", args=[1]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_form.html")

    def test_PostUpdateView_POST(self):
        
        print(f"test username {self.user.username}")
        print(f"test password {self.user.password}")

        #self.client.login(username=self.user.username, password=self.user.password)

        # self.client.login(kwargs={"username":self.user.username, "password":self.user.password})

        self.client.force_login(user=self.user)
        data = {"title": "It the title",
            "content": "updated content",
            "date_posted": "March 6,2021",
            "author":self.user}

        response = self.client.post(reverse("post-update", args=[self.post.id]), data, format= "json")

        for post in Post.objects.all():
            print('blog content', post.content)
        updated_content = Post.objects.get(pk=self.post.id).content
        
        self.post.refresh_from_db()
        self.assertEquals(response.status_code, 302)
        #self.assertRedirects(response, reverse('login'))   check in case not logged in should redirect to login page
        self.assertEquals(updated_content, data["content"])

    # def test_PostDeletelView_GET(self):

    #     response = self.client.get(reverse("post-delete", args=[1])

    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, "blog/post_confirm_delete.html")
        
    #def test_PostDeleteView_DEL(self):
        # self.user1 = User.objects.create_user(
        #     username='jacobian',
        #     email='jaco1b@…',
        #     password='1top_secret'
        # )
        # self.post1 = Post.objects.create(
        #     title="title del",
        #     content="content del",
        #     author=self.user
        # )

        # response = self.client.delete(reverse("post-delete", args=[2])
        # self.assertEquals(response.status_code, 204)
