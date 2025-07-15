from app.extensions import db
from app.models.event import Event
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

class RecommendationService:
    def __init__(self):
        # Existing initialization
        self.tfidf_matrix = None
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.events = []
        self.initialized = False
        
        # For NLP-based recommendations
        self.nlp_model = None
        self.description_embeddings = None
        self.nlp_initialized = False
    def initialize_tfidf(self, events):
        """Initialize or update the TF-IDF matrix"""
        if not events:
            return
            
        self.events = events
        # Combine text features for TF-IDF
        texts = [
            f"{event.title} {event.description} {event.category} {event.location}"
            for event in events
        ]
        
        # Create TF-IDF matrix
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        self.initialized = True

    def initialize_nlp_model(self, events):
        """Initialize NLP model and embeddings for description-based recommendations"""
        if not events:
            return
            
        self.events = events
        descriptions = [event.description for event in events if event.description]
        
        try:
            # Initialize Sentence Transformer model
            self.nlp_model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model
            self.description_embeddings = self.nlp_model.encode(descriptions)
            self.nlp_initialized = True
        except Exception as e:
            print(f"Error initializing NLP model: {e}")
            self.nlp_initialized = False

    def get_similar_by_description(self, event_id, top_n=5):
        """
        Get similar events based on description using NLP embeddings
        """
        events = self.get_all()
        if not events:
            return []

        # Initialize NLP model if not done
        if not self.nlp_initialized:
            self.initialize_nlp_model(events)
            
        if not self.nlp_initialized:
            return []

        try:
            # Find the index of our target event
            idx = next(i for i, e in enumerate(events) if e.id == event_id)
            
            # Calculate cosine similarities
            cos_sim = cosine_similarity(
                [self.description_embeddings[idx]],
                self.description_embeddings
            )[0]
            
            # Get top N most similar events (excluding itself)
            sim_scores = list(enumerate(cos_sim))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
            
            return [events[i] for i, _ in sim_scores]
        except StopIteration:
            print(f"Event with id {event_id} not found")
            return []
        except IndexError:
            print("Index error in similarity calculation")
            return []
        except Exception as e:
            print(f"Error in get_similar_by_description: {e}")
            return []

    def get_all(self):
        return Event.query.all()

    def get_by_id(self, event_id):
        return Event.query.get(event_id)

    def create(self, data):
        event = Event(**data)
        db.session.add(event)
        db.session.commit()
        return event

    def update(self, event_id, data):
        event = self.get_by_id(event_id)
        if event:
            for key, value in data.items():
                setattr(event, key, value)
            db.session.commit()
        return event

    def delete(self, event_id):
        event = self.get_by_id(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
        return event

    
    def filter_by_category(self, category):
        return Event.query.filter(Event.category.ilike(f"%{category}%")).all()

    def filter_by_location(self, location):
        return Event.query.filter(Event.location.ilike(f"%{location}%")).all()

    def search_by_title(self, keyword):
        return Event.query.filter(Event.title.ilike(f"%{keyword}%")).all()
    
    
    def get_ai_recommendations(self, event_id=None, category=None, location=None):
        events = self.get_all()
        
        # Initialize TF-IDF if not done or if events have changed
        if not self.initialized or len(events) != len(self.events):
            self.initialize_tfidf(events)
            
        if not events or self.tfidf_matrix is None:
            return []

        if event_id:
            # Content-based recommendations for specific event
            try:
                idx = next(i for i, e in enumerate(events) if e.id == event_id)
                cosine_sim = cosine_similarity(self.tfidf_matrix)
                sim_scores = list(enumerate(cosine_sim[idx]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
                return [events[i] for i, _ in sim_scores]
            except StopIteration:
                return []
        else:
            # Hybrid recommendations based on category/location
            cosine_sim = cosine_similarity(self.tfidf_matrix)
            mean_similarities = np.mean(cosine_sim, axis=1)
            
            ranked_events = []
            for i, event in enumerate(events):
                if ((not category or category.lower() in event.category.lower()) and
                    (not location or location.lower() in event.location.lower())):
                    popularity_score = event.popularity_score or 0
                    content_score = mean_similarities[i]
                    hybrid_score = 0.6 * content_score + 0.4 * (popularity_score / 10)
                    ranked_events.append((event, hybrid_score))
            
            ranked_events.sort(key=lambda x: x[1], reverse=True)
            return [event for event, _ in ranked_events[:10]]
    def recommend(self, category, location):
        events = self.get_all()
        if not events:
            return []

        descriptions = [f"{e.description} {e.category} {e.location}" for e in events]
        tfidf = TfidfVectorizer().fit_transform(descriptions)
        sim = cosine_similarity(tfidf, tfidf)

        # Classement par popularité (exemple simple)
        ranked = sorted(events, key=lambda e: e.popularity_score or 0, reverse=True)
        # Filtrer selon catégorie et location (insensible à la casse)
        filtered = [e for e in ranked if category.lower() in e.category.lower() and location.lower() in e.location.lower()]
        return filtered[:5]


 