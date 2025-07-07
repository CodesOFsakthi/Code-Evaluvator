import google.generativeai as genai


genai.configure(api_key="AIzaSyAtoba2HJx3XcgR_4ZsJ7xhiYtxlJi87cE")

model = genai.GenerativeModel("gemini-pro")

def generate_feedback(question, user_code, language):
    prompt = f"""
You are reviewing a student's code submission written in {language}.

Question:
{question}pip install google-generativeai


Student's Code:
{user_code}

Your Tasks:
1. Check if the logic is correct (be lenient on minor syntax issues like missing colons or typos).
2. If the logic is correct, give time/space complexity and suggest improvements.
3. If the logic is incorrect, explain clearly what's wrong and how to improve.
4. Use a friendly and motivational tone.

Output format:
✅ Logic Feedback
⚠️ Syntax Notes (if needed)
🧠 Suggestions
🕒 Time & Space Complexity
"""
    response = model.generate_content(prompt)
    return response.text.strip()
