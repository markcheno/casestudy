from django.contrib import admin
from casestudy.models import Likes,LogMessages


class LikesAdmin(admin.ModelAdmin):
	fields = ['time', 'company', 'num_likes']
	list_display = ('time','company','num_likes')
	list_filter = ['company']

class LogMessagesAdmin(admin.ModelAdmin):
	fields = ['time','msg_text']
	list_display = ('time','msg_text')

admin.site.register(Likes,LikesAdmin)
admin.site.register(LogMessages,LogMessagesAdmin)