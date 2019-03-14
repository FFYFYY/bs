from django.db import models
from django.contrib.auth.models import User


class Books(models.Model):
    book_name = models.CharField(max_length=40, db_index=True, verbose_name='书名')
    author = models.CharField(max_length=30, verbose_name='作者')
    intro = models.CharField(max_length=200, null=True, blank=True, verbose_name='简介')
    img_url = models.CharField(max_length=100, null=True, blank=True, verbose_name='封面')
    category = models.CharField(max_length=6, null=True, blank=True, verbose_name='类型')
    searches = models.IntegerField(default=0, verbose_name='搜索量')
    views = models.IntegerField(default=0, verbose_name='阅读量')

    class Meta:
        db_table = 'books'
        verbose_name_plural = '小说'

    def __str__(self):
        return self.book_name


class Sources(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    source = models.CharField(max_length=30)

    class Meta:
        db_table = 'sources'
        verbose_name_plural = '来源'


class Likes(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'
        verbose_name_plural = '收藏'

    def __str__(self):
        return self.user
