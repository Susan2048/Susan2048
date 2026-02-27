from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Game(BaseModel):
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    star_rating = db.Column(db.Float, nullable=True)
    
    # Foreign keys for one-to-many relationships
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'), nullable=False)
    
    # One-to-many relationships (many games belong to one category/publisher)
    category = relationship("Category", back_populates="games")
    publisher = relationship("Publisher", back_populates="games")
    
    @validates('title')
    def validate_name(self, key, name):
        """
        Validates that the game title meets minimum length requirements.
        
        Args:
            key: The attribute key being validated (provided by SQLAlchemy)
            name: The game title string to validate
        
        Returns:
            str: The validated game title
        
        Raises:
            ValueError: If the title is too short or invalid
        """
        return self.validate_string_length('Game title', name, min_length=2)
    
    @validates('description')
    def validate_description(self, key, description):
        """
        Validates that the game description meets minimum length requirements.
        
        Args:
            key: The attribute key being validated (provided by SQLAlchemy)
            description: The game description string to validate
        
        Returns:
            str: The validated game description, or None if description is None
        
        Raises:
            ValueError: If the description is too short or invalid
        """
        if description is not None:
            return self.validate_string_length('Description', description, min_length=10, allow_none=True)
        return description
    
    def __repr__(self):
        return f'<Game {self.title}, ID: {self.id}>'

    def to_dict(self):
        """
        Converts the Game model instance to a dictionary representation.
        
        Returns:
            dict: Dictionary containing game id, title, description, publisher info, 
                  category info, and star rating with camelCase keys for frontend
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'publisher': {'id': self.publisher.id, 'name': self.publisher.name} if self.publisher else None,
            'category': {'id': self.category.id, 'name': self.category.name} if self.category else None,
            'starRating': self.star_rating  # Changed from star_rating to starRating
        }