from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from functools import wraps

# Initialize Flask application
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.String(20), nullable=False)
    reviews = db.relationship('Review', backref='book', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Basic Authentication
def basic_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({'message': 'Authentication required'}), 401

        user = User.query.filter_by(username=auth.username).first()
        if not user or not bcrypt.check_password_hash(user.password, auth.password):
            return jsonify({'message': 'Invalid credentials'}), 401

        return f(user, *args, **kwargs)

    return decorated

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/books', methods=['POST'])
@basic_auth_required
def add_book(user):
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    published_date = data.get('published_date')

    if not title or not author or not published_date:
        return jsonify({'message': 'All fields are required'}), 400

    new_book = Book(title=title, author=author, published_date=published_date)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = []
    for book in books:
        result.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published_date': book.published_date
        })
    return jsonify(result), 200

@app.route('/books/<int:book_id>/reviews', methods=['POST'])
@basic_auth_required
def add_review(user, book_id):
    data = request.get_json()
    content = data.get('content')
    rating = data.get('rating')

    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    if not content or not rating or not (1 <= rating <= 5):
        return jsonify({'message': 'Content and a rating between 1-5 are required'}), 400

    new_review = Review(content=content, rating=rating, user_id=user.id, book_id=book_id)
    db.session.add(new_review)
    db.session.commit()

    return jsonify({'message': 'Review added successfully'}), 201

@app.route('/books/<int:book_id>/reviews', methods=['GET'])
def get_reviews(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    reviews = Review.query.filter_by(book_id=book_id).all()
    result = []
    for review in reviews:
        result.append({
            'id': review.id,
            'content': review.content,
            'rating': review.rating,
            'user_id': review.user_id,
            'created_at': review.created_at
        })
    return jsonify(result), 200

@app.route('/books/top-rated', methods=['GET'])
def get_top_rated_books():
    top_books = db.session.query(Book, db.func.avg(Review.rating).label('avg_rating'))\
        .join(Review)\
        .group_by(Book.id)\
        .order_by(db.desc('avg_rating'))\
        .limit(5).all()

    result = []
    for book, avg_rating in top_books:
        result.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published_date': book.published_date,
            'average_rating': round(avg_rating, 2)
        })
    return jsonify(result), 200

@app.route('/books/search', methods=['GET'])
def search_books():
    query = request.args.get('q')
    if not query:
        return jsonify({'message': 'Search query is required'}), 400

    books = Book.query.filter(
        (Book.title.ilike(f'%{query}%')) | (Book.author.ilike(f'%{query}%'))
    ).all()

    result = []
    for book in books:
        result.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published_date': book.published_date
        })
    return jsonify(result), 200

# Database Initialization
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize database tables
    app.run(debug=True)