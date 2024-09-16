# main.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Band, Venue, Concert

# Create an engine and a session
engine = create_engine('sqlite:///concerts.db')
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data (optional)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Create instances of Band
band1 = Band(name='The Beatles', hometown='Liverpool')
band2 = Band(name='The Rolling Stones', hometown='London')

# Create instances of Venue
venue1 = Venue(title='Madison Square Garden', city='New York')
venue2 = Venue(title='The Cavern Club', city='Liverpool')

# Add bands and venues to the session
session.add_all([band1, band2, venue1, venue2])
session.commit()

# Bands play in venues
concert1 = band1.play_in_venue(venue1, '2023-01-01')
concert2 = band1.play_in_venue(venue2, '2023-02-01')
concert3 = band2.play_in_venue(venue1, '2023-03-01')

# Add concerts to the session
session.add_all([concert1, concert2, concert3])
session.commit()

# Testing methods
print("Band1 Venues:", [venue.title for venue in band1.venues()])
print("Venue1 Bands:", [band.name for band in venue1.bands()])
print("Concert1 Hometown Show:", concert1.hometown_show())
print("Concert2 Hometown Show:", concert2.hometown_show())
print("Concert1 Introduction:", concert1.introduction())
print("Band1 All Introductions:", band1.all_introductions())
print("Band with Most Performances:", Band.most_performances(session).name)
print("Venue1 Most Frequent Band:", venue1.most_frequent_band().name)
print("Venue1 Concert on 2023-01-01:", venue1.concert_on('2023-01-01'))

# Close the session
session.close()
