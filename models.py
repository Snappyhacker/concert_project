# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Band(Base):
    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hometown = Column(String)

    concerts = relationship('Concert', back_populates='band', cascade='all, delete-orphan')

    def venues(self):
        return list({concert.venue for concert in self.concerts})

    def play_in_venue(self, venue, date):
        new_concert = Concert(band=self, venue=venue, date=date)
        return new_concert

    def all_introductions(self):
        return [concert.introduction() for concert in self.concerts]

    @classmethod
    def most_performances(cls, session):
        band_performance_counts = (
            session.query(cls, func.count(Concert.id).label('performance_count'))
            .join(Concert)
            .group_by(cls.id)
            .order_by(func.count(Concert.id).desc())
        )
        result = band_performance_counts.first()
        return result[0] if result else None

class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    city = Column(String)

    concerts = relationship('Concert', back_populates='venue', cascade='all, delete-orphan')

    def bands(self):
        return list({concert.band for concert in self.concerts})

    def concert_on(self, date):
        for concert in self.concerts:
            if concert.date == date:
                return concert
        return None

    def most_frequent_band(self):
        band_counts = {}
        for concert in self.concerts:
            band = concert.band
            band_counts[band] = band_counts.get(band, 0) + 1
        return max(band_counts, key=band_counts.get) if band_counts else None

class Concert(Base):
    __tablename__ = 'concerts'

    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey('bands.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    date = Column(String)  # Store date as string as per instructions

    band = relationship('Band', back_populates='concerts')
    venue = relationship('Venue', back_populates='concerts')

    def hometown_show(self):
        return self.band.hometown == self.venue.city

    def introduction(self):
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"
