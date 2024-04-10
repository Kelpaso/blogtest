from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from .models import User, Post, Comment
from .forms import PostForm, CommentForm, LoginForm, UserRegisterForm
from .forms import UpdateProfile_user

# Posts
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    url_referer = request.headers['Referer'] # The referring page
    return redirect(url_referer)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    url_referer = request.headers['Referer'] # The referring page
    if '/post/' in url_referer:
        return redirect('post_list')
    return redirect(url_referer)

# Comments
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

# Users
def sing_in(request):
    if request.user.is_authenticated:
        return redirect('logout')
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'registration/login.html', {'form':form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('post_list')
        # form is not valid or user is not authenticated
        messages.error(request, f"Invalid username or password")
        return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_user(request):
    if "submit_yes" in request.POST:
        logout(request)
        return redirect('login')
    elif "submit_no" in request.POST:
        return redirect('post_list')
    return render(request, 'registration/logout.html')

def user_register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}, account creation is successful!')
            return redirect('login')
    return render(request, 'registration/register.html', {'form': form})

# Profile views --start--

@login_required
def user_profile(request):
    user = get_object_or_404(User, pk=request.user.id)

    context = {
        'user': user,
    }
    return render(request, 'account/profile.html', context)

@login_required
def profile_edit(request):
    # default User data
    user = get_object_or_404(User, pk=request.user.id)
    # extension User data

    if request.method == 'POST':
        data_post = request.POST
        form_user = UpdateProfile_user(data_post)
        if form_user.is_valid:
            # I don't like this code, have to change this
            user.username, user.email = data_post['username'], data_post['email']
            user.phone, user.bio = data_post['phone'], data_post['bio']
            user.save()
            return redirect('user_profile')

    form_user = UpdateProfile_user(instance=user)

    context = {
        'form_user': form_user,
    }
    return render(request, 'account/profile_edit.html', context)

@login_required
def profile_posts(request):
    user = get_object_or_404(User, pk=request.user.id)
    posts = user.posts.all()
    context = {
        'posts': posts
    }
    return render(request, 'account/profile_posts.html', context)

@login_required
def profile_comments(request):
    user = get_object_or_404(User, pk=request.user.id)
    comments = user.comments.all()
    # posts = []
    # for comment in comments:
    #     posts += Post.objects.filter(pk=comment.post_id)
    # print(posts)
    # context = {
    #     'comments': comments,
    #     'posts': posts
    # }
    return render(request, 'account/profile_comments.html', {'comments': comments})

@login_required
def profile_delete(request):
    if "delete_yes" in request.POST:
        user = get_object_or_404(User, pk=request.user.id)
        user.delete()
        return redirect('post_list')
    elif "delete_no" in request.POST:
        return redirect('user_profile')
    return render(request, 'account/delete.html')

@login_required
def email_confirm(request):
    subject = f'Hi {request.user.username}, please confirm your email'
    text = f'Dear {request.user.username} select link to confirm email'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [request.user.email]
    recipient_list = [request.user.email]

    send_mail(subject, text, from_email, to_email, recipient_list)

    url_referer = request.headers['Referer'] # The referring page
    return redirect(url_referer)
# Profile views --end--
