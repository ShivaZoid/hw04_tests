from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group, User


class PostFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='NoName')
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        self.post = Post.objects.create(
            author=self.user,
            text='Тестовый текст',
        )
        posts_count = Post.objects.count()
        last_post = Post.objects.order_by('id').last()
        form_data = {
            'text': 'Тестовый текст',
            'author': self.user,
            }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response, reverse('posts:profile',
                              kwargs={'username': self.user.username})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(str(last_post), self.post.text)
        self.assertEqual(last_post.author, self.post.author)

    def test_post_edit(self):
        """Валидная форма изменяет запись в Post."""
        self.post = Post.objects.create(
            author=self.user,
            text='Изменяем текст',
        )
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        last_post = Post.objects.order_by('id').last()
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Изменяем текст',
            'group': self.group.id,
            }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=({self.post.id})),
            data=form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response, reverse('posts:post_detail',
                              kwargs={'post_id': self.post.id})
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(str(last_post), self.post.text)
        self.assertEqual(last_post.author, self.post.author)

    def test_post_edit_not_create_guest_client(self):
        """Валидная форма не изменит запись в Post если неавторизован."""
        self.post = Post.objects.create(
            author=self.user,
            text='Изменяем текст',
        )
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        last_post = Post.objects.order_by('id').last()
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Изменяем текст',
            'group': self.group.id,
            }
        response = self.guest_client.post(
            reverse('posts:post_edit', args=({self.post.id})),
            data=form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response,
            f'/auth/login/?next=/posts/{self.post.id}/edit/')
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(str(last_post), self.post.text)
        self.assertEqual(last_post.author, self.post.author)
