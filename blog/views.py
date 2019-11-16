from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q,Count
from blog.models import *
from .forms import *
# from taggit.models import Tag

# Create your views here.


# def get_author(user):
#     qs = Author.objects.filter(user=user)
#     if qs.exists():
#         return qs[0]
#     return None


def get_category_count():
    queryset = Category.objects.values("name","slug").annotate(Count("categories")) 
    return queryset


def page_view(post):
    """
    count the number of hits in desire url
    parameter post come from instance of single post
    """
    page_view = PageView.objects.filter(post = post)
    if(page_view.count()<=0):
        x=PageView.objects.create(
            post = post
            )
        x.save()
    else:
        x = page_view.first()
        x.hits = x.hits+1
        x.save()

    return x.hits



def post_list(request,category_slug=None,tag_slug=None):
    posts = Post.objects.filter(status="published")
    # posts = Post.published.all()
    top_posts = Post.published.all().order_by('-created')[:3]
    # categories = Category.objects.all()
    categories = get_category_count()
    tags = Tag.objects.all()

    category = None
    tag = None

    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        posts = posts.filter(category=category)


    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        posts = Post.objects.filter(tags=tag)


    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)  
    context = {
        'posts' : posts,
        'top_posts':top_posts,
        'categories':categories,
        'tags':tags,
        'category':category,
        'tag':tag,

    }
    return render(request, 'blog/blog-list.html',context)



def post_details(request, id, slug):
    post = get_object_or_404(Post,id=id,slug=slug)
    top_posts = Post.published.all().order_by('-created')[:3]
    related_posts = Post.published.filter(category=post.category).exclude(id=id)[:4]
    page_views = page_view(post)
    categories = get_category_count() 
    tags = Tag.objects.all()
    read_time = len(post.body.split())//50
    
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
        'top_posts':top_posts,
        'related_posts':related_posts,
        'read_time':read_time,
        'is_liked':is_liked,
        'total_likes':post.total_likes(),
        'categories':categories,
        'tags':tags,
        'comments': comments,
        'comment_form': comment_form,
        'page_views':page_views,

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
    posts = Post.published.all()
    top_posts = Post.published.all().order_by('-created')[:3]
    search = request.GET.get('q')
    categories = get_category_count() 
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
    'top_posts':top_posts,
    }

    return render(request, 'blog/blog-list.html',context)