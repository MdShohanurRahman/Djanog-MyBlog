from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from blog.models import *
from .forms import *
# from taggit.models import Tag

# Create your views here.



def post_list(request,category_id=None):
    posts = Post.objects.all()
    
    categories = Category.objects.all()
    tags = Tag.objects.all()
    category = None

    if category_id:
        category = get_object_or_404(Category,id=category_id)
        posts = posts.filter(category=category.id)

    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts = paginator.get_page(page)  
    context = {
        'posts' : posts,
        'categories':categories,
        'tags':tags,
        'category':category,

    }
    return render(request, 'blog/blog-list.html',context)


# def post_list_by_tag(request,tag_slug):
    
#     tag = get_object_or_404(Tag,id=tag_slug.id)
#     posts = posts.filter(tags__in=[tag])

#     context = {
#         'tag':tag,
#         'posts':posts
#     }
    
    return render(request, 'blog/blog-list.html',context)

def post_details(request, id, slug):
    post = get_object_or_404(Post,id=id,slug=slug)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    read_time = len(post.body.split())//50
    related_posts = Post.objects.filter(category=post.category).exclude(id=id)[:4]
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked=True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')  # content is the attr of model named comment
            reply_id = request.POST.get('comment_id')
            comment_qs = None

            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
                
            comments = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comments.save()
            return HttpResponseRedirect(post.get_absolute_url())
    
    else:
        comment_form = CommentForm()

    context = {
        'post':post,
        'related_posts':related_posts,
        'read_time':read_time,
        'is_liked':is_liked,
        'total_likes':post.total_likes(),
        'categories':categories,
        'tags':tags,
        'comments': comments,
        'comment_form': comment_form,

    }

    if request.is_ajax():
        html = render_to_string('blog/comments.html', context, request=request)
        return JsonResponse({'form': html})

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


def search_post(request):
    posts = Post.objects.all()
    search = request.GET.get('q')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    if search:
        posts=posts.filter(
        Q(title__icontains=search)|
        Q(body__icontains=search)|
        Q(description__icontains=search)
        #icontains means case insensative
    )

    context = {
    'posts':posts,
    'search':search,
    'categories':categories,
    'tags':tags,
    }

    return render(request, 'blog/blog-list.html',context)