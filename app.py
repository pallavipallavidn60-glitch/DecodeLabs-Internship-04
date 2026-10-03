from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# --- THE STATE VAULT (Slide 11: State Management) ---
# We initialize the score here. This acts as the backend's memory.
score = 0

# --- THE QUESTION BLOCK MICRO-ARCHITECTURE (Slide 12) ---
# The reference solutions (Static Data)
QUESTIONS = {
    "q1": "paris",      # What is the capital of France?
    "q2": "8",          # How many planets are in our solar system?
    "q3": "python"      # What programming language is this project written in?
}

@app.route('/')
def home():
    # Serve the HTML file
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/api/quiz', methods=['POST'])
def quiz_engine():
    """
    This function handles the core logic loop:
    Input -> Sanitize -> Evaluate -> Execute (Update State) -> Output
    """
    global score
    
    # 1. INPUT & CAPTURE (Slide 12)
    data = request.get_json()
    user_answer = data.get('answer', '')
    question_id = data.get('question_id', '')

    # 2. SANITIZE (Slide 6, 7, 12 - The Pro Recipe)
    # We apply .strip() to remove whitespace and .lower() to normalize case.
    sanitized_input = user_answer.strip().lower()

    # 3. EVALUATE (Slide 10: The Logic Gate)
    correct_answer = QUESTIONS.get(question_id)
    
    is_correct = False
    feedback_message = ""

    if correct_answer is not None:
        if sanitized_input == correct_answer:
            is_correct = True
            score += 1  # 4. UPDATE STATE (Slide 11: += 1)
            feedback_message = "Correct! +1 Point"
        else:
            feedback_message = f"Incorrect. The answer was {correct_answer.capitalize()}."
    else:
        feedback_message = "Error: Question ID not found."

    # 5. OUTPUT (Slide 13: F-String Injector)
    # We return the current state to the frontend.
    return jsonify({
        "status": "success",
        "correct": is_correct,
        "message": feedback_message,
        "current_score": score
    })

@app.route('/api/reset', methods=['POST'])
def reset_score():
    """Resets the Score Vault for a new game."""
    global score
    score = 0
    return jsonify({"status": "reset", "score": score})

if __name__ == '__main__':
    # Run the server locally
    app.run(debug=True, port=5000)