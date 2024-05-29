from sqlalchemy import BigInteger, Integer, String, Numeric, ForeignKey, Sequence
from sqlalchemy.schema import CreateSequence, DropSequence
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker

from typing import List

from config import SQLALCHEMY_URL

engine = create_async_engine(SQLALCHEMY_URL, echo=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

queue_id_seq = Sequence(
    'queue_id_seq',
    start=1,
    increment=1,
    minvalue=1,
    maxvalue=10000,
    cycle=True,
    cache=50
)

follow_id_seq = Sequence(
    'follow_id_seq',
    start=1,
    increment=1,
    minvalue=1,
    maxvalue=10000,
    cycle=True,
    cache=50
)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nickname: Mapped[str] = mapped_column(String(255))

    follows = relationship("Follow", back_populates="user")


class Group(Base):
    __tablename__ = 'groups'

    group_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    group_name: Mapped[str] = mapped_column(String(255))
    group_type: Mapped[str] = mapped_column(String(11))

    queues = relationship("Queue", back_populates="group")


class Queue(Base):
    __tablename__ = 'queues'

    queue_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, server_default=queue_id_seq.next_value())
    queue_name: Mapped[str] = mapped_column(String(255))
    group_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('groups.group_id'))
    size: Mapped[int] = mapped_column(Integer)

    group = relationship("Group", back_populates="queues")
    follows = relationship("Follow", back_populates="group")


class Follow(Base):
    __tablename__ = 'follows'

    follow_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, server_default=follow_id_seq.next_value())
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    queue_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('queues.queue_id'))
    user_position: Mapped[int] = mapped_column(Integer)

    user = relationship("User", back_populates="follows")
    group = relationship("Queue", back_populates="follows")


async def async_main():
    async with engine.begin() as conn:
        await conn.execute(CreateSequence(queue_id_seq, if_not_exists=True))
        await conn.execute(CreateSequence(follow_id_seq, if_not_exists=True))
        await conn.run_sync(Base.metadata.create_all)
