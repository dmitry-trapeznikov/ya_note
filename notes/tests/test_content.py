# отдельная заметка передаётся на страницу со списком заметок в списке object_list в словаре context;
# в список заметок одного пользователя не попадают заметки другого пользователя;
# на страницы создания и редактирования заметки передаются формы.

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор_1')
        cls.note = Note.objects.create(title='Заголовок', text='Текст', author=cls.author, slug='note-slug')
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.add_url = reverse('notes:add')
        cls.author = User.objects.create(username='Комментатор')

        # Запоминаем текущее время:
      
    def test_authorized_client_has_form_add(self):
        # Авторизуем клиент при помощи ранее созданного пользователя.
        self.client.force_login(self.author)
        response = self.client.get(self.add_url)
        self.assertIn('form', response.context)

    def test_authorized_client_has_form_edit(self):
        # Авторизуем клиент при помощи ранее созданного пользователя.
        self.client.force_login(self.author)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertIn('form', response.context)


