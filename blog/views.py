from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.utils import timezone

from .models import Post, Comment, Follow, User
from blog.forms import PostForm, UserRegistrationForm, CommentForm


def register(request):
    title_registration = 'Registration'
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создание нового юзера, но пока без сохранения (commit=False).
            new_user = user_form.save(commit=False)
            # Установка выбранного пароля.
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохранение юзера.
            new_user.save()
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'title':title_registration})


@login_required
def logout(request):
    title = 'Logout'
    request.session.flush()
    return render(request, 'registration/logout.html', {'title':title})


def paginator(request, object_list, per_page):
    paginator = Paginator(object_list, per_page)  # Show 5 contacts per page.
    per_page = request.GET.get('pag')
    page_obj = paginator.get_page(per_page)
    return page_obj


def post_list(request):
    title = 'Newspaper'
    posts = Post.objects.all().order_by('-published_date')
    per_page = request.GET.get('pag', 5)
    return render(request, 'blog/post_list.html', {'page_obj': paginator(request, posts, per_page), 'title':title})


@login_required
def subscribed_to(request):
    title = 'Subscriptions'
    subscribers = Follow.objects.filter(user=request.user)
    return render(request, 'blog/follows.html', {'subscribers': subscribers, 'title':title})


@login_required
def subscribe(request, author):
    subscriber_name = User.objects.get(username=author)
    #исключаем повторное добавление записи в таблицу
    if not Follow.objects.filter(user_id=request.user.id, author_id=subscriber_name.id).exists():
        Follow.objects.create(user_id=request.user.id, author_id=subscriber_name.id)
        return redirect('author_list', id=subscriber_name.id, value=author)
    else: return redirect('author_list', id=subscriber_name.id, value=author)


@login_required
def unsubscribe(request, author):
    subscriber_name = User.objects.get(username=author)
    subscriber = Follow.objects.get(user_id=request.user.id, author_id=subscriber_name.id)
    subscriber.delete()
    return redirect('author_list', id=subscriber_name.id, value=author)


@login_required
def profile(request):
    title = 'My Page'
    my_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    per_page = request.GET.get('pag', 5)
    return render(request, 'accounts/profile.html', {'page_obj': paginator(request, my_posts, per_page), 'title':title})


def author_list(request, id, value):
    title = str(value) + ' page'
    list = Post.objects.filter(author_id=id).order_by('-published_date')
    per_page = request.GET.get('pag', 5)
    subscriber_name = User.objects.get(username=value)
    subscribers = Follow.objects.filter(user_id=request.user.id, author_id=subscriber_name.id).exists()
    return render(request, 'blog/author_list.html', {'page_obj': paginator(request, list, per_page), 'author': value, 'subscribers':subscribers, 'title':title})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    title = str(post.title)
    comments = post.comments.filter(active=True).order_by('-created')
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            try: new_comment.name = request.user
            except ValueError: return redirect('login')
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'title':title})


@login_required
def post_new(request):
    title = 'New post'
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form, 'title':title})


@login_required
def post_edit(request, pk):
    title = 'Editing an entry'
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        post.title = request.POST.get("title")
        post.text = request.POST.get("text")
        post.author = request.user
        post.created_date = timezone.now()
        post.save()
        return redirect('post_detail', pk=post.pk)
    else:
        return render(request, "blog/edit.html", {"post": post, 'title':title})


@login_required
def delete(request, pk):
    post = Post.objects.get(pk=pk) #request_pk = pk
    post.delete()
    return redirect('post_list')


@login_required
def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post_id)

