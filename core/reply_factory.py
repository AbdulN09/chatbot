
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    current_question = answer.get_current_question(current_question_id)
    

    if not answer.validate_answer(current_question, session[answer]):
        return "Invalid answer. Please try again."


    answer.store_answer(current_question_id, current_question, session[answer])
    return True, "Answer recorded."


def get_next_question(self,current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    questions = self.get_questions(current_question_id)
    
  
    current_question_index = self.get_current_question_index(current_question_id)
    

    if current_question_index < len(questions):
        next_question = questions[current_question_index]
        self.update_current_question_index(current_question_id, current_question_index + 1)
        return next_question
    

    return "You have completed the quiz. Please submit your answers to see the results."

    


def generate_final_response(self,session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    answers = self.get_user_answers(session)
    

    score = self.calculate_score(answers)
    
 
    response = f"Your final score is {score}/{len(answers)}. "
    

    if score == len(answers):
        response += "Excellent work! You got all the answers right!"
    elif score >= len(answers) / 2:
        response += "Good job! You got more than half of the answers right."
    else:
        response += "Keep practicing! You'll get better with more quizzes."
    
    return response


