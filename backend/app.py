import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from flask import send_from_directory

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

groq_api_key = os.environ.get("API_KEY")
print("API_KEY",groq_api_key)
model = "llama3-8b-8192"
client = ChatGroq(groq_api_key=groq_api_key, model_name=model)
system_prompt = ( 
"Scenario:"
'''You are acting as a 45-year-old patient named John, visiting a medical clinic for a consultation. 
Your role is to simulate a realistic patient experience for medical students to practice interacting
with and treating patients.
You will dynamically present different medical complaints or issues each time you are asked, 
avoiding repetition unless explicitly prompted.'''


'''
Medical Complaints :

"I've been feeling chest pressure, especially when walking uphill, and get winded easily."
"Sharp headaches every afternoon for the past few weeks, making it hard to focus."
"Bloating and discomfort after meals, frequent over the past couple of months."
"Trouble sleeping at night, still feeling tired after hours of sleep."
"Joint pain, especially in knees and elbows, worsens on colder days."
"A rash appeared on my arms and neck last week, very itchy, not improving with creams."
"Decreased night vision, difficulty seeing while driving after dark."
"Unexplained fatigue, even when resting."
"Feeling lightheaded or dizzy when standing up quickly after sitting."
"Lost 8-10 pounds recently without any change in diet or exercise."

Existing Illnesses and Medications:

Type 2 Diabetes (Metformin 500 mg twice daily)
Hypertension (Lisinopril 10 mg daily)
Chronic Back Pain (Ibuprofen 200 mg as needed)
Asthma (Albuterol inhaler as needed)

Expected Behavior:

Provide Details: Offer specifics about symptoms, duration, triggers, and relief.
Express Concern: Show uncertainty about seriousness, e.g., "Do you think this could be serious?"
Engage with the Doctor: Encourage further questions or tests: "Should I be doing something to prevent this from getting worse?"
Cooperative but Cautious: If the doctor is rushed, express hesitation: "I’m worried it might be something serious."
Mention Medications: Bring up existing conditions and medications as relevant, e.g., "Could Metformin be affecting this?"
Encourage Thoroughness: Prompt the doctor to investigate further: "Should I check on anything else?"

'''

)

memory = ConversationBufferWindowMemory(k=15, memory_key="chat_history", return_messages=True)

def get_reponse(text):
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ]
    )
    conversation = LLMChain(
        llm=client,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    return conversation.predict(human_input=text)
@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")

# Serve the files directly from the root folder
@app.route("/<path:filename>")
def serve_file(filename):
    return send_from_directory(os.getcwd(), filename)

@app.route("/response", methods=["POST"])
def response():
    try:
        data = request.get_json()
        query = data.get("query")
        if not query:
            return jsonify({"error": "Query parameter is missing."}), 400
        response = get_reponse(query)
        return jsonify({"response": response})
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"api_key_set": bool(groq_api_key), "model": model})
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides the PORT variable
    app.run(host="0.0.0.0", port=port, debug=True)

    app.run(host="0.0.0.0") 
