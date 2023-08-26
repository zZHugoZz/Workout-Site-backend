from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
from .base_model import Base


class Recipe(Base):
    __tablename__ = "recipes"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    favorite_food_id = mapped_column(
        ForeignKey("favorite_foods.id", ondelete="CASCADE")
    )
    ingredients: Mapped[set[str]] = mapped_column(
        ARRAY(String, dimensions=1), nullable=False
    )
    total_calories: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    total_proteins: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    total_carbs: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    total_fats: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"Recipe(name={self.name}, ...)"
