from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from typing import Dict, List
import random

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock data for generating itineraries
activities = [
    {
        "name": "Evening Stroll in Trastevere",
        "location": "Trastevere Neighborhood",
        "description": "Explore the charming cobblestone streets, vibrant nightlife, and local eateries in Trastevere.",
        "suitability": "Perfect for meeting locals and other travelers, aligning with artistic nature",
        "reviews": "4.8/5 stars on TripAdvisor"
    },
    {
        "name": "Visit to Galleria Borghese",
        "location": "Borghese Gardens",
        "description": "Admire stunning Baroque art, including works by Caravaggio and Bernini.",
        "suitability": "Ideal for art enthusiasts and those interested in Italian culture",
        "reviews": "4.7/5 stars on Google Reviews"
    },
    {
        "name": "Colosseum and Roman Forum Tour",
        "location": "Colosseum",
        "description": "Step back in time with a guided tour of ancient Rome's most iconic landmarks.",
        "suitability": "Great for history buffs and photography enthusiasts",
        "reviews": "4.9/5 stars on Viator"
    },
    {
        "name": "Pasta Making Workshop",
        "location": "Local Cooking School",
        "description": "Learn to make authentic Italian pasta from scratch with expert chefs.",
        "suitability": "Perfect for foodies and those who enjoy hands-on experiences",
        "reviews": "5/5 stars on Airbnb Experiences"
    },
    {
        "name": "Sunset at Piazzale Michelangelo",
        "location": "Piazzale Michelangelo",
        "description": "Enjoy breathtaking panoramic views of Florence as the sun sets over the city.",
        "suitability": "Ideal for romantic moments and photography enthusiasts",
        "reviews": "4.8/5 stars on TripAdvisor"
    }
]

def generate_itinerary(days: int) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
    itinerary = {}
    for day in range(1, days + 1):
        day_activities = random.sample(activities, k=min(2, len(activities)))
        itinerary[f"Day {day}"] = {
            "title": f"Day {day}: Adventure and Exploration",
            "activities": day_activities
        }
    return itinerary

@app.route('/plan', methods=['POST'])
def plan_trip():
    try:
        data = request.json
        logger.info(f"Received request: {data}")

        age = data.get('age')
        gender = data.get('gender')
        personality = data.get('personality')
        days = int(data.get('days', 1))
        origin = data.get('origin')
        destination = data.get('destination')

        # Generate itinerary
        itinerary = generate_itinerary(days)

        response = {
            "message": "Itinerary generated successfully",
            "itinerary": itinerary
        }

        logger.info(f"Generated itinerary: {response}")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error generating itinerary: {str(e)}")
        return jsonify({"error": "Failed to generate itinerary"}), 500

if __name__ == '__main__':
    app.run(debug=True)

# Test the API
import requests

test_data = {
    "age": "30",
    "gender": "female",
    "personality": "adventurous, loves nature, enjoys local cuisine",
    "days": "3",
    "origin": "New York",
    "destination": "Rome"
}

response = requests.post('http://localhost:5000/plan', json=test_data)
print(response.json())
