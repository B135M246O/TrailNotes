from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Сообщества по маршрутам и видам путешествий."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()

    class Meta:
        ordering = ['pk']
        verbose_name = 'Сообщество путешественников'
        verbose_name_plural = 'Сообщества путешественников'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Путевая заметка с фотографией и сообществом."""
    text = models.TextField(
        verbose_name='Текст путевой заметки',
        help_text='Маршрут, впечатления и полезные детали поездки',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='group_posts',
        blank=True,
        null=True,
        help_text='Сообщество путешественников для этой заметки',
        verbose_name='Сообщество путешественников',
    )
    image = models.ImageField(
        'Фотография поездки',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Путевая заметка'
        verbose_name_plural = 'Путевые заметки'

    def __str__(self) -> str:
        return self.text[:15]


class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий к заметке'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст нового комментария',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария',
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор заметок',
    )

    class Meta:
        verbose_name = 'Подписка на путешественника'
        verbose_name_plural = 'Подписки на путешественников'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_subscribe'
            )
        ]
