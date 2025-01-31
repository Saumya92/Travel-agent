from flask import Flask, request, jsonify
from flask_cors import CORS
from my_crew import SurpriseTravelCrew
import re
import logging
import traceback
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)


def safe_crew_execution(inputs):
    """Safely execute the crew operations with detailed logging"""
    try:
        print("\n=== Creating SurpriseTravelCrew ===")
        planner_crew = SurpriseTravelCrew()
        print("SurpriseTravelCrew created successfully")

        print("\n=== Getting Crew Instance ===")
        crew_instance = planner_crew.crew()
        print(f"Crew instance type: {type(crew_instance)}")

        print("\n=== Executing Kickoff ===")
        print(f"Input parameters: {inputs}")
        response = crew_instance.kickoff(inputs=inputs)
        print(f"Kickoff response type: {type(response)}")
        print(f"Kickoff raw response: {response}")

        return response
    except Exception as e:
        print(f"Error in crew execution: {str(e)}")
        print(traceback.format_exc())
        raise


def parse_itinerary(text):
    """Parse the text output into a structured format"""
    print("\n=== Starting Parse Itinerary ===")
    print(f"Input text type: {type(text)}")
    print(f"Input text: {text}")

    if not text:
        print("Empty input received")
        return []

    days = []
    current_day = None

    try:
        # Split the text into lines
        lines = str(text).split('\n')
        print(f"Number of lines to process: {len(lines)}")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            print(f"Processing line: {line}")

            # Check for day headers
            if '### Day' in line:
                day_match = re.search(r'Day\s*(\d+)', line)
                if day_match:
                    day_num = day_match.group(1)
                    current_day = {
                        'date': f'Day {day_num}',
                        'activities': []
                    }
                    days.append(current_day)
                    print(f"Created new day: {current_day['date']}")
                continue

            # Check for activities
            if current_day is None:
                current_day = {
                    'date': 'Day 1',
                    'activities': []
                }
                days.append(current_day)

            activity_match = re.match(r'^\d+\.\s+\*\*([^*]+)\*\*', line)
            if activity_match:
                activity_name = activity_match.group(1).strip()
                activity = {
                    'name': activity_name,
                    'description': '',
                    'location': '',
                    'why_its_suitable': '',
                    'rating': ''
                }
                current_day['activities'].append(activity)
                print(f"Added activity: {activity_name}")
                continue

            # Update activity details
            if current_day and current_day['activities']:
                current_activity = current_day['activities'][-1]
                if '**Location**:' in line:
                    current_activity['location'] = line.split('**Location**:')[1].strip()
                elif '**Description**:' in line:
                    current_activity['description'] = line.split('**Description**:')[1].strip()
                elif '**Suitability**:' in line:
                    current_activity['why_its_suitable'] = line.split('**Suitability**:')[1].strip()
                elif '**Rating**:' in line:
                    current_activity['rating'] = line.split('**Rating**:')[1].split('-')[0].strip()

        print("\n=== Parse Results ===")
        print(f"Total days: {len(days)}")
        for day in days:
            print(f"Day {day['date']}: {len(day['activities'])} activities")

        return days

    except Exception as e:
        print(f"Error in parsing: {str(e)}")
        print(traceback.format_exc())
        return []


@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    try:
        print("\n=== New Request Received ===")
        data = request.json
        print(f"Request data: {data}")

        # Validate inputs
        required_fields = ['age', 'gender', 'personality', 'days', 'destination']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f"Missing required field: {field}"
                }), 400

        inputs = {
            'age': data.get('age'),
            'gender': data.get('gender'),
            'personality': data.get('personality'),
            'days': data.get('days'),
            'destination': data.get('destination')
        }
        print(f"Processed inputs: {inputs}")

        # Get travel plan
        response = safe_crew_execution(inputs)
        print("\n=== Processing Response ===")
        print(f"Response type: {type(response)}")
        print(f"Raw response: {response}")

        # Convert to parseable format
        if hasattr(response, 'to_dict'):
            raw_output = response.to_dict()
        else:
            raw_output = response
        print(f"Converted output: {raw_output}")

        # Get text to parse
        if isinstance(raw_output, dict):
            raw_text = (raw_output.get('response', '') or
                        raw_output.get('plan', '') or
                        str(raw_output))
        else:
            raw_text = str(raw_output)
        print(f"Text to parse: {raw_text}")

        # Parse the plan
        structured_plan = parse_itinerary(raw_text)
        print(f"Final structured plan: {structured_plan}")

        if not structured_plan:
            return jsonify({
                'success': False,
                'error': 'No valid travel plan was generated. Please try again.'
            }), 500

        return jsonify({
            'success': True,
            'plan': structured_plan
        })

    except Exception as e:
        print(f"Final error: {str(e)}")
        print("Full traceback:")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f"An error occurred: {str(e)}"
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
