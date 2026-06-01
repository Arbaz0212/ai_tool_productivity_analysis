import requests


def get_ai_advice(user_input):
    try:
        prompt = f"""
You are an expert productivity coach specializing in software development and AI tools.

User problem:
{user_input}

Give:
1. Specific actionable steps
2. Focus on reducing time and errors
3. Suggest how AI tools (ChatGPT, Copilot, etc.) can help
4. Keep it practical and concise
5. Limit to 5-6 clear bullet points
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama:latest",   # you can change later
                "prompt": prompt,
                "stream": False
            },
            timeout=60   # reduced timeout (faster failure if stuck)
        )

        # -------------------- RESPONSE HANDLING --------------------
        if response.status_code == 200:
            data = response.json()

            result = data.get("response", "").strip()

            if not result:
                return "⚠️ AI returned empty response."

            return result

        elif response.status_code == 404:
            return "❌ Model not found. Run: ollama pull tinyllama"

        else:
            return f"❌ Error: {response.status_code}"

    # -------------------- ERROR HANDLING --------------------
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to Ollama. Make sure it is running (ollama serve)."

    except requests.exceptions.Timeout:
        return "⏳ Request timed out. Try a smaller model like tinyllama."

    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"