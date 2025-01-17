import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from database.models.base import Base  # Import the Base class
# Create a base class for the model


class User(Base):
    __tablename__ = 'users'

    # Use UUID as primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(100), nullable=False, unique=True)  # Unique email field
    password = Column(String(255), nullable=False)

    @validates('email')
    def validate_email(self, key, value):
        return value.lower()



User.__table__.append_constraint(UniqueConstraint('email'))
