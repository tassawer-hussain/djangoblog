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
		# db_table = 'blog_posts' # can use to give a custom table name

	def __str__(self):
		return self.title

'''
Create and save post using python shell
from django.contrib.auth.models import User
from blog.models import Post
user = User.objects.get(username="tassawer.hussain")
post = Post(title="Hello World", slug="hello-world", body="This is a test post", author=user)
post.save()

Post.objects.create(							-	This create method, create and save the object in 1 step.
	title="one more post",
	slug="one-more-post",
	body="Post body of another post",
	author=user
	)
	
user, created = User.objects.get_or_create(username="admin")	-	attempts to retrieve a User object with the username admin, and if it doesn’t exist, it will create one. This get_or_create method return a tuple

post.title = "New title"				-	Update the title to something diffrent on the object in memory and save it to update the record in database
post.save()								-	This time the save() method performs an update SQL statement

all_posts = Post.objects.all()			-	get all posts
posts = Post.objects.filter(title="who was Django Reinhardt?")		-	Return all post that match the exact title

## Field lookups
Post.objects.filter(id=1)								-	When no specific lookup type is provided, default is exact. Return all posts that match the id
Post.objects.filter(id__exact=1)						-	Return all posts that match the exact id
Post.objects.filter(id__gt=1)							-	Return all posts that are greater than the id
Post.objects.filter(id__gte=1)							-	Return all posts that are greater than or equal to the id
Post.objects.filter(id__lt=1)							-	Return all posts that are less than the id
Post.objects.filter(id__lte=1)							-	Return all posts that are less than or equal to the id
Post.objects.filter(id__in=[1, 2, 3])					-	Return all posts that are in the list
Post.objects.filter(id__not_in=[1, 2, 3])				-	Return all posts that are not in the list
Post.objects.filter(id__isnull=True)					-	Return all posts that are null
Post.objects.filter(id__isnull=False)					-	Return all posts that are not null
Post.objects.filter(title__exact="Hello World")			-	Return all posts that match the exact title
Post.objects.filter(title__contains="Hello")			-	Return all posts that contain the word "Hello" in the title
Post.objects.filter(title__icontains="Hello")			-	Return all posts that contain the word "Hello" in the title - case insensitive
Post.objects.filter(title__startswith="Hello")			-	Return all posts that start with the word "Hello" in the title
Post.objects.filter(title__istartswith="Hello")			-	Return all posts that start with the word "Hello" in the title - case insensitive
Post.objects.filter(title__endswith="World")			-	Return all posts that end with the word "World" in the title
Post.objects.filter(title__iendswith="World")			-	Return all posts that end with the word "World" in the title - case insensitive
Post.objects.filter(title__iexact="Hello World")		-	Return all posts that match the exact title - case insensitive
Post.objects.filter(title__iregex="^Hello")				-	Return all posts that start with the word "Hello" in the title
Post.objects.filter(title__iregex="World$")				-	Return all posts that end with the word "World" in the title
Post.objects.filter(title__iregex="^Hello.*World$")		-	Return all posts that start with the word "Hello" and end with the word "World" in the title

## Date Lookups
from datetime import date
Post.objects.filter(publish__date=date(2025, 10, 30))	-	Return all posts that match the exact date
Post.objects.filter(publish__year=2025)					-	Return all posts that match the exact year
Post.objects.filter(publish__month=10)					-	Return all posts that match the exact month
Post.objects.filter(publish__day=30)					-	Return all posts that match the exact day
Post.objects.filter(publish__week_day=3)				-	Return all posts that match the exact week day
Post.objects.filter(publish__date__gte=date(2025, 10, 30))	-	Return all posts that are greater than or equal to the date
Post.objects.filter(publish__date__lte=date(2025, 10, 30))	-	Return all posts that are less than or equal to the date
Post.objects.filter(publish__date__gt=date(2025, 10, 30))	-	Return all posts that are greater than the date
Post.objects.filter(publish__date__lt=date(2025, 10, 30))	-	Return all posts that are less than the date
Post.objects.filter(publish__date__range=[date(2025, 10, 30), date(2025, 10, 31)])	-	Return all posts that are between the date range
Post.objects.filter(publish__date__year=2025)				-	Return all posts that match the exact year
Post.objects.filter(publish__date__month=10)				-	Return all posts that match the exact month
Post.objects.filter(publish__date__day=30)					-	Return all posts that match the exact day
Post.objects.filter(publish__date__week_day=3)			-	Return all posts that match the exact week day

## Lookup related objects fields
Post.objects.filter(author__username="tassawer.hussain")	-	Return all posts that match the exact username
Post.objects.filter(author__username__exact="tassawer.hussain")	-	Return all posts that match the exact username
Post.objects.filter(author__username__contains="tassawer")	-	Return all posts that contain the word "tassawer" in the username
Post.objects.filter(author__username__icontains="tassawer")	-	Return all posts that contain the word "tassawer" in the username - case insensitive
Post.objects.filter(author__username__startswith="tassawer")	-	Return all posts that start with the word "tassawer" in the username
Post.objects.filter(author__username__istartswith="tassawer")	-	Return all posts that start with the word "tassawer" in the username - case insensitive
Post.objects.filter(author__username__endswith="hussain")	-	Return all posts that end with the word "hussain" in the username
Post.objects.filter(author__username__iendswith="hussain")	-	Return all posts that end with the word "hussain" in the username - case insensitive
Post.objects.filter(author__username__iexact="tassawer.hussain")	-	Return all posts that match the exact username - case insensitive
Post.objects.filter(author__username__iregex="^tassawer.*hussain$")	-	Return all posts that start with the word "tassawer" and end with the word "hussain" in the username

## Filter by multiple fields
Post.objects.filter(title__exact="Hello World", status="PB")	-	Return all posts that match the exact title and status
Post.objects.filter(title__exact="Hello World", status="PB", author__username="tassawer.hussain")	-	Return all posts that match the exact title, status, and username
Post.objects.filter(publish__year=2025, author__username="tassawer.hussain")	-	Return all posts that match the exact year and username
Post.objects.filter(publish__year=2025, author__username="tassawer.hussain", status="PB")	-	Return all posts that match the exact year, username, and status
Post.objects.filter(publish__year=2025, author__username="tassawer.hussain", status="PB", title__exact="Hello World")	-	Return all posts that match the exact year, username, status, and title
Post.objects.filter(publish__year=2025, author__username="tassawer.hussain", status="PB", title__exact="Hello World", body__contains="Hello")	-	Return all posts that match the exact year, username, status, title, and body
Post.objects.filter(publish__year=2025, author__username="tassawer.hussain", status="PB", title__exact="Hello World", body__contains="Hello")	-	Return all posts that match the exact year, username, status, title, and body

## Chaining Filters
Post.objects.filter(title__exact="Hello World").filter(status="PB")	-	Return all posts that match the exact title and status
Post.objects.filter(title__exact="Hello World").filter(status="PB").filter(author__username="tassawer.hussain")	-	Return all posts that match the exact title, status, and username
Post.objects.filter(publish__year=2025).filter(author__username="tassawer.hussain")	-	Return all posts that match the exact year and username
Post.objects.filter(publish__year=2025).filter(author__username="tassawer.hussain").filter(status="PB")	-	Return all posts that match the exact year, username, and status
Post.objects.filter(publish__year=2025).filter(author__username="tassawer.hussain").filter(status="PB").filter(title__exact="Hello World")	-	Return all posts that match the exact year, username, status, and title
Post.objects.filter(publish__year=2025).filter(author__username="tassawer.hussain").filter(status="PB").filter(title__exact="Hello World").filter(body__contains="Hello")	-	Return all posts that match the exact year, username, status, title, and body
Post.objects.filter(publish__year=2025).filter(author__username="tassawer.hussain").filter(status="PB").filter(title__exact="Hello World").filter(body__contains="Hello")	-	Return all posts that match the exact year, username, status, title, and body

## Excluding Objects
Post.objects.filter(publish__year=2025).exclude(title__startswith="Hello")	-	Return all posts that do not start with the word "Hello" in the title
Post.objects.exclude(title__exact="Hello World")	-	Return all posts that do not match the exact title
Post.objects.exclude(title__exact="Hello World").exclude(status="PB")	-	Return all posts that do not match the exact title and status
Post.objects.exclude(title__exact="Hello World").exclude(status="PB").exclude(author__username="tassawer.hussain")	-	Return all posts that do not match the exact title, status, and username
Post.objects.exclude(publish__year=2025)	-	Return all posts that do not match the exact year
Post.objects.exclude(publish__year=2025).exclude(author__username="tassawer.hussain")	-	Return all posts that do not match the exact year and username
Post.objects.exclude(publish__year=2025).exclude(author__username="tassawer.hussain").exclude(status="PB")	-	Return all posts that do not match the exact year, username, and status
Post.objects.exclude(publish__year=2025).exclude(author__username="tassawer.hussain").exclude(status="PB").exclude(title__exact="Hello World")	-	Return all posts that do not match the exact year, username, status, and title
Post.objects.exclude(publish__year=2025).exclude(author__username="tassawer.hussain").exclude(status="PB").exclude(title__exact="Hello World").exclude(body__contains="Hello")	-	Return all posts that do not match the exact year, username, status, title, and body
Post.objects.exclude(publish__year=2025).exclude(author__username="tassawer.hussain").exclude(status="PB").exclude(title__exact="Hello World").exclude(body__contains="Hello")	-	Return all posts that do not match the exact year, username, status, title, and body

## Ordering Objects - Ascending order is default. '-' is used to order the objects in descending order.
Post.objects.order_by('title')	-	Return all posts ordered by the title
Post.objects.order_by('-title')	-	Return all posts ordered by the title in descending order
Post.objects.order_by('title', 'publish')	-	Return all posts ordered by the title first and then publish
Post.objects.order_by('-title', '-publish')	-	Return all posts ordered by the title and publish in descending order
Post.objects.order_by('?')	-	Return all posts ordered randomly

## Limiting Objects - Note that negative indexing is not supported.
Post.objects.all()[:5]	-	Return the first 5 posts
Post.objects.all()[5:10]	-	Return the posts from 6 to 10 - SQL OFFSET 5 LIMIT 10
Post.objects.all()[10:]	-	Return the posts from 11 to the end
Post.objects.all()[:10:2]	-	Return the posts from 0 to 10 with a step of 2
Post.objects.all()[::2]	-	Return the posts with a step of 2
Post.objects.all()[::-1]	-	Return the posts in reverse order
Post.objects.order_by('?')[0]	-	Retrieve the first random post - So we can use an index instead.

## Counting Objects - This method translates to a SELECT COUNT(*)  SQL statement.
Post.objects.count()	-	Return the number of posts
Post.objects.filter(title__exact="Hello World").count()	-	Return the number of posts that match the exact title
Post.objects.filter(id__lte=3).count()	-	Return the number of posts that have an id less than or equal to 3

## Checking if an object exists - Returns a boolean (True/False) value.
Post.objects.filter(id=1).exists()	-	Return True if the post with the id 1 exists, False otherwise
Post.objects.filter(title__startswith="Hello").exists()	-	Return True if the post with the title that starts with "Hello" exists, False otherwise

## Deleting Objects - This method translates to a DELETE SQL statement.
## Note that deleting objects will also delete any dependent relationships for ForeignKey  objects defined with on_delete set to CASCADE.
Post.objects.filter(id=1).delete()	-	Delete the post with the id 1
Post.objects.filter(title__startswith="Hello").delete()	-	Delete the posts with the title that starts with "Hello"
post = Post.objects.get(id=1)	-	Get the post with the id 1
post.delete()					-	Delete the post object

## Complex lookups with Q objects - Use to build the OR relationship between filters.
## You can compose statements by combining Q objects with the & (and), | (or), and ^ (xor) operators.
from django.db.models import Q
Post.objects.filter(Q(title__startswith="Hello") & Q(title__endswith="World"))	-	Return all posts that start with "Hello" and end with "World" in the title

## Following code retrieves posts with a title that starts with the string who or why (case-insensitive):
from django.db.models import Q
starts_who = Q(title__istartswith="who")
starts_why = Q(title__istartswith="why")
Post.objects.filter(starts_who | starts_why)	-	Return all posts that start with "who" or "why" in the title
Post.objects.filter(starts_who & starts_why)	-	Return all posts that start with "who" and "why" in the title
Post.objects.filter(starts_who ^ starts_why)	-	Return all posts that start with "who" or "why" in the title but not both
'''