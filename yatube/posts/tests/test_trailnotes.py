from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post, User


class TrailNotesTests(TestCase):
    def test_travel_labels_and_communities_fixture(self):
        call_command('loaddata', 'travel_communities', verbosity=0)
        self.assertEqual(Group.objects.count(), 3)
        self.assertTrue(Group.objects.filter(slug='hiking').exists())
        self.assertEqual(PostForm().fields['text'].label, 'Текст путевой заметки')
        self.assertEqual(Post._meta.verbose_name, 'Путевая заметка')

    def test_travel_note_visible_on_profile_and_community(self):
        user = User.objects.create_user(username='traveller')
        group = Group.objects.create(title='Пешие маршруты', slug='hiking', description='Тропы')
        note = Post.objects.create(author=user, group=group, text='Маршрут по тропе вдоль озера')
        for url in [reverse('posts:profile', args=[user.username]), reverse('posts:group_list', args=[group.slug]), reverse('posts:post_detail', args=[note.pk])]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, 'TrailNotes')
                self.assertContains(response, note.text)

    def test_author_page_shows_adaptation_author(self):
        self.assertContains(self.client.get(reverse('about:author')), 'Автор адаптации и доработок — Рябуха Олег')
