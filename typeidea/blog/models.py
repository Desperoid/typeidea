from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from django.core.cache import cache

import mistune
# Create your models here.

class Category(models.Model):
    STATUS_NOMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS =( (STATUS_NOMAL, '正常'), (STATUS_DELETE, '删除'))

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NOMAL, choices=STATUS_ITEMS, verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status = cls.STATUS_NOMAL)
        nav_categories = []
        normal_categories = []
        for category in categories:
            if category.is_nav:
                nav_categories.append(category)
            else :
                normal_categories.append(category)
        return {
            'navs':nav_categories,
            'categories':normal_categories,
        }

    def  __str__(self):
        return  self.name
    class Meta:
        verbose_name =verbose_name_plural='分类'


class Tag(models.Model):
    STATUS_NOMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = ((STATUS_NOMAL, '正常'), (STATUS_DELETE, '删除'))
    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NOMAL, choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural= '标签'

class Post(models.Model):
    STATUS_NOMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = ((STATUS_NOMAL, '正常'), (STATUS_DELETE, '删除'),
                    (STATUS_DRAFT, '草稿'))

    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须用MarkDown格式')
    content_html = models.TextField(verbose_name='正文html代码', blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NOMAL, choices=STATUS_ITEMS, verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    is_md = models.BooleanField(default=False, verbose_name='markdown语法')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_md:
            self.content_html = mistune.markdown(self.content)
        else :
            self.content_html = self.content
        super().save(force_insert, force_update, using, update_fields)

    @cached_property
    def tags(self):
        return '.'.join(self.tag.values_list('name', flat=True))

    @classmethod
    def hot_posts(cls):
        result = cache.get('hot_posts')
        if not result:
            result = cls.objects.filter(status=cls.STATUS_NOMAL).order_by('-pv').only('title','id')
            cache.set('hot_posts', result, 10*60)
        return result

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else :
            post_list = tag.post_set.filter(status=Post.STATUS_NOMAL).select_related('owner', 'category')
        return post_list,tag

    @staticmethod
    def get_by_category(category_id):
        try:
            categroy = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            categroy = None
            post_list = []
        else:
            post_list = categroy.post_set.filter(status = Post.STATUS_NOMAL).select_related('owner', 'category')

        return post_list, categroy

    @classmethod
    def latest_posts(cls, with_related=True):
        queryset = cls.objects.filter(status=cls.STATUS_NOMAL)
        if with_related:
            queryset = queryset.select_related('owner', 'category').prefetch_related('tag')
        return queryset

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id'] #根据id的降序排序