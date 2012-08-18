from django.db import models

class Likes(models.Model):
	time = models.DateTimeField('datetime collected')
	company = models.CharField(max_length=32)
	num_likes = models.IntegerField()
	def __unicode__(self):
		return self.company


class LogMessages(models.Model):
	time = models.DateTimeField('datetime generated')
	msg_text = models.CharField(max_length=200)
	def __unicode__(self):
		return self.msg_text
