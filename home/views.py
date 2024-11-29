from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from .forms import UserProfileForm

class HomePageView(TemplateView):
    template_name = "home/home.html"


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=profile)

    template = 'home/profile.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
