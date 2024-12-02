from recipes.models import CUISINE_CHOICES

def cuisine_choices(request):
    return {'CUISINE_CHOICES': CUISINE_CHOICES}