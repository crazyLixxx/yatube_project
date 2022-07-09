from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Group, Post

User = get_user_model()
CommonURLs = {
    '': 'posts/index.html',
}
OnlyAuthorisedURLs = {
    '/create/': 'posts/create_post.html',
    '/group/group_slug/': 'posts/group_list.html',
    '/posts/1/': 'posts/post_detail.html',
    '/profile/hanson/': 'posts/profile.html',
}
OnlyAuthorURLs ={
    '/posts/1/edit/': 'posts/create_post.html',
}


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)


class DynamicURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(username='tom')
        User.objects.create_user(username='hanson')
        Group.objects.create(
            title='Название группы',
            slug='group_slug',
            description='Описание группы на 500 символов'
        )
        Post.objects.create(
            author=User.objects.get(username='hanson'),
            text='тут текст гениального поста про стенс'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user_reader = User.objects.get(username='tom')
        self.authorized_user_reader = Client()
        self.authorized_user_reader.force_login(self.user_reader)
        self.user_author = User.objects.get(username='hanson')
        self.authorized_user_author = Client()
        self.authorized_user_author.force_login(self.user_author)

    def test_urls_exist_at_desired_location(self):
        for address in OnlyAuthorisedURLs:
            with self.subTest(address=address):
                self.assertEqual(
                    self.authorized_user_author.get(address).status_code, 200
                    )

    def test_urls_exist_at_desired_location_main(self):
        users = [
            self.guest_client,
            self.authorized_user_reader,
            self.authorized_user_author
        ]
        pages = [
            CommonURLs,
            OnlyAuthorisedURLs,
            OnlyAuthorURLs
        ]
        for user in users:
            for page in pages:
                if user == OnlyAuthorURLs