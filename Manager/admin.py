from django.contrib import admin
from .models import myuser
from django.contrib.auth.models import User

# Register your models here.
def apply_ranker(modeladmin, request, queryset):
    for user in queryset:
        user.ranker = True
        user.save()
apply_ranker.short_description = 'Ranker로 등록하기'

def disapply_ranker(modeladmin, request, queryset):
    for user in queryset:
        user.ranker = False
        user.save()
disapply_ranker.short_description = 'Ranker를 해제하기'

class UserAdmin(admin.ModelAdmin):
	list_display = ['username','first_name','score_one','rank_one','score_three','rank_three','ranker']
	list_filter = ['score_one','score_three']
	actions = [apply_ranker, disapply_ranker,]

admin.site.register(myuser, UserAdmin)
admin.site.register(User)
