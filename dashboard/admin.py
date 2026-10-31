from django.contrib import admin
from .models import Builder, GalleryImage, Event, Project, ProjectImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'order', 'created_at')
    list_editable = ('order',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'location')


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'coming_soon', 'order')
    list_editable = ('order',)
    filter_horizontal = ('builders',)
    inlines = [ProjectImageInline]


@admin.register(Builder)
class BuilderAdmin(admin.ModelAdmin):
    list_display = ('name', 'major', 'year')
    search_fields = ('name',)
