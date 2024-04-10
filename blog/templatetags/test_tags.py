from django.shortcuts import get_object_or_404
from blog.models import Post # why "blog.models"
from django import template


register = template.Library()

@register.filter(name="get_post_title")
def post_title(pk):
    post = get_object_or_404(Post, pk=pk)
    return post.title
