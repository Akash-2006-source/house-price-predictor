from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
class Prediction(Base):
    __tablename__ = 'predictions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_sqft: Mapped[float] = mapped_column(Float, nullable=False)
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String(160), nullable=False)
    predicted_price_inr: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
