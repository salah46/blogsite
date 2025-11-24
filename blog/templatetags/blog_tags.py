from django import template
from django.db.models import Count, Q
from blog.models import Post
register = template.Library()


@register.simple_tag
def get_recent_posts(count=5):
    return Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-publish')[:count]


@register.inclusion_tag('blog/post/latest_posts.html')
def get_latest_posts_inclusion_style(count  = 5):
    latest_posts = Post.objects.filter(
        status=Post.Status.PUBLISHED).order_by('-publish')[:count]

    return  {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.filter(
        status=Post.Status.PUBLISHED
    ).annotate(
        total_comments=Count('comments', filter=Q(comments__active=True))
    ).order_by('-total_comments', '-publish')[:count]       

@register.simple_tag
def total_posts():
    return Post.objects.filter(status=Post.Status.PUBLISHED).count()
