import os,django,random

os.environ.setdefault("DJANGO_SETTINGS_MODULE","Django_MyBlog.settings")
django.setup()

from faker import Faker
from blog.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager
from taggit import *

cat = Category.objects.create(name='Category')

def create_post(N):

    fake=Faker()
    for i in range(1,N+1):

        id=random.randint(1,N)
        title=fake.name()
        status=random.choice(["published","draft"])
        post = Post.objects.get(id=i)
        Post.objects.create(title=title+"post!!!",
        author = User.objects.get(id=1),
        slug = "-".join(title.lower().split()),
        category = Category.objects.first(),
        tags = post.tags.add('music', 'jazz', 'django'),
        body = fake.text(),
        created = timezone.now(),
        updated = timezone.now(),)

create_post(10)
