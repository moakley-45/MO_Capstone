from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe 


class HomePageView(TemplateView):
    template_name = "home/home.html"

@login_required
def profile(request):
    """ Display the user's profile. """
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
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
 
