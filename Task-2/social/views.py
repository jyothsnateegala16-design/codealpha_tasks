from django.shortcuts import render, redirect
from .models import Post, Like, Comment, Follow
from .forms import CommentForm
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .forms import ProfileImageForm
from .models import Profile
from .models import Notification




def home(request):

    # Search query
    query = request.GET.get('q')

    # Latest posts first
    posts = Post.objects.all().order_by('-created_at')

    # Apply search
    if query:
        posts = posts.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
        )

    # Pagination
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # Stats
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    total_likes = Like.objects.count()

    liked_posts = []
    notifications = []
    unread_notifications = 0

    if request.user.is_authenticated:

        liked_posts = Like.objects.filter(
            user=request.user
        ).values_list('post_id', flat=True)

        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')

        unread_notifications = notifications.filter(
            is_read=False
        ).count()

    context = {
        'posts': posts,
        'total_users': total_users,
        'total_posts': total_posts,
        'total_likes': total_likes,
        'liked_posts': liked_posts,
        'notifications': notifications,
        'unread_notifications': unread_notifications,
    }

    return render(request, 'social/home.html', context)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})



@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "🎉 Post created successfully!")
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'social/create_post.html', {'form': form})

@login_required
def profile(request):
    user = request.user

    posts = Post.objects.filter(user=user).order_by('-created_at')

    followers_count = Follow.objects.filter(following=user).count()

    following_count = Follow.objects.filter(follower=user).count()

    context = {
        'profile_user': user,
        'posts': posts,
        'total_posts': posts.count(),
        'followers_count': followers_count,
        'following_count': following_count,
    }

    return render(request, 'social/profile.html', context)


@login_required
def user_profile(request, user_id):
    profile_user = User.objects.get(id=user_id)

    posts = Post.objects.filter(user=profile_user).order_by('-created_at')

    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'total_posts': posts.count(),
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    }

    return render(request, 'social/profile.html', context)


@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id, user=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Post updated successfully!")
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, 'social/edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id, user=request.user)

    if request.method == "POST":
        post.delete()
        messages.success(request, "🗑️ Post deleted successfully!")
        return redirect('home')

    return render(request, 'social/delete_post.html', {'post': post})



def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comment_set.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'social/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )
    if post.user != request.user:
        Notification.objects.create(
            user=post.user,
            message=f"{request.user.username} liked your post ❤️"
        )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    like_count = Like.objects.filter(post=post).count()

    return JsonResponse({
        "liked": liked,
        "like_count": like_count
    })


def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

    return redirect('post_detail', post_id=pk)

@login_required
def follow_user(request, user_id):

    user_to_follow = User.objects.get(id=user_id)

    if user_to_follow == request.user:
        return redirect('profile')

    follow = Follow.objects.filter(
        follower=request.user,
        following=user_to_follow
    )

    if follow.exists():

        follow.delete()
        messages.success(request, f"You unfollowed {user_to_follow.username}.")

    else:

        Follow.objects.create(
            follower=request.user,
            following=user_to_follow
        )

        # Notification
        Notification.objects.create(
            user=user_to_follow,
            message=f"{request.user.username} started following you 👤"
        )

        messages.success(request, f"You are now following {user_to_follow.username}.")

    return redirect('user_profile', user_id=user_id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Comment owner matrame delete cheyyali
    if request.user == comment.user:
        post_id = comment.post.id
        comment.delete()
        return redirect('post_detail', post_id=post_id)

    return redirect('home')

@login_required
def upload_profile_image(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        print("POST Request")
        print(request.FILES)

        form = ProfileImageForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()
            print("Image Saved Successfully")

            return redirect('profile')

        else:

            print(form.errors)

    else:

        form = ProfileImageForm(instance=profile)

    return render(request, 'social/upload_image.html', {'form': form})



