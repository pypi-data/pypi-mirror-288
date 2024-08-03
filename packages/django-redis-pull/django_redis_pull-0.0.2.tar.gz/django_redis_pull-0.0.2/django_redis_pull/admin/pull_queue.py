from django.contrib import admin

from ..models import PullQueue as Model


class ModelAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
    ]


admin.site.register(Model, ModelAdmin)
