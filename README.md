# TechSwap - Item Trading Platform

TechSwap is a Django REST Framework-based platform that allows users to trade items with each other. The platform includes features for user authentication, item listings, and swap requests.

## Features

### Authentication System

- User registration with email verification
- JWT-based authentication
- Secure password hashing
- Protected routes for authenticated users
- Token refresh mechanism

### User Management

- User profiles with customizable information
- Profile photo upload support
- Location-based user search

### File Uploads

#### Profile Photos

- Supported formats: JPEG, PNG, WebP
- Maximum file size: 2MB
- Photos are automatically cropped to square
- Upload during registration or profile update
- Files stored in: `/media/profile_photos/`

#### Registration with Photo

```http
POST /api/auth/register/
Content-Type: multipart/form-data

Fields:
- username: string
- password: string
- password2: string
- email: string
- first_name: string
- last_name: string
- photo: file (optional)
```

Example using Postman:

1. Create new request:
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/auth/register/`
   - Body: form-data
   ```
   username: your_username
   password: your_password
   password2: your_password
   email: your@email.com
   first_name: Your First Name
   last_name: Your Last Name
   photo: [select file] (set type as 'File')
   ```

Expected Response:

```json
{
  "user": {
    "username": "your_username",
    "email": "your@email.com",
    "first_name": "Your First Name",
    "last_name": "Your Last Name",
    "photo": "http://127.0.0.1:8000/media/profile_photos/your-photo.jpg"
  },
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Updating Profile Photo

```http
PUT /api/profiles/{id}/
Authorization: Bearer your_access_token
Content-Type: multipart/form-data

Fields:
- photo: file
- bio: string (optional)
- location: string (optional)
```

Example using Postman:

1. **First, get an access token:**

   - POST `http://127.0.0.1:8000/api/auth/token/`
   - Body (raw JSON):
     ```json
     {
       "username": "your_username",
       "password": "your_password"
     }
     ```

2. **Then update profile:**
   - PUT `http://127.0.0.1:8000/api/profiles/{id}/`
   - Headers:
     ```
     Authorization: Bearer your_access_token
     ```
   - Body: form-data
     ```
     photo: [select file] (set type as 'File')
     bio: Your bio text (optional)
     location: Your location (optional)
     ```

Example Response:

```json
{
  "id": 1,
  "user": 1,
  "bio": "Your bio text",
  "location": "Your location",
  "photo": "http://127.0.0.1:8000/media/profile_photos/your-photo.jpg"
}
```

Example using cURL:

```bash
# Get token first
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'

# Then update profile
curl -X PUT http://127.0.0.1:8000/api/profiles/1/ \
  -H "Authorization: Bearer your_access_token" \
  -F "photo=@/path/to/photo.jpg" \
  -F "bio=Your bio text" \
  -F "location=Your location"
```

### Item Listings Management

#### Create New Listing

```http
POST /api/listings/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "title": "Gaming Laptop",
    "description": "High-end gaming laptop in excellent condition",
    "category": "Electronics"
}
```

Example using Postman:

1. Create new listing:
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/listings/`
   - Headers:
     ```
     Authorization: Bearer your_access_token
     Content-Type: application/json
     ```
   - Body (raw JSON):
     ```json
     {
       "title": "Gaming Laptop",
       "description": "High-end gaming laptop in excellent condition",
       "category": "Electronics"
     }
     ```

Example Response:

```json
{
  "id": 1,
  "owner": 1,
  "title": "Gaming Laptop",
  "description": "High-end gaming laptop in excellent condition",
  "category": "Electronics",
  "created_at": "2025-05-31T10:30:00Z"
}
```

#### Get All Listings

```http
GET /api/listings/
Authorization: Bearer your_access_token
```

Example Response:

```json
[
  {
    "id": 1,
    "owner": 1,
    "title": "Gaming Laptop",
    "description": "High-end gaming laptop in excellent condition",
    "category": "Electronics",
    "created_at": "2025-05-31T10:30:00Z"
  },
  {
    "id": 2,
    "owner": 2,
    "title": "Mechanical Keyboard",
    "description": "RGB mechanical keyboard with brown switches",
    "category": "Electronics",
    "created_at": "2025-05-31T11:00:00Z"
  }
]
```

### Swap Requests Management

#### Create Swap Request

```http
POST /api/swap-requests/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "listing": 1,
    "message": "I'm interested in trading my desktop PC for your laptop"
}
```

Example using Postman:

1. Create swap request:
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/swap-requests/`
   - Headers:
     ```
     Authorization: Bearer your_access_token
     Content-Type: application/json
     ```
   - Body (raw JSON):
     ```json
     {
       "listing": 1,
       "message": "I'm interested in trading my desktop PC for your laptop"
     }
     ```

Example Response:

```json
{
  "id": 1,
  "listing": 1,
  "requester": 2,
  "status": "Pending",
  "message": "I'm interested in trading my desktop PC for your laptop",
  "created_at": "2025-05-31T12:00:00Z"
}
```

#### Get All Swap Requests

```http
GET /api/swap-requests/
Authorization: Bearer your_access_token
```

Example Response:

```json
[
  {
    "id": 1,
    "listing": 1,
    "requester": 2,
    "status": "Pending",
    "message": "I'm interested in trading my desktop PC for your laptop",
    "created_at": "2025-05-31T12:00:00Z"
  }
]
```

#### Update Swap Request Status

```http
PUT /api/swap-requests/{id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "status": "Accepted"  // or "Rejected"
}
```

Example Response:

```json
{
  "id": 1,
  "listing": 1,
  "requester": 2,
  "status": "Accepted",
  "message": "I'm interested in trading my desktop PC for your laptop",
  "created_at": "2025-05-31T12:00:00Z"
}
```

Example PowerShell Commands:

```powershell
# Get all listings
$token = "your_access_token"
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

# Create a new listing
$body = @{
    title = "Gaming Laptop"
    description = "High-end gaming laptop in excellent condition"
    category = "Electronics"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/listings/" `
    -Method Post `
    -Headers $headers `
    -Body $body

# Create a swap request
$swapBody = @{
    listing = 1
    message = "I'm interested in trading my desktop PC for your laptop"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/swap-requests/" `
    -Method Post `
    -Headers $headers `
    -Body $swapBody
```

- Open a new request
- POST `http://127.0.0.1:8000/api/auth/token/`
- Select "Body" > "raw" > "JSON"
- Enter credentials:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- Send request and copy the access token from the response

3. **Update Profile:**
   - Open a new request
   - PUT `http://127.0.0.1:8000/api/profiles/{id}/`
   - Add Authorization:
     - Type: Bearer Token
     - Token: (paste your access token)
   - Select "Body" > "form-data"
   - Add fields:
     - Key: `photo` (select "File" type)
     - Value: Select your image file
   - Send request

Expected Response:

```json
{
  "user": {
    "username": "ase1",
    "email": "ase@gmail.com",
    "first_name": "ase",
    "last_name": "ase"
  },
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

##### Using cURL:

```bash
curl -X PUT \
  -H "Authorization: Bearer <access_token>" \
  -F "photo=@/path/to/photo.jpg" \
  -F "bio=Updated bio" \
  -F "location=New location" \
  http://localhost:8000/api/profiles/{id}/
```

### Item Listings

- Create, read, update, and delete item listings
- Image upload for items
- Search and filter listings
- Rate limiting for API endpoints

### Swap Requests

- Create and manage swap requests
- Accept or reject swap proposals
- Track swap request status

## API Endpoints

### Authentication

- `POST /api/auth/register/` - Register a new user
  ```json
  {
    "username": "string",
    "password": "string",
    "password2": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string"
  }
  ```
- `POST /api/auth/token/` - Obtain JWT tokens
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- `POST /api/auth/token/refresh/` - Refresh JWT token
  ```json
  {
    "refresh": "string"
  }
  ```
- `POST /api/auth/token/verify/` - Verify JWT token
  ```json
  {
    "token": "string"
  }
  ```

### User Profiles

- `GET /api/profiles/` - List user profiles (authenticated)
- `GET /api/profiles/{id}/` - Retrieve specific profile
- `PUT /api/profiles/{id}/` - Update profile
- `PATCH /api/profiles/{id}/` - Partially update profile

### Listings

- `GET /api/listings/` - List all items
- `POST /api/listings/` - Create new listing
- `GET /api/listings/{id}/` - Retrieve specific listing
- `PUT /api/listings/{id}/` - Update listing
- `DELETE /api/listings/{id}/` - Delete listing

### Swap Requests

- `GET /api/swap-requests/` - List swap requests
- `POST /api/swap-requests/` - Create swap request
- `GET /api/swap-requests/{id}/` - Retrieve specific request
- `PUT /api/swap-requests/{id}/` - Update request
- `DELETE /api/swap-requests/{id}/` - Delete request

## Authentication Flow

1. **Registration**

   - User submits registration data
   - System validates input and creates user account
   - JWT tokens are generated and returned

2. **Login**

   - User submits credentials
   - System validates and returns JWT tokens
   - Access token is used for subsequent requests

3. **Protected Routes**

   - Include JWT token in Authorization header
   - Format: `Authorization: Bearer <access_token>`

4. **Token Refresh**
   - Use refresh token to obtain new access token
   - Refresh token is valid for 24 hours
   - Access token is valid for 60 minutes

## Security Features

- Password hashing using Django's built-in password hashers
- JWT token-based authentication
- Rate limiting on API endpoints
- Input validation and sanitization
- File upload restrictions (size and type)

## Setup and Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Environment Variables

Create a `.env` file with the following variables:

```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Testing

Run the test suite:

```bash
python manage.py test
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse:

- 10 requests per minute per user
- Rate limit headers included in responses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Using Postman for API Testing

### Setting Up Postman

1. Download and install Postman from https://www.postman.com/downloads/
2. Create a new collection for TechSwap
3. Set up environment variables:
   - Create a new environment
   - Add variables:
     - `base_url`: `http://localhost:8000`
     - `token`: (leave empty, will be filled after login)

### Authentication in Postman

1. **Register a New User:**

   - POST `{{base_url}}/api/auth/register/`
   - Body (JSON):
     ```json
     {
       "username": "testuser",
       "password": "your_password",
       "password2": "your_password",
       "email": "test@example.com",
       "first_name": "Test",
       "last_name": "User"
     }
     ```

2. **Get Access Token:**

   - POST `{{base_url}}/api/auth/token/`
   - Body (JSON):
     ```json
     {
       "username": "testuser",
       "password": "your_password"
     }
     ```
   - Save the access token to environment variable:
     - In "Tests" tab, add:
     ```javascript
     var jsonData = JSON.parse(responseBody);
     pm.environment.set("token", jsonData.access);
     ```

3. **Using the Token:**
   - For all protected endpoints, add Authorization header:
   - Type: Bearer Token
   - Token: `{{token}}`

### Example Requests

1. **List User Profiles:**

   - GET `{{base_url}}/api/profiles/`
   - Authorization: Bearer Token

2. **Create Listing:**

   - POST `{{base_url}}/api/listings/`
   - Authorization: Bearer Token
   - Body (JSON):
     ```json
     {
       "title": "Test Item",
       "description": "Test Description",
       "category": "Electronics"
     }
     ```

3. **Create Swap Request:**
   - POST `{{base_url}}/api/swap-requests/`
   - Authorization: Bearer Token
   - Body (JSON):
     ```json
     {
       "listing": 1,
       "message": "I'm interested in this item"
     }
     ```

### Testing Rate Limits

- Each endpoint is limited to 10 requests per minute
- Watch for 429 Too Many Requests response
- Headers in response show rate limit status
