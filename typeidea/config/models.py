from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string


# 友链Model
class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    title = models.CharField(max_length=50, verbose_name="标题")
    href = models.URLField(verbose_name="链接")  # 默认长度为200
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1, 6), range(1, 6)), verbose_name="权重", help_text="权重高展示顺序靠前")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '友链'
        ordering = ['-weight']
    
    @classmethod
    def get_links(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset


# 侧边栏Model
class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    SIDE_TYPE_HTML = 1
    SIDE_TYPE_LATEST_POSTS = 2
    SIDE_TYPE_HOT_POSTS = 3
    SIDE_TYPE_LATEST_COMMENTS = 4
    STATUS_ITEMS = (
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏'),
    )
    SIDE_TYPE = (
        (SIDE_TYPE_HTML, 'HTML'),
        (SIDE_TYPE_LATEST_POSTS, '最新文章'),
        (SIDE_TYPE_HOT_POSTS, '最热文章'),
        (SIDE_TYPE_LATEST_COMMENTS, '最近评论'),
    )

    title = models.CharField(max_length=50, verbose_name="标题")
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE, verbose_name="展示类型")
    content = models.CharField(max_length=500, blank=True, verbose_name="内容", help_text="如果设置的不是HTML类型，可为空")
    status = models.PositiveIntegerField(default=STATUS_SHOW, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    @property
    def content_html(self):
        """ 直接渲染模板 """
        from blog.models import Post
        from comment.models import Comment

        result = ''

        if self.display_type == self.SIDE_TYPE_HTML:
            result = self.content
        elif self.display_type == self.SIDE_TYPE_LATEST_POSTS:
            context = {
                'posts': Post.latest_posts(),
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.SIDE_TYPE_HOT_POSTS:
            context = {
                'posts': Post.hot_posts(),
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.SIDE_TYPE_LATEST_COMMENTS:
            context = {
                'comments': Comment.latest_comments(),
            }
            result = render_to_string('config/blocks/sidebar_comments.html', context)
        else:
            pass

        return result

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'