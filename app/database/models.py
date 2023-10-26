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

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column()


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column()

    queues = relationship('Queue', back_populates='group')


class Queue(Base):
    __tablename__ = 'queues'

    id: Mapped[int] = mapped_column(primary_key=True)
    queue_name: Mapped[str] = mapped_column()
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    position: Mapped[int] = mapped_column()

    users = relationship('User', back_populates='queues')
    group = relationship('Group', back_populates='queues')


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
