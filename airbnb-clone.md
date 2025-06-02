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

[v] GET POST /categories
[v] GET(Rooms) PUT DELETE /categories/1

### Rooms

[v] GET POST /rooms
[v] GET PUT DELETE /rooms/1
[v] GET /rooms/1/amenities
[v] GET /rooms/1/reviews
GET POST /rooms/1/bookings
GET PUT DELETE /rooms/1/bookings/2
[v] GET POST /amenities
[v] GET PUT DELETE /amenities/1
POST /rooms/1/photos
DELETE /rooms/1/photos/1

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

### Reviews

POST /reviews

### Wishlists

GET POST /wishlists
GET PUT DELETE /wishlists/1
