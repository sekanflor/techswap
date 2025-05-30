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
