from datetime import datetime

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, mapped_column

Base = declarative_base()


class OrganizationModel(Base):
    __abstract__ = True

    organization = mapped_column(String(200))
    username = mapped_column(String(200))

    created_at = mapped_column(DateTime(timezone=True), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    last_updated_at = mapped_column(DateTime(timezone=True), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    is_active = mapped_column(Boolean, default=True)
    is_deleted = mapped_column(Boolean, default=False)


class BasicModel(Base):
    __abstract__ = True

    created_at = mapped_column(DateTime(timezone=True), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    last_updated_at = mapped_column(DateTime(timezone=True), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    is_active = mapped_column(Boolean, default=True)
    is_deleted = mapped_column(Boolean, default=False)
