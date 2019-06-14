from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import  LogEntry

from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager, RelatedFieldListFilter
import xadmin

from .models import Category, Tag, Post
from typeidea.base_admin import BaseOwnerAdmin


class PostInline:
    form_layout=(
        Container(
            Row('title','desc'),
        )
    )
    fields = ('title', 'desc')
    extra = 1
    model = Post

class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id','name')

manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    #form = PostAdminForm
    list_display = ('title', 'category', 'status', 'created_time', 'owner','operator')
    list_display_links = []

    list_filter = ['category',]
    search_fields = ( 'title', 'category__name')
    actions_on_top =  True
    actions_on_bottom = True

    #编辑页面
    save_on_top = True


    exclude = ('owner',)
    form_layout = (
        Fieldset('基础配置', Row('title','category'), 'status', 'tag'),
        Fieldset('内容信息', 'desc','content'),
    )
    filter_horizontal = ('tag',)
    #fields = ( ('category', 'title'), 'desc', 'status', 'content', 'tag')

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('xadmin:blog_post_change', args=(obj.id,)))

    operator.short_description = "操作"

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "tag":
            kwargs["queryset"] = Tag.objects.filter(owner_id=request.user.id)
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(owner_id=request.user.id)
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

   # class Media:
      #  css = {
          #  'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',)
     #   }
      #  js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = (PostInline,)
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')
