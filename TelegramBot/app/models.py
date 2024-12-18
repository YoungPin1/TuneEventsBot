from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    user_telegram_id = Column(Integer, nullable=False)
    city = Column(String, nullable=False)

    artists = relationship("ArtistsUsers", back_populates="user")
    concerts = relationship("UserConcerts", back_populates="user")


class Artist(Base):
    __tablename__ = 'artists'
    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String, nullable=False)

    artists_users = relationship("ArtistsUsers", back_populates="artist")
    concerts = relationship("Concert", back_populates="artist")


class ArtistsUsers(Base):
    __tablename__ = 'artists_users'
    artists_users_id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)

    user = relationship("User", back_populates="artists")
    artist = relationship("Artist", back_populates="artists_users")


class Concert(Base):
    __tablename__ = 'concerts'
    concert_id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'), nullable=False)
    concert_date = Column(Date, nullable=False)
    concert_city = Column(String, nullable=False)

    artist = relationship("Artist", back_populates="concerts")
    user_concerts = relationship("UserConcerts", back_populates="concert")


class UserConcerts(Base):
    __tablename__ = 'user_concerts'
    user_concerts_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    concert_id = Column(Integer, ForeignKey('concerts.concert_id'), nullable=False)

    user = relationship("User", back_populates="concerts")
    concert = relationship("Concert", back_populates="user_concerts")
