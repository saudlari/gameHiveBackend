from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'gamehive.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    games = db.relationship('Game', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)


class Game(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    contact_email = db.Column(db.String(100), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    is_new = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, description, price, category, image=None, 
                 contact_email=None, contact_phone=None, is_new=True, user_id=None):
        self.title = title
        self.description = description
        self.price = price
        self.category = category
        self.image = image
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.is_new = is_new
        self.user_id = user_id


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'created_at', 'updated_at')


class GameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'price', 'image', 'category', 
                  'contact_email', 'contact_phone', 'is_new', 'created_at', 
                  'updated_at', 'user_id')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
game_schema = GameSchema()
games_schema = GameSchema(many=True)



@app.route('/users', methods=["POST"])
def register_user():
    user_data = request.get_json()
    username = user_data.get('username')
    email = user_data.get('email')
    password = user_data.get('password')
    
    # Check if user already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({"error": "Username or email already exists"}), 400
    
    new_user = User(username, email, password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user))


@app.route('/login', methods=["POST"])
def login():
    login_data = request.get_json()
    email = login_data.get('email')
    password = login_data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return jsonify(user_schema.dump(user))
    
    return jsonify({"error": "Invalid credentials"}), 401



@app.route('/games', methods=['POST'])
def add_game():
    data = request.json
    
    # Verificar que todos los campos requeridos estén presentes
    required_fields = ['title', 'description', 'price', 'category', 'image', 'contact_email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    

    new_game = Game(
        title=data['title'],
        description=data['description'],
        price=float(data['price']),
        category=data['category'],
        image=data['image'],
        contact_email=data['contact_email'],
        contact_phone=data.get('contact_phone', ''),
        is_new=data.get('is_new', True),
        user_id=data.get('user_id', '1')
    )
    

    db.session.add(new_game)
    db.session.commit()
    

    return game_schema.jsonify(new_game), 201


@app.route("/games", methods=["GET"])
def get_games():
    all_games = Game.query.all()
    return jsonify(games_schema.dump(all_games))


@app.route("/games/<id>", methods=["GET"])
def get_game(id):
    game = Game.query.get(id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    return jsonify(game_schema.dump(game))


@app.route("/games/<id>", methods=["PUT"])
def update_game(id):
    game = Game.query.get(id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        game.title = data['title']
    if 'description' in data:
        game.description = data['description']
    if 'price' in data:
        game.price = data['price']
    if 'image' in data:
        game.image = data['image']
    if 'category' in data:
        game.category = data['category']
    if 'contactEmail' in data:
        game.contact_email = data['contactEmail']
    if 'contactPhone' in data:
        game.contact_phone = data['contactPhone']
    if 'isNew' in data:
        game.is_new = data['isNew']
    
    game.updated_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify(game_schema.dump(game))


@app.route("/games/<id>", methods=["DELETE"])
def delete_game(id):
    game = Game.query.get(id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    db.session.delete(game)
    db.session.commit()

    return jsonify({"message": "Game deleted successfully"})


@app.route("/users/<user_id>/games", methods=["GET"])
def get_user_games(user_id):
    user_games = Game.query.filter_by(user_id=user_id).all()
    return jsonify(games_schema.dump(user_games))



@app.route("/healthchecker", methods=["GET"])
def healthchecker():
    return {"status": "success", "message": "GameHive API is running"}



def create_tables():
    with app.app_context():  # Set up the application context
        db.create_all()
        # Create admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User('admin', 'admin@gamehive.com', 'admin123')
            db.session.add(admin)
            db.session.commit()


if __name__ == "__main__":
    create_tables()  # Call the function directly
    app.run(host='0.0.0.0', debug=True, port=8000)
