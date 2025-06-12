# 장고에서 기본으로 제공하는 TestCase Class가 있음. 이걸 사용하지 않을 것!
# from django.test import TestCase
# Django REST Framework에서 제공하는 TestCase Class가 있음. 단축 기능이 많아서 좋음!
from rest_framework.test import APITestCase
from rooms import models


# APITestCase에는 유용한 메서드들이 많이 있음
class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Description"

    # setUp 메서드는 다른 모든 test들이 실행되기 전에 실행됨
    # 여기서 DB를 생성하고 테스트를 진행할 수 있음
    def setUp(self) -> None:
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    # 모든 테스트를 한번에 테스트 하기 위해서는 APITestCase Class 안의 Method 명명 규칙을 숙지하고 있어야 함
    # 메서드 이름이 반드시 `test_`로 시작해야 함. `test_`로 시작하지 않으면 장고는 그 Test 코드를 실행하지 않음
    # self는 APITestCase Class를 가리킴
    def test_all_amenities(self):
        # client는 API Client를 말하는 것으로 API 서버로 request를 보낼 수 있게 함
        # URL을 넣어주면 마치 브라우저에서 접근하는 것 처럼 request를 전송
        response = self.client.get("/api/v1/rooms/amenities/")
        data = response.json()

        # data가 없기 때문에 데이터 없이 테스트 할 수 있는 것들을 테스트 해야 함
        # rooms/amenities는 완전 공개 url이므로 누구나 접근 가능해야 함을 테스트
        # 데이터 없이도 누구나 접근 가능해 상태 코드가 200을 받음을 테스트 할 수 있음
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        # 데이터가 없어도 serializer.data는 리스트로 반환되어야 하므로 빈 리스트를 받는지 확인 가능
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESC)
