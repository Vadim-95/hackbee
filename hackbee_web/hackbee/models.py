from django.db import models
import datetime
# Create your models here.



class Zbgoodfind(models.Model):
	name = models.CharField(max_length = 20 , default="ZBGOODFIND")
	key = models.CharField(max_length=129,null=True)
	guesses = models.IntegerField(null=True)
	status_code = models.CharField(max_length=10,null=True)
	start_time = models.DateTimeField(auto_now_add=True, blank=True)


	def __str__(self):
		return self.name

class Zbconvert(models.Model):
	name = models.CharField(max_length = 20 , default="ZBCONVERT")
	status_code = models.CharField(max_length=10,null=True)
	start_time = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return self.name

class Zbreplay(models.Model):
	name = models.CharField(max_length = 20 , default="ZBREPLAY")
	status_code = models.CharField(max_length=10,null=True)
	results = models.IntegerField(null=True)
	start_time = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return self.name