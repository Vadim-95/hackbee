from django.db import models

# Create your models here.

class report(models.Model):
	time = models.DateTimeField()


class Zbgoodfind(models.Model):
	key = models.CharField(max_length=129,null=True)
	guesses = models.IntegerField(null=True)
	status_code = models.CharField(max_length=10,null=True)
	def __str__(self):
		return self.name

class Zbconvert(models.Model):
	status_code = models.CharField(max_length=10,null=True)
	def __str__(self):
		return self.name

class Zbreplay(models.Model):
	status_code = models.CharField(max_length=10,null=True)
	results = models.IntegerField(null=True)
	def __str__(self):
		return self.name
