
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    image = models.ImageField(
        default='default.png',
        upload_to='profile_pics'
    )


    def __str__(self):
        return f"{self.user.username} Profile"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_like')
        ]

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.id}"

# FOLLOW SYSTEM
class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    following = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


#class Profile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    #image = models.ImageField(upload_to='profile_pics', default='default.png')
    #bio = models.TextField(blank=True, max_length=250)

    #def __str__(self):
        #return self.user.username


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    message = models.CharField(max_length=255)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message