from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated
from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
        )
        print(serializer.data)
        # [{'id': 1, 'created_at': '2025-05-17T11:59:41.156367+09:00', 'updated_at': '2025-05-17T11:59:41.156382+09:00', 'name': '여행 가방 보관 가능', 'description': '체크인 시간보다 일찍 도착하거나 체크아웃 후 짐 보관을 원하는 게스트를 위한 서비스'}, {'id': 2, 'created_at': '2025-05-17T12:00:08.629960+09:00', 'updated_at': '2025-05-17T12:00:08.629986+09:00', 'name': '장기 숙박 가능', 'description': '28일 이상 숙박 가능'}, {'id': 3, 'created_at': '2025-05-17T12:00:57.920259+09:00', 'updated_at': '2025-05-30T13:28:09.479454+09:00', 'name': '디지털도어록', 'description': '게스트가 현관문 비밀번호를 입력하여 직접 체크인합니다'}]
        return Response(serializer.data)

    def post(self, request):
        print("request.data", request.data)
        # request.data {'name': '멋진 뒷뜰', 'description': '꽃밭에서 놀아요'}
        serializer = AmenitySerializer(data=request.data)
        print("serializer", serializer)
        # serializer AmenitySerializer(data={'name': '멋진 뒷뜰', 'description': '꽃밭에서 놀아요'}):
        # id = IntegerField(label='ID', read_only=True)
        # created_at = DateTimeField(read_only=True)
        # updated_at = DateTimeField(read_only=True)
        # name = CharField(max_length=150)
        # description = CharField(allow_blank=True, allow_null=True, max_length=150, required=False)
        if serializer.is_valid():
            amenity = serializer.save()
            print("amenity", amenity)
            ### Python Object
            # amenity 멋진 뒷뜰
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        print("amenity", amenity)
        ### Python Object
        # amenity 멋진 도어록
        serializer = AmenitySerializer(amenity)
        print("serializer", serializer)
        # serializer AmenitySerializer(<Amenity: 멋진 도어록>):
        # id = IntegerField(label='ID', read_only=True)
        # created_at = DateTimeField(read_only=True)
        # updated_at = DateTimeField(read_only=True)
        # name = CharField(max_length=150)
        # description = CharField(allow_blank=True, allow_null=True, max_length=150, required=False)
        print("serializer.data", serializer.data)
        # JSON 변환됨
        # serializer.data {'id': 3, 'created_at': '2025-05-17T12:00:57.920259+09:00', 'updated_at': '2025-05-30T13:20:35.069248+09:00', 'name': '멋진 도어록', 'description': '게스트가 현관문 비밀번호를 입력하여 직접 체크인합니다'}
        return Response(serializer.data)
        # return Response(
        #     AmenitySerializer(self.get_object(pk)).data,
        # )

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        print("serializer", serializer)
        # serializer AmenitySerializer(<Amenity: 멋진 도어록>, data={'name': '디지털도어록'}, partial=True):
        # id = IntegerField(label='ID', read_only=True)
        # created_at = DateTimeField(read_only=True)
        # updated_at = DateTimeField(read_only=True)
        # name = CharField(max_length=150)
        # description = CharField(allow_blank=True, allow_null=True, max_length=150, required=False)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            print("updated_amenity", updated_amenity)
            # Python Object
            # updated_amenity 멋진 도어록
            print("after serializing", AmenitySerializer(updated_amenity).data)

            # after serializing {'id': 3, 'created_at': '2025-05-17T12:00:57.920259+09:00', 'updated_at': '2025-05-30T13:20:35.069248+09:00', 'name': '멋진 도어록', 'description': '게스트가 현관문 비밀번호를 입력하여 직접 체크인합니다'}
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        print(dir(request))
        # ['FILES', 'POST', '__class__', '__class_getitem__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__firstlineno__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__static_attributes__', '__str__', '__subclasshook__', '__weakref__', '_auth', '_authenticate', '_authenticator', '_content_type', '_data', '_default_negotiator', '_files', '_full_data', '_load_data_and_files', '_load_stream', '_not_authenticated', '_parse', '_request', '_stream', '_supports_form_parsing', '_user', 'accepted_media_type', 'accepted_renderer', 'auth', 'authenticators', 'content_type', 'csrf_processing_done', 'data', 'force_plaintext_errors', 'negotiator', 'parser_context', 'parsers', 'query_params', 'stream', 'successful_authenticator', 'user', 'version', 'versioning_scheme']
        print(dir(request.user))
        # ['CurrencyChoices', 'DoesNotExist', 'EMAIL_FIELD', 'GenderChoices', 'LanguageChoices', 'Meta', 'MultipleObjectsReturned', 'REQUIRED_FIELDS', 'USERNAME_FIELD', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__firstlineno__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__static_attributes__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_composite_pk', '_check_constraints', '_check_db_table_comment', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_field_expression_map', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_session_auth_hash', '_get_unique_checks', '_is_pk_set', '_meta', '_parse_save_params', '_password', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', '_state', '_validate_force_insert', 'acheck_password', 'adelete', 'aget_all_permissions', 'aget_group_permissions', 'aget_user_permissions', 'ahas_module_perms', 'ahas_perm', 'ahas_perms', 'arefresh_from_db', 'asave', 'avatar', 'bookings', 'chatting_rooms', 'check', 'check_password', 'clean', 'clean_fields', 'currency', 'date_error_message', 'date_joined', 'delete', 'email', 'email_user', 'experiences', 'first_name', 'from_db', 'full_clean', 'gender', 'get_all_permissions', 'get_constraints', 'get_currency_display', 'get_deferred_fields', 'get_email_field_name', 'get_full_name', 'get_gender_display', 'get_group_permissions', 'get_language_display', 'get_next_by_date_joined', 'get_previous_by_date_joined', 'get_session_auth_fallback_hash', 'get_session_auth_hash', 'get_short_name', 'get_user_permissions', 'get_username', 'groups', 'has_module_perms', 'has_perm', 'has_perms', 'has_usable_password', 'id', 'is_active', 'is_anonymous', 'is_authenticated', 'is_host', 'is_staff', 'is_superuser', 'language', 'last_login', 'last_name', 'logentry_set', 'messages', 'name', 'natural_key', 'normalize_username', 'objects', 'password', 'pk', 'prepare_database_save', 'refresh_from_db', 'reviews', 'rooms', 'save', 'save_base', 'serializable_value', 'set_password', 'set_unusable_password', 'unique_error_message', 'user_permissions', 'username', 'username_validator', 'validate_constraints', 'validate_unique', 'wishlists']
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                # owner, amenities, category를 Relationship에 있는 데이터로 read_only=True 설정하여 함
                # read_only=True 설정으로 인해 owner, amenities, category 데이터 없이도 유효성 검사를 통과함
                # 하지만 데이터베이스에 저장되기 위해서는 owner, amenities, category가 not null이기 때문에 반드시 주어져야 함
                # request.data 외에 데이터를 어딘가에서 받아 방을 생성할 수 있는 방법을 찾아야 함
                # models.py의 모델에 owner로 속성을 만들었기 때문에 반드시 owner로 보내야 함
                room = serializer.save(owner=request.user)
                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)
