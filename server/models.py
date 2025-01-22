from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_author_name(self, key, address):
        if not address:
            raise ValueError("Name cannot be empty string")
        elif address in [Author.name for Author in Author.query.all()]:
            raise ValueError("Name must be unique")
        return address
    
    @validates('phone_number')
    def validate_phone_number(self, key, address):
        if not len(address) == 10 or not int(address):
            raise ValueError("Number must be exactly 10 digits long")
        return address


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, address):
        if len(address) < 250:
            raise ValueError("Content must be at least 250 characters long")
        return address
    
    @validates('summary')
    def validate_summary(self, key, address):
        if len(address) > 250:
            raise ValueError("Summary must be less than 250 characters")
        return address
    
    @validates('category')
    def validate_category(self, key, address):
        if address not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Invalid Category")
        
    @validates('title')
    def validate_title(self, key, address):
        if not address or [el in address for el in ["Won't Believe", "Secret", "Top", "Guess"]].count(True) == 0:
            raise ValueError("Not click-baity enough!")

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
