from django.contrib import admin
from .models import Task, Option, Test


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['text']


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['text']


@admin.register(Test)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['name']
