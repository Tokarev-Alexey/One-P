from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from .forms import UserRegistrationForm


def post_list(request):
    posts = Post.objects.order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def author_list(request, id, value):
    list = Post.objects.filter(author_id=id).order_by('-published_date')
    return render(request, 'blog/author_list.html', {'list': list, 'author': value})


@login_required
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
    return render(request, 'blog/post_edit.html', {'form': form})


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
            return render(request, 'registration/login.html', {'new_user': new_user})
#            return redirect('post_list.html')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})
#    return redirect('post_list.html')


#@login_required

def logout(request):
    return render(request, 'registration/logout.html')
