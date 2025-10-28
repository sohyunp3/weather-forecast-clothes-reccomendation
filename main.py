# from nwsAPI import fetch_forecast_by_location
# from openai_integration import get_clothing_recommendation

# if __name__ == "__main__":
#     # Initialize user input
#     user_city = input("Enter city: ").strip()
#     user_state = input("Enter state: ").strip()

#     # Fetch forecast data
#     print(f"Fetching weather forecast for {user_city}, {user_state}...")
#     forecast_data = fetch_forecast_by_location(user_city, user_state)

#     if forecast_data:
#         print(f"Weather forecast retrieved successfully for {user_city}, {user_state}.")
        
#         # Display forecast
#         print("\nToday's weather:")
#         today = forecast_data["properties"]["periods"][0]
#         print(f"{today['name']}: {today['shortForecast']}, {today['temperature']}°{today['temperatureUnit']}")

#         print("\nTomorrow's weather:")
#         tomorrow = forecast_data["properties"]["periods"][1]
#         print(f"{tomorrow['name']}: {tomorrow['shortForecast']}, {tomorrow['temperature']}°{tomorrow['temperatureUnit']}")

#         # Get clothing recommendation
#         print("\nFetching clothing recommendations...")
#         recommendation = get_clothing_recommendation(forecast_data)
#         print("\nClothing Recommendations:")
#         print(recommendation)
#     else:
#         print(f"Could not retrieve weather forecast for {user_city}, {user_state}.")

#########################
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from nwsAPI import fetch_forecast_by_location, init_db
# from gemini_integration import get_clothing_recommendation

# app = Flask(__name__)
# CORS(app)  # Allow requests from all origins

# @app.route("/")
# def home():
#     """
#     Root endpoint to confirm the server is running.
#     """
#     return "Weather and Clothing Recommendation API is running!"

# @app.route("/get-forecast", methods=["GET", "POST"])
# def get_forecast():
#     """
#     Handles POST requests to fetch weather data and clothing recommendations.
#     """

#     if request.method == "GET":
#         return "This endpoint supports POST requests to retrieve weather and clothing recommendations."

#     try:
#         data = request.json
#         city = data.get("city")
#         state = data.get("state")

#         if not city or not state:
#             return jsonify({"error": "City and state are required"}), 400

#         # Fetch weather forecast using the provided city and state
#         forecast_data = fetch_forecast_by_location(city, state)
#         if not forecast_data:
#             return jsonify({"error": "Could not fetch weather data for {city}, {state}"}), 500

#         # Generate clothing recommendations using OpenAI
#         recommendations = get_clothing_recommendation(forecast_data)
#         return jsonify({
#             "weather": forecast_data["properties"]["periods"][:2],  # Return Today and Tomorrow
#             "recommendations": recommendations
#         })
    
#     except Exception as e:
#         print(f"Error in /get-forecast: {e}")
#         return jsonify({"error": "Internal Server Error"}), 500
    
# if __name__ == "__main__":
#     init_db()
#     app.run(debug=True)
##########################

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from nwsAPI import fetch_forecast_by_location, init_db
from gemini_integration import get_clothing_recommendation

app = Flask(__name__, static_folder="./build")  # Serve React build files
CORS(app)  # Allow cross-origin requests

@app.route("/")
def serve():
    """
    Serve the React frontend for the root route.
    """
    return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(404)
def not_found(e):
    """
    Serve index.html for all unknown routes (React Router fallback).
    """
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static_file(path):
    """
    Serve static files (e.g., JavaScript, CSS) for the React app.
    """
    return send_from_directory(app.static_folder, path)

@app.route("/get-forecast", methods=["POST"])
def get_forecast():
    """
    Fetch weather forecast and clothing recommendations.
    """
    try:
        data = request.json
        city = data.get("city")
        state = data.get("state")

        if not city or not state:
            return jsonify({"error": "City and state are required"}), 400

        # Fetch weather forecast
        forecast_data = fetch_forecast_by_location(city, state)
        if not forecast_data:
            return jsonify({"error": f"Could not fetch weather data for {city}, {state}"}), 500

        # Get clothing recommendations
        recommendations = get_clothing_recommendation(forecast_data)

        # Return weather and recommendations in JSON format
        return jsonify({
            "weather": forecast_data["properties"]["periods"][:2],  # Today and Tomorrow
            "recommendations": recommendations  # Plain text
        })

    except Exception as e:
        print(f"Error in /get-forecast: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    init_db()
    # Run the Flask app and allow connections from other devices
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)
