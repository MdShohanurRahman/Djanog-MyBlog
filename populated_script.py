import os,django,random

os.environ.setdefault("DJANGO_SETTINGS_MODULE","Django_MyBlog.settings")
django.setup()

from faker import Faker
from blog.models import *
from django.contrib.auth.models import User
from django.utils import timezone




def create_credential():
    """
    create credential for post
    """
    fake = Faker()
    for i in range(5): # create five credentials
        cat_name = fake.name()
        tag_name = fake.name()
        Category.objects.create(name=cat_name,slug="-".join(cat_name.lower().split()))
        Tag.objects.create(name=cat_name,slug="-".join(tag_name.lower().split()))



def create_post(N):

    fake=Faker()
    # user = User.objects.create_user(username='test',
    #                              email='test@gmail.com',
    #                              password='123456789u')
    for i in range(1,N+1):

        id=random.randint(1,5)
        title=fake.name()
        # status=random.choice(["published","draft"])
        tag1 = Tag.objects.get(id=random.randint(1,2))
        tag2 = Tag.objects.get(id=random.randint(3,5))
        post = Post.objects.create(title=title+"post!!!",
            author = User.objects.get(id=1),
            slug = "-".join(title.lower().split()),
            category = Category.objects.get(id=id),
            description = fake.text(),
            body = fake.text(),
            created = timezone.now(),
            updated = timezone.now(),
            status = status )

        post.tags.add(tag1,tag2)
        

create_credential()
create_post(10)
print('successfully done')