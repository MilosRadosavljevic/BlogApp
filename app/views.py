from django.shortcuts import render
from app.forms import CommentForm, SubscribeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.models import Comments, Post, Profile, Tag, WebsiteMeta
from django.contrib.auth.models import User
from django.db.models import Count


def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]
    featured_blog = Post.objects.filter(is_featured=True)
    subscribe_form = SubscribeForm()
    subscribe_message = ''
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if featured_blog:
        featured_blog = featured_blog[0]

    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            request.session['subscribed'] = True
            subscribe_message = 'Subscribed successfully'
            subscribe_form = SubscribeForm()
        else:
            subscribe_message = 'This email already exists'

    context = {
        'posts': posts,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'subscribe_form': subscribe_form,
        'subscribe_message': subscribe_message,
        'featured_blog': featured_blog,
        'website_info': website_info,
    }

    return render(request, 'app/index.html', context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post=post, parent=None)
    form = CommentForm()

    if request.POST:
        comment_form = CommentForm(request.POST)
        parent_obj = None
        if comment_form.is_valid:
            if request.POST.get('parent'):
                # saving reply
                parent = request.POST.get('parent')
                parent_obj = Comments.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.save()
                    # redirecting after leaving a comment, prevent multiplying the same comment while refreshing the page
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
            else:
                # saving commnet
                comment = comment_form.save(commit=False)
                postid = request.POST.get('post_id')
                post = Post.objects.get(id=postid)
                comment.post = post
                comment.save()
                # redirecting after leaving a comment, prevent multiplying the same comment while refreshing the page
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    post.save()

    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }

    return render(request, 'app/post.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)

    top_posts = Post.objects.filter(
        tags__in=[tag.id]).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(
        tags__in=[tag.id]).order_by('-last_updated')[0:3]

    tags = Tag.objects.all()

    context = {
        'tag': tag,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'tags': tags,
    }
    return render(request, 'app/tag.html', context)


def author_page(request, slug):
    profile = Profile.objects.get(slug=slug)

    top_posts = Post.objects.filter(
        author=profile.user).order_by('-view_count')[0:2]

    recent_posts = Post.objects.filter(
        author=profile.user).order_by('-last_updated')[0:3]

    # anotate every querySet with the provided list of query expresions
    # example -> a = User.objects.annotate(number=Count('post')) ---> for every user in the querySet
    # setting the property `number` which is representing the count of posts that this user has
    # example2 -> a[0].number
    top_authors = User.objects.annotate(
        number=Count('post')).order_by('number')

    context = {
        'profile': profile,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'top_authors': top_authors,
    }

    return render(request, 'app/author.html', context)


def search_post(request):
    search_query = ''
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)
    context = {
        'posts': posts,
        'search_query': search_query,
    }
    return render(request, 'app/search.html', context)


def about(request):
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    context = {
        'website_info': website_info,
    }
    return render(request, 'app/about.html', context)
