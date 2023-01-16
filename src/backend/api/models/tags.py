from sqlalchemy import Column, Integer, String

from api.db.database import Base
from api.models.mixins import Timestamp


class Tag(Timestamp, Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
