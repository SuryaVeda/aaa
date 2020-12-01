from django import template
from archives.models import Review

register = template.Library()


@register.simple_tag
def has_review(user, book):
    try:
        Review.objects.get(user=user, book=book)
        return True
    except:
        return False
