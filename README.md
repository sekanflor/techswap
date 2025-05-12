# TechSwap API

TechSwap is a Django-based API for managing user profiles, PC component listings, and swap requests.

---

## Demo Superuser Account

For easy access during testing and grading, use the following superuser credentials:

```
Username: pc01
Password: ase12345
```

> **Note:** These credentials are for demo/testing purposes only.

---

## Table of Contents
- [Setup](#setup)
- [Rate Limiting](#rate-limiting)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [UserProfile](#userprofile)
  - [Listings](#listings)
  - [SwapRequests](#swaprequests)
- [File Upload](#file-upload)
- [Using Postman](#using-postman)
- [Troubleshooting](#troubleshooting)
- [Admin Panel](#admin-panel)
- [Contributing](#contributing)
- [License](#license)

---

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd techswap
   ```
2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install Pillow
   ```
4. **Configure your database settings in `techswap/settings.py` if needed.**
5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```
7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
8. **Access the API at** `http://localhost:8000/`

---

## Rate Limiting

All API endpoints are rate limited to **100 requests per minute per IP address**. If you exceed this limit, you will receive a 429 Too Many Requests response with the following format:

```json
{
    "error": "Rate limit exceeded",
    "message": "Too many requests. Please try again in X seconds."
}
```

### How to Test Rate Limiting

#### Using Postman
1. **Get a JWT Token**
   - Send a `POST` request to `http://localhost:8000/api/token/` with body:
     ```json
     {
         "username": "your_username",
         "password": "your_password"
     }
     ```
   - Copy the `access` token from the response.
2. **Create a GET request** to `http://localhost:8000/api/user-profiles/`.
   - Add headers:
     - `Authorization: Bearer <your_token>`
     - `Content-Type: application/json`
3. **Save the request to a collection**.
4. **Open the Collection Runner** (Runner button or Ctrl+R).
   - Set Iterations to 101
   - Set Delay to 100 ms
   - Click Run
5. **Observe the results**:
   - The first 100 requests should return status 200
   - The 101st request should return status 429 with the error message

#### Troubleshooting
- If you never see a 429 error:
  - Make sure you are not restarting the Django server during the test
  - Ensure you are using the same IP address for all requests (localhost/127.0.0.1)
  - If using Django's default cache, it may reset on server restart. For production, use Redis or Memcached.
  - Try lowering the limit in the decorator for testing (e.g., `requests=5`)
- If you see a 429 error, but not the expected JSON:
  - Make sure the decorator uses `JsonResponse` as shown in the codebase

---

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

## File Upload

The API supports profile photo uploads with the following specifications:
- Maximum file size: 2MB
- Allowed file types: JPEG, PNG, WebP
- Images are automatically cropped to a 1:1 aspect ratio

### Profile Photo Upload

#### Update Profile with Photo
**PUT** `/api/user-profiles/<id>/`

**Headers:**
- `Authorization: Bearer <access_token>`
- `Content-Type: multipart/form-data`

**Body:**
```json
{
    "bio": "Updated bio",
    "location": "Updated location",
    "photo": <file>
}
```

**Response:**
```json
{
    "id": 1,
    "user": 1,
    "bio": "Updated bio",
    "location": "Updated location",
    "photo": "/media/profile_photos/photo.jpg"
}
```

#### Create Profile with Photo
**POST** `/api/user-profiles/`

**Headers:**
- `Authorization: Bearer <access_token>`
- `Content-Type: multipart/form-data`

**Body:**
```json
{
    "user": 1,
    "bio": "New bio",
    "location": "New location",
    "photo": <file>
}
```

**Response:**
```json
{
    "id": 2,
    "user": 1,
    "bio": "New bio",
    "location": "New location",
    "photo": "/media/profile_photos/photo.jpg"
}
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss what you would like to change.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
