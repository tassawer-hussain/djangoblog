from django.db import models
from django.utils import timezone
from django.conf import settings # use for user model in author field

# Create your models here.
class Post(models.Model):

	class Status(models.TextChoices):
		DRAFT = 'DF', 'Draft'
		PUBLISHED = 'PB', 'Published'

	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250)
	body = models.TextField()

	# publish = models.DateTimeField(db_default=Now()) ## used db generate default value
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE, # delete all posts if user is deleted. It's SQL specific.
		related_name='blog_posts'
		)

	class Meta:
		ordering = ['-publish']
		indexes = [
			models.Index(fields=['-publish']),
		]

	def __str__(self):
		return self.title