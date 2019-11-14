from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.models import *
from taggit.models import Tag

# Create your views here.



def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'posts' : posts,
        'categories':categories,
        'tags':tags,

    }
    return render(request, 'blog/blog-list.html',context)


def post_details(request, id, slug):
    post = get_object_or_404(Post,id=id,slug=slug)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    read_time = len(post.body.split())//50
    related_posts = Post.objects.filter(category=post.category).exclude(id=id)[:4]

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked=True

    context = {
        'post':post,
        'related_posts':related_posts,
        'read_time':read_time,
        'is_liked':is_liked,
        'total_likes':post.total_likes(),
        'categories':categories,
        'tags':tags,

    }
    return render(request,'blog/blog-details.html',context)


def like_post(request):
    post=get_object_or_404(Post,id=request.POST.get('post_id')) #came from value=post.id
    # post=get_object_or_404(Post,id=request.POST.get('id')) #came from value=post.id
    is_liked =False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked=False
    else:
        post.likes.add(request.user)
        is_liked=True

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes()
    }

    if request.is_ajax():
        html=render_to_string('blog/like-section.html',context,request=request)
        return JsonResponse ({'form':html})
