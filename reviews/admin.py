from django.contrib import admin
from .models import Review


class RatingFilter(admin.SimpleListFilter):
    title = "Filter by rating"

    parameter_name = "good_or_bad"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, reviews):
        good_or_bad = self.value()
        if good_or_bad == "good":
            return reviews.filter(rating__gte=3)
        elif good_or_bad == "bad":
            return reviews.filter(rating__lt=3)
        else:
            return reviews


# WordFilter 클래스를 별도의 파일에 저장한 후 임포트하여 사용해도 됨
class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"

    parameter_name = "word"  # /?word=good 형식으로 url에 붙게 됨

    # lookups: 필터에서 선택하는 부분을 보여주는 부분에 해당, 필수 구현!!!
    # Must be overridden to return a list of tuples (value, verbose value)
    def lookups(
        self, request, model_admin
    ):  # request: 사용하고 있는 유저 정보, model_admin: lookups를 사용하는 모델
        return [
            # 튜플의 첫 번째는 url에 포함되는 부분
            # 튜플의 두 번째는 관리자 페이지에 실제로 보여지는 라벨
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):  # reviews는 세 번째 인자인 queryset에 해당
        # # 모든 리뷰를 확인할 수 있음
        # print(reviews)
        # print(dir(request))
        # # url에서 쿼리를 받아옴. 딕셔너리 형태의 QueryDict로 받아옴. <QueryDict: {'word': ['good']}>
        # print(request.GET)
        # # 장고는 준비되어 있어 별도의 코딩 없이 필터링 값만 직접 받을 수 있음. good
        # print(self.value())
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        # "__str__": __str__ 메서드의 반환값을 보여줌
        "__str__",
        "payload",
    )
    list_filter = (
        # 위에서부터 차례대로 필터링하므로 필터링 순서에 따라 결과가 달라질 수 있음
        WordFilter,
        RatingFilter,
        "rating",
        "user__is_host",  # user는 review model의 Foreign Key
        # room은 Review Model의 Foreign Key
        # category는 Room Model의 Foreign Key
        "room__category",
        "room__pet_friendly",
    )
