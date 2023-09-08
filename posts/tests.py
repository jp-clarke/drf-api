from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='johnnytest', password='dukey')

    def test_can_list_posts(self):
        johnnytest = User.objects.get(username='johnnytest')
        Post.objects.create(owner=johnnytest, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='johnnytest', password='dukey')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        johnnytest = User.objects.create_user(
            username='johnnytest', password='dukey'
        )
        mary = User.objects.create_user(
            username='mary', password='susan'
        )
        Post.objects.create(
            owner=johnnytest, title='johnnys test', content='johnnys content'
        )
        Post.objects.create(
            owner=mary, title='marys test', content='marys content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'johnnys test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='johnnytest', password='dukey')
        response = self.client.put('/posts/1/', {'title': 'johnnys NEW test'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'johnnys NEW test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='mary', password='susan')
        response = self.client.put('/posts/1/', {'title': 'marys test'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
