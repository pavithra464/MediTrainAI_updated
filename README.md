# 🏥 MediTrain AI

## 📚 Introduction
MediTrain AI is an innovative application that leverages the power of AI to simulate patient interactions, providing a hands-on training tool for medical professionals. This project aims to enhance medical education by mimicking real-world scenarios in a controlled environment.

---

## 🛠️ Technologies Used

### Frontend
- **Streamlit**: Interactive and user-friendly interface.

### Backend
- **Flask**: API for handling and processing user queries.
- **LangChain**: Contextual enhancements for AI responses.
- **GROQ API**: Powers the AI chatbot for medical interactions.

---

## 🚀 Features
- **Simulated Patient Interactions**: Mimics real-life medical consultations.
- **Dynamic Context**: Adapts to various medical scenarios and patient histories.
- **Custom Responses**: Generates detailed and accurate medical guidance.

---

## 🖥️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/username/MediTrainAI.git
   ```
2. Navigate to the project directory:
   ```bash
   cd MediTrainAI
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your API keys:
   ```env
   API_KEY=your_api_key_here
   ```

---

## ⚙️ Usage
1. Run the Flask API:
   ```bash
   python api.py
   ```
2. Access the Streamlit interface:
   ```bash
   streamlit run app.py
   ```
3. Use Postman or a browser to interact with the API:
   - Endpoint: `http://127.0.0.1:5000/response`
   - Example Query:
     ```json
     {
       "query": "What are the symptoms of diabetes?"
     }
     ```

---

## 📋 Sample Code
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/response', methods=['POST'])
def respond():
    data = request.json
    user_query = data.get('query', '')
    response = f"You asked: {user_query}"
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 🤝 Contributing
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

