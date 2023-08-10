from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views import View

from users.forms import UserRegisterForm
from users.models import Profile


class RegisterView(View):
    def get(self, request):

        try:
            user = User.objects.get(username=request.user.username)
            if user:
                return redirect('index')
        except:
            form = UserRegisterForm()
            return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form})


class CheckUsernameExists(View):
    def post(self, request):
        username = request.POST.get('username')

        if not len(username) > 2:
            return HttpResponse('<small style="color: red; padding-left: 4px">username too short</small>')
        else:
            invalid_chars = [' ', '!', '@', '#', '$',
                             '^', '&', '*', '(', ')', '-', '=', '+']
            if any(char in invalid_chars for char in username.strip()):
                return HttpResponse('<small style="color: red; padding-left: 4px">invalid username</small>')
            user = User.objects.filter(username=username.strip()).exists()
            if user:
                return HttpResponse('<small style="color: red; padding-left: 4px">username already taken</small>')

            else:
                return HttpResponse('<small style="color: green; padding-left: 4px">username avlaible</small>')


class PasswordResetView(View):
    def get(self, request):
        messages.error(request, 'mujhe bhi nhi pata, tu gaand mara!')
        return redirect('login')


class ProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        user_is_owner = False
        if user == request.user:
            user_is_owner = True
        profile = get_object_or_404(Profile, user=user)

        ctx = {
            'user_is_owner': user_is_owner,
            'profile': profile
        }
        return render(request, 'users/profile.html', ctx)
