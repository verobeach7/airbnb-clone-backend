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


### Resolover
# class 안에 있는 메서드가 아니기 때문에 self는 필요하지 않음
def movies():
    return movies_db


# 별도의 함수로 뺐기 때문에 self 없이 query argument만 있으면 됨
def movie(movie_pk: int):
    return movies_db[movie_pk - 1]


### Query
# 데코레이터(@)를 이용해 strawberry에게 type임을 알림
@strawberry.type
class Query:
    # Strawberry를 사용하면 반드시 타입을 명시해줘야 함
    # 이렇게 해주기만 하면 Qeury와 Resolver 등을 Strawberry가 알아서 다 만들어 줌
    # 반드시 ping을 field로 만들어 줘야 함: 데코레이터 이용
    # @strawberry.field
    # def movies(self) -> typing.List[Movie]:  # Type Annotation
    #     return movies_db
    movies: typing.List[Movie] = strawberry.field(resolver=movies)

    movie: Movie = strawberry.field(resolver=movie)


def add_movie(title: str, year: int, rating: int) -> Movie:
    new_movie = Movie(
        pk=len(movies_db) + 1,
        title=title,
        year=year,
        rating=rating,
    )
    # movies_db는 리스트이므로 .append 사용
    movies_db.append(new_movie)
    # 반드시 Movie 객체를 반환해야 함
    return new_movie


### Mutation
@strawberry.type
class Mutation:
    add_movie: Movie = strawberry.mutation(resolver=add_movie)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)

# 여기서 만든 Strawberry API를 어떻게 User에게 보여줄 것인가?
# config/urls.py에서 보여주면 됨
