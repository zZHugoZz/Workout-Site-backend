from sqlalchemy import ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base
from .recipes_model import Recipe


class FavoriteFood(Base):
    __tablename__ = "favorite_foods"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    calories_per_100g: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    proteins_per_100g: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    carbs_per_100g: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    fats_per_100g: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    # maybe benefits
    recipes: Mapped[list[Recipe]] = relationship(
        "Receipe", lazy="selectin", cascade="all, delete"
    )
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self) -> None:
        f"FavoriteFood(name={self.name}, calories_per_100g={self.calories_per_100g}, ...)"
