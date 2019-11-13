from django.shortcuts import render, get_object_or_404

# Create your views here.
from blog.models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts,
    }
    return render(request, 'blog/blog-list.html',context)


def post_details(request, id, slug):
    post = get_object_or_404(Post,id=id,slug=slug)
    read_time = len(post.body.split())//50
    print(len(post.body.split()))
    context = {
        'post':post,
        'read_time':read_time
    }
    return render(request,'blog/blog-details.html',context)