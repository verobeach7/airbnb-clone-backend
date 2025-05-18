from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        # "__str__": __str__ 메서드의 반환값을 보여줌
        "__str__",
        "payload",
    )
    list_filter = ("rating",)
