from django.shortcuts import render, get_object_or_404
from .forms import PostForm, UserRegistrationForm, CommentForm
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post, Comment


def paginator(request, value, namber):
    if namber == '':
        namber = 5
    else:
        namber = namber
        paginator = Paginator(value, namber)  # Show 5 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj


def register(request):
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
    return render(request, 'registration/register.html', {'user_form': user_form})


def logout(request):
    request.session.flush()
    return render(request, 'registration/logout.html')


def post_list(request):
    posts = Post.objects.all().order_by('-published_date')
    namber = request.GET.get('pag', 5)
    return render(request, 'blog/post_list.html', {'page_obj': paginator(request, posts, namber)})


def author_list(request, id, value):
    list = Post.objects.filter(author_id=id).order_by('-published_date')
    namber = request.GET.get('pag', 5)
    return render(request, 'blog/author_list.html', {'page_obj': paginator(request, list, namber), 'author': value})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True).order_by('-created')
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.name = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


def profile(request):
    my_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    namber = request.GET.get('pag', 5)
    return render(request, 'accounts/profile.html', {'page_obj': paginator(request, my_posts, namber)})


# @login_required
def post_new(request):
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
    return render(request, 'blog/post_new.html', {'form': form})


def post_edit(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        post.title = request.POST.get("title")
        post.text = request.POST.get("text")
        post.author = request.user
        post.published_date = timezone.now()
        post.save()
        return redirect('post_detail', pk=post.pk)
    else:
        return render(request, "blog/edit.html", {"post": post})


def delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('post_list')
