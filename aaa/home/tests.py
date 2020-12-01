from django.test import TestCase
from .models import Post, Comment
from accounts.models import User

# Create your tests here.

# tests for models


class PostTestCase(TestCase):
    def setUp(self):
        User.objects.create(email='kati@gmail.com', password='katikati', username='kati')
        User.objects.create(email='sk@gmail.com', password='katikati', username='sk')
        kati = User.objects.get(email='kati@gmail.com')
        sk = User.objects.get(email='sk@gmail.com')
        a =Post.objects.create(heading='greetings', content='hi', user=kati)
        b =Comment.objects.create(text='hello to you too', user= sk)
        a.comments.add(b)

    def test_post(self):
        post = Post.objects.get(heading='greetings')
        comment = Comment.objects.get(text='hello to you too')
        self.assertEqual(post.content, 'hi')
        a = post.comments.all()
        self.assertEqual(a[0], comment)