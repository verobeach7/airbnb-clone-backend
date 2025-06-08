import strawberry

# config/schema.py에 rooms/schema.py 연결
from rooms import schema as rooms_schema


# Concept: config/urls.py에 모든 앱의 urls.py를 다 연결하는 것과 같은 방식임
# Query가 rooms_schema.Query를 다 상속(Inherit) 받게 됨
@strawberry.type
# class Query(rooms_schema.Query, users_schema.Query):
# 만든 각 앱의 Query들을 다 상속 받아 모두 섞어서 사용
class Query(rooms_schema.Query):
    pass


@strawberry.type
class Mutation:
    pass


schema = strawberry.Schema(
    query=Query,
    # mutation은 아직 코딩하지 않았으므로 잠시 주석처리
    # mutation=Mutation,
)

# 여기서 만든 Strawberry API를 어떻게 User에게 보여줄 것인가?
# config/urls.py에서 보여주면 됨
