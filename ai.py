import requests
import google.generativeai as genai


def generate_trip(
    destination,
    days,
    budget,
    interests,
    provider="ollama",
    api_key=None
):
    """
    Generate a detailed day-wise trip itinerary.

    Parameters:
        destination (str): Travel destination
        days (int): Number of days
        budget (str): Budget range
        interests (str): User interests
        provider (str): 'ollama' or 'gemini'
        api_key (str): Gemini API key (required for Gemini)

    Returns:
        str: Generated itinerary
    """

    prompt = f"""
You are an expert travel planner.

Create a detailed {days}-day travel itinerary for:

Destination: {destination}
Budget: {budget}
Interests: {interests}

Requirements:
- Provide a day-wise plan.
- Include morning, afternoon, and evening activities.
- Suggest local food to try.
- Mention estimated daily expenses.
- Keep the itinerary within the budget.
- End with travel tips.

Format clearly using headings:
Day 1
Day 2
...
"""

    provider = provider.lower()

    if provider == "ollama":
        return _generate_with_ollama(prompt)

    elif provider == "gemini":
        if not api_key:
            raise ValueError("Gemini API key is required.")
        return _generate_with_gemini(prompt, api_key)

    else:
        raise ValueError("Provider must be 'ollama' or 'gemini'")


def _generate_with_ollama(prompt):
    """
    Generate itinerary using local Ollama llama3 model.
    """

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload, timeout=120)

    if response.status_code != 200:
        raise Exception(
            f"Ollama Error: {response.status_code} - {response.text}"
        )

    data = response.json()
    return data.get("response", "No response generated.")


def _generate_with_gemini(prompt, api_key):
    """
    Generate itinerary using Gemini API.
    """

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(prompt)

    return response.text


# Example test
if __name__ == "__main__":

    itinerary = generate_trip(
        destination="Goa",
        days=3,
        budget="₹15,000",
        interests="beaches, food, nightlife",
        provider="ollama"
    )

    print(itinerary)