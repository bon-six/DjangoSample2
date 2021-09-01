from django.contrib import admin

from .models import Question, Choice, Vote

class ReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date')

admin.site.register(Question, QuestionAdmin)


class VoteAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('voter_name', 'vote_date', 'choice')
admin.site.register(Vote, VoteAdmin)