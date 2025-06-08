import strawberry

# Type Annotation(주석)을 추가할 수 있도록 해주는 패키지
# List 타입을 추가할 수 있도록 해 줌
import typing


# Movie Type
@strawberry.type
class Movie:
    pk: int
    title: str
    year: int
    rating: int


# Movie DB
movies_db = [
    Movie(pk=1, title="Godfather", year=1990, rating=10),
]


### Strawberry API
# 데코레이터(@)를 이용해 strawberry에게 type임을 알림
@strawberry.type
class Query:
    # Strawberry를 사용하면 반드시 타입을 명시해줘야 함
    # 이렇게 해주기만 하면 Qeury와 Resolver 등을 Strawberry가 알아서 다 만들어 줌
    # 반드시 ping을 field로 만들어 줘야 함: 데코레이터 이용
    @strawberry.field
    def movies(self) -> typing.List[Movie]:  # Type Annotation
        return movies_db

    @strawberry.field
    # movie_id라고 이름지어주면 Strawberry가 알아서 movieId라고 GraphQL 방식으로 이름지어줌
    def movie(self, movie_pk: int) -> Movie:
        return movies_db[movie_pk - 1]


schema = strawberry.Schema(query=Query)

# 여기서 만든 Strawberry API를 어떻게 User에게 보여줄 것인가?
# config/urls.py에서 보여주면 됨
