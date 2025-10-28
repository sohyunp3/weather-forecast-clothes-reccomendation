# import openai
# from openai import OpenAI

# client = OpenAI(api_key="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")

# def get_clothing_recommendation(weather_data):
#     """
#     Generates a clothing recommendation for today and tomorrow based on weather data.
#     """
#     try:
#         # Extract weather data for today and tomorrow
#         today_weather = weather_data["properties"]["periods"][0]  # Today's forecast
#         tomorrow_weather = weather_data["properties"]["periods"][1]  # Tomorrow's forecast

#         # Build the OpenAI prompt
#         prompt = f"""
#         Based on the following weather information, recommend appropriate clothes:
#         - Today: {today_weather['shortForecast']}, {today_weather['temperature']}°{today_weather['temperatureUnit']}
#         - Tomorrow: {tomorrow_weather['shortForecast']}, {tomorrow_weather['temperature']}°{tomorrow_weather['temperatureUnit']}
        
#         Provide separate recommendations for today and tomorrow.
#         """

#         print("prompt: ", prompt)

#         print("client.api_key: ", client.api_key)

#         # Call OpenAI API
#         response = client.completions.create(
#             model="davinci-002",
#             prompt=prompt,
#             max_tokens=150,
#             temperature=0.7
#         )

#         # Extract recommendation from response
#         recommendation = response.choices[0].text.strip()
#         return recommendation

#     except openai.OpenAIError as e:
#         print(f"Error with OpenAI API: {e}")
#         return "Unable to provide clothing recommendation at this time."

#######################
# import google.generativeai as genai

# genai.configure(api_key="AIzaSyAnBXKjPxsyijztu9odLVhiHuPS7G7NEb4")
# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("Explain how AI works")
# print(response.text)
#####################

import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key="AIzaSyAnBXKjPxsyijztu9odLVhiHuPS7G7NEb4")

def get_clothing_recommendation(weather_data):
    """
    Generates a clothing recommendation for today and tomorrow based on weather data.
    """
    try:
        # Extract weather data for today and tomorrow
        today_weather = weather_data["properties"]["periods"][0]
        tomorrow_weather = weather_data["properties"]["periods"][1]

        # Build the Gemini (Google Generative AI) prompt
        prompt = f"""
        Based on the following weather information, recommend appropriate clothes:
        - Today: {today_weather['shortForecast']}, {today_weather['temperature']}°{today_weather['temperatureUnit']}
        - Tomorrow: {tomorrow_weather['shortForecast']}, {tomorrow_weather['temperature']}°{tomorrow_weather['temperatureUnit']}
        
        Provide separate recommendations for today and tomorrow.
        """

        # Call Gemini API (text generation model)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        print(response.text)

        # response = genai.generate_text(
        #     model="gemini-1.5-flash",  # Gemini text model
        #     prompt=prompt,
        #     temperature=0.7,
        #     max_output_tokens=150
        # )
        
        return response.text

    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return "Unable to provide clothing recommendation at this time."
