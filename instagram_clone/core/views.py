from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, ChatMessage
from django.db.models import Q

@login_required
def post_list(request):
    posts = Post.objects.all()
    messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('timestamp')
    users = User.objects.exclude(username=request.user.username)
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        message = request.POST.get('message')
        receiver = User.objects.get(id=receiver_id)
        ChatMessage.objects.create(sender=request.user, receiver=receiver, message=message)
        return redirect('post_list')
    return render(request, 'core/post_list.html', {'posts': posts, 'messages': messages, 'users': users})

@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        comment = Comment.objects.create(post=post, author=request.user, text=text)
        return redirect('post_list')
    return render(request, 'core/add_comment.html', {'post': post})

@login_required
def chat(request, username):
    other_user = User.objects.get(username=username)
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) | 
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    if request.method == 'POST':
        message = request.POST.get('message')
        ChatMessage.objects.create(sender=request.user, receiver=other_user, message=message)
        return redirect('chat', username=username)
    return render(request, 'core/chat.html', {'messages': messages, 'other_user': other_user})


