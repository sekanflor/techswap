# TechSwap API

TechSwap is a Django-based API for managing user profiles, PC component listings, and swap requests.

## Authentication

Use JWT for all endpoints.

### 🔐 Login
**POST** `/api/token/`

**Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "jwt-access-token",
  "refresh": "jwt-refresh-token"
}
```

**Header:**  
`Authorization: Bearer <access_token>`

---

## Endpoints

### 👤 UserProfile

#### List UserProfiles
**GET** `/api/user-profiles/`

**Response:**
```json
[
  {
    "id": 1,
    "user": 1,
    "bio": "Sample bio",
    "location": "Sample location"
  }
]
```

#### Create UserProfile
**POST** `/api/user-profiles/`

**Body:**
```json
{
  "user": 1,
  "bio": "New bio",
  "location": "New location"
}
```

**Response:**
```json
{
  "id": 2,
  "user": 1,
  "bio": "New bio",
  "location": "New location"
}
```

#### Retrieve UserProfile
**GET** `/api/user-profiles/<id>/`

**Response:**
```json
{
  "id": 1,
  "user": 1,
  "bio": "Sample bio",
  "location": "Sample location"
}
```

#### Update UserProfile
**PUT** `/api/user-profiles/<id>/`

**Body:**
```json
{
  "bio": "Updated bio",
  "location": "Updated location"
}
```

**Response:**
```json
{
  "id": 1,
  "user": 1,
  "bio": "Updated bio",
  "location": "Updated location"
}
```

#### Delete UserProfile
**DELETE** `/api/user-profiles/<id>/`

**Response:** `204 No Content`

---

### 📦 Listings

#### List Listings
**GET** `/api/listings/`

**Response:**
```json
[
  {
    "id": 1,
    "owner": 1,
    "title": "Sample Listing",
    "description": "Sample description",
    "category": "Sample category",
    "created_at": "2023-01-01T00:00:00Z"
  }
]
```

#### Create Listing (Sample via Postman)
**POST** `/api/listings/`
- **Headers:**
  - `Authorization: Bearer <access_token>`
  - `Content-Type: application/json`
- **Body:**
```json
{
  "owner": 1,
  "title": "Sample Listing",
  "description": "Brand new item for swap",
  "category": "Electronics"
}
```

**Response:**
```json
{
  "id": 2,
  "owner": 1,
  "title": "Sample Listing",
  "description": "Brand new item for swap",
  "category": "Electronics",
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Retrieve Listing
**GET** `/api/listings/<id>/`

**Response:**
```json
{
  "id": 1,
  "owner": 1,
  "title": "Sample Listing",
  "description": "Sample description",
  "category": "Sample category",
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Update Listing
**PUT** `/api/listings/<id>/`

**Body:**
```json
{
  "title": "Updated Listing",
  "description": "Updated description",
  "category": "Updated category"
}
```

**Response:**
```json
{
  "id": 1,
  "owner": 1,
  "title": "Updated Listing",
  "description": "Updated description",
  "category": "Updated category",
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Delete Listing
**DELETE** `/api/listings/<id>/`

**Response:** `204 No Content`

---

### 🔄 SwapRequests

#### List SwapRequests
**GET** `/api/swap-requests/`

**Response:**
```json
[
  {
    "id": 1,
    "listing": 1,
    "requester": 1,
    "status": "Pending",
    "message": "Sample message",
    "created_at": "2023-01-01T00:00:00Z"
  }
]
```

#### Create SwapRequest (Sample via Postman)
**POST** `/api/swap-requests/`
- **Headers:**
  - `Authorization: Bearer <access_token>`
  - `Content-Type: application/json`
- **Body:**
```json
{
  "listing": 1,
  "requester": 1,
  "status": "Pending",
  "message": "Interested to swap!"
}
```

**Response:**
```json
{
  "id": 2,
  "listing": 1,
  "requester": 1,
  "status": "Pending",
  "message": "Interested to swap!",
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Retrieve SwapRequest
**GET** `/api/swap-requests/<id>/`

**Response:**
```json
{
  "id": 1,
  "listing": 1,
  "requester": 1,
  "status": "Pending",
  "message": "Sample message",
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Update SwapRequest
**PUT** `/api/swap-requests/<id>/`

**Body:**
```json
{
  "status": "Approved",
  "message": "Updated message"
}
```

**Response:**
```json
{
  "id": 1,
  "listing": 1,
  "requester": 1,
  "status": "Approved",
  "message": "Updated message",
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Delete SwapRequest
**DELETE** `/api/swap-requests/<id>/`

**Response:** `204 No Content`

---

## Using Postman

1. **Get a JWT Token:**
   - POST to `/api/token/` with your username and password.
   - Copy the `access` token from the response.
2. **Add Authorization Header:**
   - In your request, add a header:
     - `Authorization: Bearer <access_token>`
3. **Set Content-Type:**
   - `Content-Type: application/json`
4. **Send your request!**

---

## Troubleshooting

- **401 Unauthorized:**
  - Make sure you included the correct JWT token in the `Authorization` header.
  - Generate a new token if expired.
- **500 Internal Server Error:**
  - Check if you have run migrations (`python manage.py makemigrations` and `python manage.py migrate`).
  - Make sure your database is running and accessible.
- **ProgrammingError: relation ... does not exist:**
  - Run migrations to create the necessary tables.
- **Empty list response:**
  - This is normal if there is no data yet in the table.

---

## Admin Panel
- Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) to view and manage users, user profiles, listings, and swap requests.

---

For more details, see the code and comments in each endpoint or contact the project maintainer.
