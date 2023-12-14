from sqlalchemy import Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ..extensions import db
import enum

class EnumTypes(enum.Enum):
    Other = 1
    Pets = 2
    Gym = 3
    Food = 4

class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    text: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String, nullable=True, default="generic_post_pic.jpg")
    created: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now())
    type: Mapped[EnumTypes] = mapped_column(db.Enum(EnumTypes), default=EnumTypes.Other.name)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)  # ForeignKey added
    user = relationship('User', backref='posts')  # Relationship to User added

    def __repr__(self) -> str:
        return f"ID:{self.id} Title:{self.title} Created:{self.created} UserID: {self.user_id}"
