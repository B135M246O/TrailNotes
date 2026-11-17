from django.test import TestCase

from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг группы',
            description='Описание тестовой группы',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост для проверки длины __str__',
            group=cls.group,
        )

    def test_models_have_correct_object_names(self):
        """Проверка, что у моделей корректно работает __str__."""
        self.assertEqual(str(self.post), self.post.text[:15])
        self.assertEqual(str(self.group), self.group.title)

    def test_models_have_correct_verbose_name(self):
        """Проверка корректности verbose_name."""
        field_verbose = {
            'text': 'Текст путевой заметки',
            'group': 'Сообщество путешественников',
            'author': 'Автор',
            'pub_date': 'Дата публикации',
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.post._meta.get_field(value).verbose_name, expected)

    def test_models_have_correct_help_texts(self):
        """Проверка корректности help_text."""
        field_help_texts = {
            'text': 'Маршрут, впечатления и полезные детали поездки',
            'group': 'Сообщество путешественников для этой заметки',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.post._meta.get_field(value).help_text, expected)
