import asyncpg
import asyncio

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import SQLALCHEMY_URL

engine = create_async_engine(SQLALCHEMY_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    tg_id = mapped_column(BigInteger, primary_key=True)
    nickname: Mapped[str] = mapped_column()


class Group(Base):
    __tablename__ = 'groups'

    tg_id = mapped_column(BigInteger, primary_key=True)

    # queues = relationship('Queue', back_populates='group')


class Queue(Base):
    __tablename__ = 'queues'

    id: Mapped[int] = mapped_column(primary_key=True)
    queue_name: Mapped[str] = mapped_column()
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))

    # users = relationship('User', back_populates='queues')
    # group = relationship('Group', back_populates='queues')


class Follow(Base):
    __tablename__ = 'follows'

    following_user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))
    following_queue_id: Mapped[int] = mapped_column(ForeignKey('queues.id'))
    position: Mapped[int] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Welcome message
# Create queue function:
# - Random
# - Joinable
# Join queue function:
# - The first empty position
# - The random empty position
# - The specific empty position
# - Const. Fila = 20
# Show queue function:
# - Show all queues
# - Show specific function and all position
# Delete queue function:
# - Delete all queues
# - Delete specific queue
