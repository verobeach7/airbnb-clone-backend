# 장고에서 기본으로 제공하는 TestCase Class가 있음. 이걸 사용하지 않을 것!
# from django.test import TestCase
# Django REST Framework에서 제공하는 TestCase Class가 있음. 단축 기능이 많아서 좋음!
from rest_framework.test import APITestCase


# APITestCase에는 유용한 메서드들이 많이 있음
class TestAmenities(APITestCase):
    # 모든 테스트를 한번에 테스트 하기 위해서는 APITestCase Class 안의 Method 명명 규칙을 숙지하고 있어야 함
    # 메서드 이름이 반드시 `test_`로 시작해야 함. `test_`로 시작하지 않으면 장고는 그 Test 코드를 실행하지 않음
    # self는 APITestCase Class를 가리킴
    def test_two_plus_two(self):
        # self.을 찍어보면 엄청 많은 메서드들이 보이는데 이 중 assert로 시작하는 것은 결과가 참임을 가정. assertIsNot은 거짓임을 가정.
        self.assertEqual(2 + 2, 5, "The math is wrong")

        # client는 API Client를 말하는 것으로 API 서버로 request를 보낼 수 있게 함
        # URL을 넣어주면 마치 브라우저에서 접근하는 것 처럼 request를 전송
