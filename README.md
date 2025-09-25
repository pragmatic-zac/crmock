# CRMock API

A lightweight mock CRM API built with FastAPI for testing purposes.

## Features

- User registration and authentication (Basic Auth)
- Full CRUD operations for customer management
- SQLite database for persistence
- Ready for deployment on Fly.io

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd crmock
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /api/register` - Create a new user account
- `GET /api/me` - Get current user information (requires authentication)

### Customers

All customer endpoints require Basic Authentication.

- `POST /api/customers` - Create a new customer
- `GET /api/customers` - List all customers for the authenticated user
- `GET /api/customers/{id}` - Get a specific customer
- `PUT /api/customers/{id}` - Update a customer
- `DELETE /api/customers/{id}` - Delete a customer

### Credit Check

Simulate long-running processing with callbacks.

- `POST /api/credit-check` - Initiate a mock credit check (requires authentication)

## Usage Example

### Register a new user

```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### Create a customer (requires authentication)

```bash
curl -X POST http://localhost:8000/api/customers \
  -u testuser:testpass123 \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "123-456-7890",
    "company": "Acme Corp"
  }'
```

### List all customers

```bash
curl -X GET http://localhost:8000/api/customers \
  -u testuser:testpass123
```

### Initiate a credit check (with callback)

```bash
curl -X POST http://localhost:8000/api/credit-check/ \
  -u testuser:testpass123 \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer-uuid-here",
    "callback_url": "https://your-server.com/webhook/credit-result",
    "wait_seconds": 10
  }'
```

## Deployment on Fly.io

### Prerequisites

- [Fly CLI](https://fly.io/docs/hands-on/install-flyctl/) installed
- Fly.io account

### Deploy

1. Launch the app (first time only):
```bash
fly launch
```

2. Create a volume for persistent storage:
```bash
fly volumes create crmock_data --size 1 --region iad
```

3. Deploy:
```bash
fly deploy
```

Your API will be available at `https://crmock.fly.dev`

## Environment Variables

- `DATABASE_URL` - SQLite database URL (default: `sqlite:///./crmock.db`)

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **Authentication**: HTTP Basic Auth
- **Password Hashing**: bcrypt
- **Deployment**: Docker + Fly.io

## License

MIT