# FastAPI with Supabase Integration

This is a FastAPI application that demonstrates integration with Supabase as a backend database.

## Features

- RESTful API endpoints for managing news items
- Supabase database integration
- Comprehensive error handling
- JSON response formatting
- Thread-safe database connection management

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd FastApi
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application is configured to connect to a Supabase database with the following credentials:
- URL: `https://eeuwpcynygzohstndlxf.supabase.co`
- API Key: `sb_secret_C-HpaYbH0gGYtivfb6j_1A_hkdWVKVy`

## Running the Application

Start the server using uvicorn:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### GET `/items/{item_id}`
Retrieve an item by its ID.

Parameters:
- `item_id` (integer): The ID of the item to retrieve
- `q` (string, optional): Additional query parameter

### GET `/test-json`
Returns a sample JSON response for testing purposes.

### GET `/news`
Retrieves all news items from the database. Also inserts a test item before retrieving.

### GET `/news/{news_id}`
Retrieves a specific news item by its ID.

Parameters:
- `news_id` (integer): The ID of the news item to retrieve

## Error Handling

The application includes comprehensive error handling for:
- 404 Not Found errors
- Request validation errors
- Internal server errors

All errors are returned in a consistent JSON format.

## Database Operations

The application supports all CRUD operations through the Supabase client:
- Create (insert_data)
- Read (query_data, query_data_id)
- Update (update_data_id)
- Delete (delete_data_id)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
