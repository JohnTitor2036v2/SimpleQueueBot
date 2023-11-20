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

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nickname: Mapped[str] = mapped_column()


class Group(Base):
    __tablename__ = 'groups'

    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    chat_name: Mapped[str] = mapped_column()


class Queue(Base):
    __tablename__ = 'queues'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    queue_name: Mapped[str] = mapped_column()
    chat_id: Mapped[int] = mapped_column(ForeignKey('groups.chat_id'))
    size: Mapped[int] = mapped_column()


class Follow(Base):
    __tablename__ = 'follows'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    following_user_id: Mapped[int] = mapped_column(BigInteger)
    following_queue_id: Mapped[int] = mapped_column(BigInteger)
    position: Mapped[int] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
