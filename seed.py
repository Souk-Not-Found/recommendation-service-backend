from app import create_app
from app.extensions import db
from app.models.event import Event
from faker import Faker
import random

app = create_app()
app.app_context().push()
fake = Faker()

# Clear existing data
db.session.query(Event).delete()
db.session.commit()

categories = [
    "Tech", "Music", "Art", "Sports", "Food",
    "Business", "Education", "Health", "Science", "Travel"
]

locations = [
    "Tunis", "Sfax", "Sousse", "Paris", "London",
    "Berlin", "New York", "Dubai", "Barcelona", "Rome"
]

events = []

# Generate 25 diverse events
for _ in range(25):
    category = random.choice(categories)
    location = random.choice(locations)
    
    event = Event(
        title=fake.sentence(nb_words=3),
        description=fake.paragraph(nb_sentences=3),
        category=category,
        location=location,
        popularity_score=round(random.uniform(1.0, 5.0), 1)
    )
    
    # Make some events more related for testing similarity
    if random.random() < 0.3:  # 30% chance to create related events
        base_title = "Tech Conference" if category == "Tech" else "Music Festival"
        event.title = f"{base_title} {fake.word()}"
        event.description = f"Join us for {base_title.lower()} focusing on {fake.word()}"

    events.append(event)

# Add some specific events for testing
specific_events = [
    Event(
        title="AI Summit Tunis",
        description="Annual conference on artificial intelligence and machine learning",
        category="Tech",
        location="Tunis",
        popularity_score=4.8
    ),
    Event(
        title="AI Workshop",
        description="Hands-on workshop about practical AI applications",
        category="Tech",
        location="Tunis",
        popularity_score=4.2
    ),
    Event(
        title="Jazz Night Paris",
        description="Evening of live jazz performances with international artists",
        category="Music",
        location="Paris",
        popularity_score=4.9
    ),
    Event(
        title="Classical Concert Paris",
        description="Symphony orchestra performing classical masterpieces",
        category="Music",
        location="Paris",
        popularity_score=4.7
    )
]

events.extend(specific_events)

# Insert all events
for event in events:
    db.session.add(event)

db.session.commit()
print(f"Successfully inserted {len(events)} events.")