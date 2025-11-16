from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,InvalidPage,PageNotAnInteger

# Create your views here.
def post_list(request):
    try:
        post_list = Post.objects.filter(status=Post.Status.PUBLISHED)

        # Pagination with 3 posts per page
        paginator = Paginator(post_list, 1)
        page_number = request.GET.get('page', 1)
        
        posts = paginator.page(page_number)
    except EmptyPage:
     # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts=paginator.page(1)

    return render(
    request,
    'blog/post/list.html',
    {'posts': posts}
)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    return render(request, "blog/post/details.html", {"post": post})
