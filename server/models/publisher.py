from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Publisher(BaseModel):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one publisher has many games
    games = relationship("Game", back_populates="publisher")

    @validates('name')
    def validate_name(self, key, name):
        """
        Validates that the publisher name meets minimum length requirements.
        
        Args:
            key: The attribute key being validated (provided by SQLAlchemy)
            name: The publisher name string to validate
        
        Returns:
            str: The validated publisher name
        
        Raises:
            ValueError: If the name is too short or invalid
        """
        return self.validate_string_length('Publisher name', name, min_length=2)

    @validates('description')
    def validate_description(self, key, description):
        """
        Validates that the publisher description meets minimum length requirements.
        
        Args:
            key: The attribute key being validated (provided by SQLAlchemy)
            description: The publisher description string to validate
        
        Returns:
            str: The validated publisher description, or None if description is None
        
        Raises:
            ValueError: If the description is too short or invalid
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)

    def __repr__(self):
        return f'<Publisher {self.name}>'

    def to_dict(self):
        """
        Converts the Publisher model instance to a dictionary representation.
        
        Returns:
            dict: Dictionary containing publisher id, name, description, and game count
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_count': len(self.games) if self.games else 0
        }