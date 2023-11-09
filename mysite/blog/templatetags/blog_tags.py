from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import *

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag()
def get_count_post():
    return Post.objects.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_post(count: int = 5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag()
def get_most_discussed(count: int = 5):
    most_discussed = Post.published.annotate(
        cnt_comments=Count("comments")
    ).order_by('-cnt_comments')[:count]
    return most_discussed
