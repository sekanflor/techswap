# TechSwap - Item Trading Platform

TechSwap is a Django REST Framework-based platform that allows users to trade items with each other. The platform includes features for user authentication, item listings, and swap requests.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Rate Limiting Test](#rate-limiting-test)

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

### Item Management
- Create, read, update, and delete item listings
- Category-based organization
- Search and filter functionality
- Image upload support for items

### Swap System
- Create and manage swap requests
- Real-time notifications
- Chat functionality between users
- Swap status tracking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/techswap.git
cd techswap
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
techswap/
├── api/                    # API endpoints
├── core/                   # Core functionality
├── users/                  # User management
├── items/                  # Item management
├── swaps/                  # Swap functionality
├── media/                  # User-uploaded files
├── static/                 # Static files
├── templates/             # HTML templates
└── manage.py              # Django management script
```

## API Documentation

### Authentication Endpoints

#### Register User
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

#### Login
```http
POST /api/auth/token/
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

### Profile Endpoints

#### Update Profile
```http
PUT /api/profiles/{id}/
Authorization: Bearer your_access_token
Content-Type: multipart/form-data

Fields:
- photo: file
- bio: string (optional)
- location: string (optional)
```

### Item Endpoints

#### Create Listing
```http
POST /api/listings/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "title": "string",
    "description": "string",
    "category": "string"
}
```

#### Get Listings
```http
GET /api/listings/
Authorization: Bearer your_access_token
```

### Swap Endpoints

#### Create Swap Request
```http
POST /api/swap-requests/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "listing": integer,
    "message": "string"
}
```

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
This project follows PEP 8 guidelines. To check your code:
```bash
flake8
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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

## Rate Limiting Test

TechSwap API implements rate limiting (e.g., 10 requests per minute per user) to prevent abuse.

### How to Test Rate Limiting in Postman

#### Manual Test
1. Pick any protected endpoint (e.g., `GET http://localhost:8000/api/profiles/`).
2. Send the request repeatedly (at least 11 times within 1 minute).
3. Observe the responses:
   - The first 10 requests should succeed (status 200).
   - The 11th and subsequent requests within the same minute should return:
     - **Status:** 429 Too Many Requests
     - **Body:**
       ```json
       {
         "detail": "Request was throttled. Expected available in X seconds."
       }
       ```

#### Automated Test (Postman Runner)
1. Add a request (e.g., GET `/api/profiles/`) to a collection.
2. Click the "Runner" button in Postman.
3. Set the number of iterations to 15 (or more than your rate limit).
4. Run the collection.
5. Check the results: the first 10 should be 200 OK, the rest should be 429 Too Many Requests.

#### Notes
- Rate limiting applies per user/token.
- Wait for the window to reset (usually 60 seconds) before you can send more requests.
