from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор_1')
        cls.reader = User.objects.create(username='Автор_2')
        cls.note = Note.objects.create(title='Заголовок', text='Текст', author=cls.author, slug='note-slug')


    def test_pages_availability(self):
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK) 


    def test_edit_note_delete_pages_availability_for_author(self):
        with self.subTest():
            self.client.force_login(self.author)
            url = reverse('notes:detail', args=(self.note.slug,))
            response = self.client.get(url)
            print(response.status_code)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_list_success_add_for_logged_user(self):
        self.client.force_login(self.author)
        for name in ('notes:list', 'notes:success', 'notes:add'):  
            with self.subTest(user=self.author, name=name):        
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK) 

    def test_availability_for_detail_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit', 'notes:detail', 'notes:delete'):  
                with self.subTest(user=user, name=name):        
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)                          


    def test_redirect_for_anonymous_client_with_slug(self):
        login_url = reverse('users:login')
        for name in ('notes:detail', 'notes:edit', 'notes:delete'):
            with self.subTest(name=name):
                url = reverse(name, args=(self.note.slug,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)


    def test_redirect_for_anonymous_client_without_slug(self):
        login_url = reverse('users:login')
        for name in ('notes:list', 'notes:success', 'notes:add'):
            with self.subTest(name=name):
                url = reverse(name)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)                                     

