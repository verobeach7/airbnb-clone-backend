# 장고에서 기본으로 제공하는 TestCase Class가 있음. 이걸 사용하지 않을 것!
# from django.test import TestCase
# Django REST Framework에서 제공하는 TestCase Class가 있음. 단축 기능이 많아서 좋음!
from rest_framework.test import APITestCase
from rooms import models
from users.models import User


# APITestCase에는 유용한 메서드들이 많이 있음
class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Description"
    URL = "/api/v1/rooms/amenities/"

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
        response = self.client.get(self.URL)
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

    def test_create_amenity(self):
        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity Description"

        response = self.client.post(
            self.URL,
            data={
                "name": new_amenity_name,
                "description": new_amenity_description,
            },
        )
        data = response.json()
        # print(data)  # {'name': 'New Amenity', 'description': 'New Amenity Description'}
        # print(type(data))  # <class 'dict'>
        # print(data["name"])  # New Amenity
        # print(data.get("name"))  # New Amenit: 더 안전한 방식!

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )

        self.assertEqual(
            data["name"],
            new_amenity_name,
        )
        self.assertEqual(
            data["description"],
            new_amenity_description,
        )

        # 데이터 없이 POST Request를 보내는 경우: name과 description 모두 없음
        response = self.client.post(self.URL)
        data = response.json()

        # 데이터 없이 보내면 name은 필수 입력이므로 에러가 발생
        # 데이터가 없으면 400 응답을 잘 보내는지 확인
        self.assertEqual(response.status_code, 400)
        # 에러 메시지 안에 name이라는 키워드가 있는지 확인
        self.assertIn("name", data)


class TestAmenity(APITestCase):
    NAME = "Test Amenity"
    DESC = "Test Description"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_found(self):
        # 해당 Amenity가 존재하지 않는 경우
        response = self.client.get("/api/v1/rooms/amenities/2")

        self.assertEqual(response.status_code, 404)  # 404: NotFound

    def test_get_amenity(self):

        # 해당 Amenity가 존재하는 경우
        response = self.client.get("/api/v1/rooms/amenities/1")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(
            data["name"],
            self.NAME,
        )
        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_put_amenity(self):
        updated_amenity_name = "Updated Amenity"
        updated_amenity_description = "Updated Amenity Description"

        response = self.client.put(
            "/api/v1/rooms/amenities/1",
            data={
                "name": updated_amenity_name,
            },
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            data["name"],
            updated_amenity_name,
        )

        response = self.client.put(
            "/api/v1/rooms/amenities/1",
            data={
                "description": updated_amenity_description,
            },
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            data["description"],
            updated_amenity_description,
        )

        response = self.client.put(
            "/api/v1/rooms/amenities/1",
            data={
                "name": updated_amenity_name,
                "description": updated_amenity_description,
            },
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )

        invalid_name = "name" * 40

        response = self.client.put(
            "/api/v1/rooms/amenities/1",
            data={
                "name": invalid_name,
                # "description": invalid_desc,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )

    def test_delete_amenity(self):

        response = self.client.delete("/api/v1/rooms/amenities/1")

        self.assertEqual(response.status_code, 204)


class TestRooms(APITestCase):
    def setUp(self):
        # 계정 생성
        user = User.objects.create(
            username="test",
        )
        user.set_password("123")  # password 설정도 테스트에서는 꼭 하지 않아도 됨
        user.save()
        self.user = user  # user 객체를 생성하여 Class 내부에 저장해주기만 하면 됨

    def test_create_room(self):

        response = self.client.post("/api/v1/rooms/")
        print(response.json())

        # 로그인 되지 않은 상태에서는 403 에러가 발생함
        self.assertEqual(response.status_code, 403)

        # # 계정 생성 및 로그인
        # # 계정 생성 -> setUp()로 이동
        # user = User.objects.create(
        #     username="test",
        # )
        # user.set_password("123")
        # user.save()
        # # 로그인 -> username과 password 기억할 필요 없음: 강제 로그인 시키면 됨
        # self.client.login(
        #     username="test",
        #     password="123",
        # )

        # 강제 로그인
        # 다른 부분은 강제 로그인하여 테스트하면 되지만 User를 생성하는 단계를 테스트 할 때는 강제 로그인이 아닌 각 과정을 테스트 해야 함
        self.client.force_login(
            self.user,
        )

        response = self.client.post("/api/v1/rooms/")
        print(response.json())
