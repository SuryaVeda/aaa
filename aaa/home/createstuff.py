from .models import Tag
from django.utils.text import slugify


def fuck():
    for i in Tag.objects.all():
        print(slugify(i.name))
        i.name = slugify(i.name)
        i.save()
        print(i)
