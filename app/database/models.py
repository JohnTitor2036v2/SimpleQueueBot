from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine

from config import SQLALCHEMY_URL

engine = create_async_engine(SQLALCHEMY_URL, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)



class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    tg_id = mapped_column(BigInteger, primary_key=True)
    nickname: Mapped[str] = mapped_column()

    # Relationships
    # followed_queues = relationship('Queue', back_populates='followers')


class Group(Base):
    __tablename__ = 'groups'

    tg_id = mapped_column(BigInteger, primary_key=True)

    # Relationships
    # queues = relationship('Queue', back_populates='groups')


class Queue(Base):
    __tablename__ = 'queues'

    id: Mapped[int] = mapped_column(primary_key=True)
    queue_name: Mapped[str] = mapped_column()
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.tg_id'))

    # Relationships
    # followed_users = relationship('User', back_populates='followed_queues')
    # groups = relationship('Group', back_populates='queues')


class Follow(Base):
    __tablename__ = 'follows'

    following_user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'), primary_key=True)
    following_queue_id: Mapped[int] = mapped_column(ForeignKey('queues.id'), primary_key=True)
    position: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    # user = relationship('User', back_populates='followed_queues')
    # queue = relationship('Queue', back_populates='followers')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
