from django.contrib import admin
from .models import Experience, Perk
from categories.models import Category


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "start",
        "end",
        "created_at",
    )
    # category를 기준으로 필터링할 수 있음
    list_filter = ("category",)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ExperienceAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["category"].queryset = Category.objects.filter(
            kind="experiences"
        )
        return form


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "detail",
        "explanation",
    )
