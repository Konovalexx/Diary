from django.test import TestCase
from django.urls import reverse, resolve
from diary.views import (
    IndexView,
    MyDiaryView,
    EntryCreateView,
    EntryDeleteView,
    EntryUpdateView,
)


class URLTest(TestCase):
    def test_home_url(self):
        # Проверка главной страницы (home)
        resolver = resolve("/")
        self.assertEqual(resolver.view_name, "home")

    def test_index_url(self):
        # Проверка пути для главной страницы дневника
        resolver = resolve("/diary/")
        self.assertEqual(resolver.view_name, "diary:index")

    def test_new_entry_url(self):
        # Проверка пути для создания новой записи
        resolver = resolve("/diary/new/")
        self.assertEqual(resolver.view_name, "diary:new_entry")

    def test_my_diary_url(self):
        # Проверка пути для личного дневника пользователя
        resolver = resolve("/diary/my-diary/")
        self.assertEqual(resolver.view_name, "diary:my_diary")

    def test_update_entry_url(self):
        # Проверка пути для редактирования записи
        resolver = resolve("/diary/1/edit/")
        self.assertEqual(resolver.view_name, "diary:update_entry")

    def test_delete_entry_url(self):
        # Проверка пути для удаления записи
        resolver = resolve("/diary/1/delete/")
        self.assertEqual(resolver.view_name, "diary:delete_entry")
