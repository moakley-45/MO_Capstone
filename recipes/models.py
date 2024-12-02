from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"), (2, "Archived"))

CUISINE_CHOICES = (
    ('NON', 'Non-specific'),
    ('BRI', 'British Cuisine'),
    ('ITA', 'Italian Cuisine'),
    ('MID', 'Middle Eastern Cuisine'),
    ('ETH', 'Ethiopian Cuisine'),
    ('AME', 'American Cuisine'),
    ('MEX', 'Mexican Cuisine'),
    ('CAR', 'Caribbean Cuisine'),
    ('IND', 'Indian Cuisine'),
    ('THA', 'Thai Cuisine'),
)

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    creator = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name="recipes"
    )
    image = CloudinaryField('image', default='placeholder')
    notes = models.TextField()
    ingredients = models.TextField()
    method = models.TextField()
    serves = models.IntegerField()
    cuisine = models.CharField(max_length=3, choices=CUISINE_CHOICES, default='NON')
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | created by {self.creator}"

class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipe_reviews")
    title = models.CharField(max_length=200)
    image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(6)])
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Review by {self.author} on {self.recipe.title}"

class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_comments")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Comment by {self.author} on {self.review.title}"