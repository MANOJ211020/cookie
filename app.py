import requests
from flask import Flask, request, jsonify

from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/51b7327920f1e040f3d6fdfb22d07872/ai/run/"
headers = {"Authorization": "Bearer <your_token>"}

def generate(user_id, prompt, token, user_name, email):
    model = "@cf/mistral/mistral-7b-instruct-v0.1"
    msg = [
        {"role": "system", "content": f"You are Cookie, a Business Expert AI. Your task is to guide users through the process of refining their business models. You will ask insightful questions about their product, competition, and market. You will then analyze the responses and provide tailored advice, including funding opportunities and how to apply for them. Use resources from Y Combinator, Shark Tank, and Founders Fund to provide expert-level responses in a concise manner. The user you're assisting is {user_name}."}
    ]
    msg.append({"role": "user", "content": prompt})

    input = {"messages": msg}
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    
    try:
        data = response.json()["result"]["response"]
        # Customize the analysis
        analysis = analyze_business_idea(prompt, data)
        msg.append({"role": "assistant", "content": analysis})
        return analysis
    except:
        return "Unable to contact Cookie Engine!"

# Analyze the business idea and provide insights
def analyze_business_idea(user_input, ai_response):
    # Example analysis (can be more dynamic based on AI's response)
    analysis = f"Based on your idea: '{user_input}', here's my analysis:\n\n"
    analysis += f"1. **Product/Service**: {ai_response}.\n"
    analysis += f"2. **Competition**: Who are your competitors? What's unique about your product?\n"
    analysis += f"3. **Market Potential**: How large is your target market?\n\n"
    analysis += f"**Funding Opportunities**:\n"
    analysis += "You can apply for funding through Y Combinator, Shark Tank, or Founders Fund.\n"
    analysis += "Typically, you can secure funding in the range of 1-10 Crores INR depending on your business model and pitch.\n"
    analysis += "To apply, you should prepare a concise pitch, outline your product's uniqueness, market potential, and financial projections.\n"
    
    return analysis

@app.route('/generate', methods=['POST'])
def handle_message():
    data = request.get_json()
    user_input = data.get('user_input')
    # Assume a fixed user_id, token, etc. You can modify this to fetch real user data
    user_id = "example_user_id"
    token = "example_token"
    user_name = "John Doe"
    email = "johndoe@example.com"
    
    response = generate(user_id, user_input, token, user_name, email)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
