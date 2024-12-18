# Books API

A RESTful API built using Flask for managing users, books, and reviews. The API includes functionality for user registration, book addition, review creation, and retrieval of books and reviews. It also supports search and top-rated book listings.

---

## Features

- **User Authentication:** Basic authentication with password hashing.
- **Books Management:** Add, retrieve, and search books.
- **Reviews Management:** Add and retrieve reviews for books.
- **Top-rated Books:** Retrieve a list of the top 5 books based on average ratings.

---

## Installation

### Prerequisites
- Python 3.8+
- `pip` package manager

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/books-api.git
   cd books-api
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   python app.py
   ```
   The database (`books.db`) will be created in the project root.
5. Run the application:
   ```bash
   python app.py
   ```
   The API will be available at `http://127.0.0.1:5000`.

---

## Endpoints

### Authentication

#### `POST /register`
- **Description:** Register a new user.
- **Request Body:**
  ```json
  {
      "username": "string",
      "password": "string"
  }
  ```
- **Response:**
  ```json
  {
      "message": "User registered successfully"
  }
  ```

---

### Books

#### `POST /books`
- **Description:** Add a new book (requires authentication).
- **Headers:** Basic Authentication (`username`, `password`)
- **Request Body:**
  ```json
  {
      "title": "string",
      "author": "string",
      "published_date": "string"
  }
  ```
- **Response:**
  ```json
  {
      "message": "Book added successfully"
  }
  ```

#### `GET /books`
- **Description:** Retrieve all books.
- **Response:**
  ```json
  [
      {
          "id": 1,
          "title": "string",
          "author": "string",
          "published_date": "string"
      }
  ]
  ```

#### `GET /books/search?q=<query>`
- **Description:** Search books by title or author.
- **Response:**
  ```json
  [
      {
          "id": 1,
          "title": "string",
          "author": "string",
          "published_date": "string"
      }
  ]
  ```

#### `GET /books/top-rated`
- **Description:** Retrieve the top 5 books based on average ratings.
- **Response:**
  ```json
  [
      {
          "id": 1,
          "title": "string",
          "author": "string",
          "published_date": "string",
          "average_rating": 4.5
      }
  ]
  ```

---

### Reviews

#### `POST /books/<int:book_id>/reviews`
- **Description:** Add a review for a specific book (requires authentication).
- **Headers:** Basic Authentication (`username`, `password`)
- **Request Body:**
  ```json
  {
      "content": "string",
      "rating": 5
  }
  ```
- **Response:**
  ```json
  {
      "message": "Review added successfully"
  }
  ```

#### `GET /books/<int:book_id>/reviews`
- **Description:** Retrieve reviews for a specific book.
- **Response:**
  ```json
  [
      {
          "id": 1,
          "content": "string",
          "rating": 5,
          "user_id": 1,
          "created_at": "datetime"
      }
  ]
  ```

---

## Database Models

### User
- `id`: Integer, primary key
- `username`: String, unique, required
- `password`: String (hashed), required

### Book
- `id`: Integer, primary key
- `title`: String, required
- `author`: String, required
- `published_date`: String, required

### Review
- `id`: Integer, primary key
- `content`: Text, required
- `rating`: Integer (1-5), required
- `user_id`: Integer, foreign key to `User`
- `book_id`: Integer, foreign key to `Book`
- `created_at`: Datetime, default is current time

---

## Authentication
- Uses HTTP Basic Authentication.
- Passwords are hashed using `bcrypt`.

---

## Development

### Running in Development Mode
Enable debug mode to auto-reload on code changes:
```bash
python app.py
```

### Testing
You can use tools like [Postman](https://www.postman.com/) or `curl` to test the API.

### Example Curl Commands
- **Register a User:**
  ```bash
  curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password"}'
  ```
- **Add a Book:**
  ```bash
  curl -X POST http://127.0.0.1:5000/books \
  -H "Authorization: Basic dGVzdHVzZXI6cGFzc3dvcmQ=" \
  -H "Content-Type: application/json" \
  -d '{"title": "Book Title", "author": "Author Name", "published_date": "2024"}'
  ```

---


## Contributing

Feel free to fork the repository and submit pull requests. All contributions are welcome!

