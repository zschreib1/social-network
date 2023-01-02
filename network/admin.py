from django.contrib import admin
from .models import User, Post, FollowersCount, FollowingCount

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(FollowersCount)
admin.site.register(FollowingCount)