from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from core.forms import HomeForm
from core.models import Post, Friend

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get(self, request):
        form = HomeForm()
        #posts = Post.objects.all()
        posts = Post.objects.all().order_by('-created')
        users = User.objects.exclude(pk=request.user.pk)
        friends = []
        if Friend.objects.filter(me=request.user).exists():
            friends = Friend.objects.get(me=request.user).users.all()
        args = {'form': form, 'posts':posts, 'users': users, 'friends': friends}

        return render(request, self.template_name, args)

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # will do something with that object
            post.user = request.user
            post.save()
            text = form.cleaned_data['post']
            users = User.objects.exclude(pk=request.user.pk)
            # return redirect('ui:profile')
            args = {'form': form, 'text': text, 'users': users}
            return render(request, self.template_name, args)


def friending(request, operation, pk):
    new_friend = Friend.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, new_friend)

    elif operation == 'remove':
        Friend.unfriend(request.user, new_friend)

    return redirect('core:home')
