# AirBnb Clone Schedule

- All Models
  - Recap of Defaults and Relationship
  - Users
    - Profile Photo
    - Gender
    - Language
    - Currency Options
  - Abstract Model
  - Rooms
    - Country
    - City
    - Price Per Night
    - Description
    - Owner
    - Room #
    - Toilet #
    - Address
    - Pet Freindly
    - Category
    - Type of Place(Entire Place | Private Room | Shared Room)
    - Amenities(Many to Many)
      - Name
  - Experiences
    - Country
    - City
    - Name
    - Host
    - Price
    - Description
    - Address
    - Start Time
    - End Time
    - Category
    - Materials (Many to Many)
      - Name
      - Description
  - Categories
    - Kind (Room | Experience)
    - Name
  - Reviews
    - Review
    - Rating
    - Room
    - Experience
    - User
  - Wishlists
    - Name
    - Rooms
    - Experieces
    - User
  - Bookings
    - Kind (Room | Experience)
    - Room
    - Experience
    - Check In
    - Check Out
    - Experience Date
  - Photos
    - File
    - Description
    - Room
    - Experience
  - Messages
    - Room
      - Users
    - Message
      - Text
      - User
      - Room
- Admins for All
  - `search fields` Foreign Key
    - ^ istartswith
    - = iexact
    - @ search
    - None icontains
- Custom Filters

  - SimpleListFilter
  - Lookups
  - QuerySet

- Why API
- Installation
- Categories API
  - Without DRF
  - @api_view
  - Serializer
  - GET /categories
  - GET /categories/1
  - \*args, \*\*kwargs
  - POST /categories (.create)
  - PUT /categories/1 (.update)
  - ModelSerializer
  - APIView
  - DELETE /categories/1
  - ModelViewSet
- Amenities API
- Perks API
- Rooms API
  - Serializer Relationships
  - owner=request.user
- Experiences API
- Medias API
  - ImageField -> URLField
- Reviews API
- Wishlist API
- Bookings API
- Direct Messages API

### Extras To Do:

Dynamic Serializer Fields (is_liked)
Pagination

## API Planning:

### Categories

[x] GET POST /categories
[x] GET(Rooms) PUT DELETE /categories/1

### Rooms

[x] GET POST /rooms
[x] GET PUT DELETE /rooms/1
[x] GET /rooms/1/amenities
[x] GET /rooms/1/reviews
[x] GET POST /rooms/1/bookings
GET PUT DELETE /rooms/1/bookings/2
[x] GET POST /amenities
[x] GET PUT DELETE /amenities/1

##### 어떤 방에 관련된 사진인지 알아야 하기 때문에 아래 Route는 좋음

[x] POST /rooms/1/photos

##### 사진 삭제 시 아래 둘 중 어떤 것을 선택하는 것이 더 좋을까?

[x] DELETE /rooms/1/photos/1
[x] DELETE /medias/photos/1

### Experiences

GET POST /experiences
GET PUT DELETE /experiences/1
GET /experiences/1/perks
GET POST /experiences/1/bookings
GET PUT DELETE /experiences/1/bookings/2
GET POST /perks
GET PUT DELETE /perks/1

### Medias

POST /medias
DELETE /medias/1

### Users

POST /users
GET /users/rooms
GET /users/experiences
GET /users/bookings
GET PUT /users/1
GET /users/1/reviews

### Wishlists

[x] GET POST /wishlists - wishlist들을 만들고 가져오는데 사용
[x] GET PUT DELETE /wishlists/1 - wishlist 내에 room이나 experience의 세부정보를 가져오거나 업데이트하거나 삭제하는데 사용
[x] PUT /wishlists/1/rooms - serializer를 사용하지 않고 room의 id를 보내면 wishlist의 rooms 리스트에 id를 추가

- 방법1: url에 방의 pk를 포함하여 보냄: /wishlists/1/rooms/2
- 방법2: /wishlists/1/rooms url로 따로 데이터를 포함하여 전송: {"room_pk": 2}
  is_liked
