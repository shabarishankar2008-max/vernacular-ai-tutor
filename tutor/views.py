from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import StudentProfile, ChatMessage, QuizResult
from .services import ask_ai_tutor
import random


# =========================================================
# QUIZ QUESTION BANK
# =========================================================

QUIZ_QUESTIONS = {

    # =====================================================
    # BEGINNER
    # =====================================================

    "Beginner": [

        {
            "q": "She ___ to college every day.",
            "options": ["go", "goes", "going"],
            "answer": "goes",
            "topic": "Present Simple",
            "explanation": 'With "She", use "goes" in the Present Simple.'
        },

        {
            "q": "I ___ a student.",
            "options": ["am", "is", "are"],
            "answer": "am",
            "topic": "Basic Grammar",
            "explanation": 'With "I", use "am".'
        },

        {
            "q": "They ___ football every Sunday.",
            "options": ["play", "plays", "playing"],
            "answer": "play",
            "topic": "Present Simple",
            "explanation": 'With "They", use the base verb "play".'
        },

        {
            "q": "Choose the correct article: I saw ___ elephant.",
            "options": ["a", "an", "the"],
            "answer": "an",
            "topic": "Articles",
            "explanation": '"Elephant" begins with a vowel sound, so use "an".'
        },

        {
            "q": "The opposite of difficult is ___.",
            "options": ["easy", "slow", "late"],
            "answer": "easy",
            "topic": "Vocabulary",
            "explanation": '"Easy" is the opposite of "difficult".'
        },

        {
            "q": "He ___ his homework yesterday.",
            "options": ["finish", "finished", "finishing"],
            "answer": "finished",
            "topic": "Past Tense",
            "explanation": '"Yesterday" indicates the past tense.'
        },

        {
            "q": "She ___ a car.",
            "options": ["have", "has", "having"],
            "answer": "has",
            "topic": "Have / Has",
            "explanation": 'With "She", use "has".'
        },

        {
            "q": "We ___ students.",
            "options": ["is", "am", "are"],
            "answer": "are",
            "topic": "Basic Grammar",
            "explanation": 'With "We", use "are".'
        },

    ],


    # =====================================================
    # MODERATE
    # =====================================================

    "Moderate": [

        {
            "q": "Choose the correct sentence.",
            "options": [
                "He don't like coffee.",
                "He doesn't like coffee.",
                "He doesn't likes coffee."
            ],
            "answer": "He doesn't like coffee.",
            "topic": "Sentence Correction",
            "explanation": "After \"doesn't\", use the base verb \"like\"."
        },

        {
            "q": "I ___ studying English when he called me.",
            "options": ["am", "was", "were"],
            "answer": "was",
            "topic": "Past Continuous",
            "explanation": 'With "I", use "was" in the Past Continuous.'
        },

        {
            "q": "She has lived here ___ 2020.",
            "options": ["for", "since", "from"],
            "answer": "since",
            "topic": "Prepositions",
            "explanation": 'Use "since" with a specific starting point.'
        },

        {
            "q": "Choose the correct sentence.",
            "options": [
                "There is many students.",
                "There are many students.",
                "There am many students."
            ],
            "answer": "There are many students.",
            "topic": "Subject-Verb Agreement",
            "explanation": '"Students" is plural, so use "are".'
        },

        {
            "q": "If I ___ time, I will help you.",
            "options": ["have", "had", "having"],
            "answer": "have",
            "topic": "Conditional Sentences",
            "explanation": 'In the First Conditional, use Present Simple after "if".'
        },

        {
            "q": "He is ___ than his brother.",
            "options": ["tall", "taller", "tallest"],
            "answer": "taller",
            "topic": "Comparatives",
            "explanation": '"Than" is used with the comparative form.'
        },

        {
            "q": "Identify the incorrect word: She go to college every day.",
            "options": ["She", "go", "college"],
            "answer": "go",
            "topic": "Error Detection",
            "explanation": 'With "She", the correct form is "goes".'
        },

        {
            "q": "Choose the correct form: They ___ already finished the work.",
            "options": ["have", "has", "having"],
            "answer": "have",
            "topic": "Present Perfect",
            "explanation": 'With "They", use "have".'
        },

    ],


    # =====================================================
    # ADVANCED
    # =====================================================

    "Advanced": [

        {
            "q": "Choose the grammatically correct sentence.",
            "options": [
                "Although he was tired, but he continued working.",
                "Although he was tired, he continued working.",
                "Although he tired, but continued working."
            ],
            "answer": "Although he was tired, he continued working.",
            "topic": "Conjunctions",
            "explanation": '"Although" already shows contrast, so "but" is unnecessary.'
        },

        {
            "q": "By the time we arrived, the train ___.",
            "options": ["left", "had left", "has left"],
            "answer": "had left",
            "topic": "Past Perfect",
            "explanation": 'The earlier past action uses the Past Perfect.'
        },

        {
            "q": "Choose the correct sentence.",
            "options": [
                "If I had known, I would have helped you.",
                "If I knew, I would have helped you.",
                "If I have known, I would helped you."
            ],
            "answer": "If I had known, I would have helped you.",
            "topic": "Conditional Sentences",
            "explanation": 'This is a Third Conditional sentence.'
        },

        {
            "q": "Which sentence uses the passive voice correctly?",
            "options": [
                "The project completed by the team.",
                "The project was completed by the team.",
                "The project is complete by the team."
            ],
            "answer": "The project was completed by the team.",
            "topic": "Passive Voice",
            "explanation": 'The Past Simple Passive uses "was/were + past participle".'
        },

        {
            "q": "Choose the correct word: The manager's decision was ___ by the committee.",
            "options": ["approved", "approval", "approving"],
            "answer": "approved",
            "topic": "Vocabulary",
            "explanation": '"Approved" is the correct past participle for the passive construction.'
        },

        {
            "q": "Identify the error: Neither of the students have completed the assignment.",
            "options": ["Neither", "have", "assignment"],
            "answer": "have",
            "topic": "Error Detection",
            "explanation": '"Neither" is treated as singular here, so use "has".'
        },

        {
            "q": "Choose the best sentence.",
            "options": [
                "Despite of the rain, we went outside.",
                "Despite the rain, we went outside.",
                "Despite it was raining, we went outside."
            ],
            "answer": "Despite the rain, we went outside.",
            "topic": "Advanced Grammar",
            "explanation": '"Despite" is followed directly by a noun or gerund, not "of".'
        },

        {
            "q": "Which sentence is correctly punctuated?",
            "options": [
                "However I decided to continue.",
                "However, I decided to continue.",
                "However I, decided to continue."
            ],
            "answer": "However, I decided to continue.",
            "topic": "Punctuation",
            "explanation": 'A comma is normally used after the introductory "However".'
        },

    ],
}


# =========================================================
# GET STUDENT
# =========================================================

def get_student(request):

    student_id = request.session.get("student_id")

    if not student_id:
        return None

    try:
        return StudentProfile.objects.get(id=student_id)

    except StudentProfile.DoesNotExist:
        request.session.pop("student_id", None)
        return None


# =========================================================
# HOME
# =========================================================

def home(request):

    student = get_student(request)

    return render(
        request,
        "home.html",
        {
            "student": student
        }
    )


# =========================================================
# REGISTER STUDENT
# =========================================================

def register_student(request):

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        language = request.POST.get(
            "native_language",
            "Tamil"
        )

        level = request.POST.get(
            "level",
            "Beginner"
        )

        if name:

            student = StudentProfile.objects.create(
                name=name,
                native_language=language,
                level=level,
            )

            request.session["student_id"] = student.id

            return redirect("dashboard")

    return render(
        request,
        "register.html"
    )


# =========================================================
# AI TUTOR
# =========================================================

def tutor_chat(request):

    student = get_student(request)

    if not student:
        return redirect("register")

    messages = student.messages.order_by(
        "-created_at"
    )[:20]

    if request.method == "POST":

        user_message = request.POST.get(
            "message",
            ""
        ).strip()

        if user_message:

            answer = ask_ai_tutor(
                user_message,
                student.native_language,
                student.level,
            )

            ChatMessage.objects.create(
                student=student,
                user_message=user_message,
                tutor_response=answer,
            )

        return redirect("tutor")

    return render(
        request,
        "tutor.html",
        {
            "student": student,
            "messages": reversed(messages),
        }
    )


# =========================================================
# QUIZ
# =========================================================

def quiz(request):

    student = get_student(request)

    if not student:
        return redirect("register")


    # =====================================================
    # SUBMIT QUIZ
    # =====================================================

    if request.method == "POST":

        selected_questions = request.session.get(
            "quiz_questions"
        )

        difficulty = request.session.get(
            "quiz_difficulty"
        )

        if not selected_questions or not difficulty:
            return redirect("quiz")


        score = 0
        review = []


        # =================================================
        # CHECK ANSWERS
        # =================================================

        for i, item in enumerate(selected_questions):

            user_answer = request.POST.get(
                f"q{i}",
                "Not answered"
            )

            correct_answer = item["answer"]

            is_correct = (
                user_answer == correct_answer
            )

            if is_correct:
                score += 1


            review.append({
                "question": item["q"],
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": item["explanation"],
                "topic": item["topic"],
            })


        total = len(selected_questions)


        # =================================================
        # SAVE QUIZ RESULT
        # =================================================

        QuizResult.objects.create(
            student=student,
            topic=f"{difficulty} - English",
            score=score,
            total=total,
        )


        # =================================================
        # CALCULATE PERCENTAGE
        # =================================================

        percentage = round(
            (score / total) * 100
        )


        # =================================================
        # UPDATE STUDENT SCORES
        # =================================================

        student.grammar_score = percentage

        student.vocabulary_score = percentage

        student.reading_score = max(
            student.reading_score,
            percentage
        )

        student.writing_score = max(
            student.writing_score,
            percentage
        )

        student.save()


        # =================================================
        # SAVE REVIEW
        # =================================================

        request.session["quiz_review"] = review

        request.session["quiz_review_difficulty"] = difficulty


        # Clear current quiz

        request.session.pop(
            "quiz_questions",
            None
        )

        request.session.pop(
            "quiz_difficulty",
            None
        )


        # =================================================
        # SHOW RESULT
        # =================================================

        return render(
            request,
            "quiz_result.html",
            {
                "student": student,
                "score": score,
                "total": total,
                "percentage": percentage,
                "difficulty": difficulty,
            }
        )


    # =====================================================
    # START NEW QUIZ
    # =====================================================

    difficulty = request.GET.get(
        "difficulty"
    )


    # =====================================================
    # SHOW DIFFICULTY SELECTION
    # =====================================================

    if difficulty not in QUIZ_QUESTIONS:

        return render(
            request,
            "quiz.html",
            {
                "student": student,
                "questions": [],
                "difficulty": None,
                "difficulties": [
                    "Beginner",
                    "Moderate",
                    "Advanced",
                ],
            }
        )


    # =====================================================
    # SELECT 5 RANDOM QUESTIONS
    # =====================================================

    question_bank = QUIZ_QUESTIONS[difficulty]

    selected_questions = random.sample(
        question_bank,
        5
    )


    # =====================================================
    # SAVE QUIZ IN SESSION
    # =====================================================

    request.session["quiz_questions"] = (
        selected_questions
    )

    request.session["quiz_difficulty"] = (
        difficulty
    )


    # =====================================================
    # SHOW QUIZ
    # =====================================================

    return render(
        request,
        "quiz.html",
        {
            "student": student,
            "questions": selected_questions,
            "difficulty": difficulty,
            "difficulties": [
                "Beginner",
                "Moderate",
                "Advanced",
            ],
        }
    )


# =========================================================
# VIEW MY ANSWERS
# =========================================================

def quiz_review(request):

    student = get_student(request)

    if not student:
        return redirect("register")


    review = request.session.get(
        "quiz_review"
    )

    difficulty = request.session.get(
        "quiz_review_difficulty"
    )


    if not review:
        return redirect("quiz")


    return render(
        request,
        "quiz_review.html",
        {
            "student": student,
            "review": review,
            "difficulty": difficulty,
        }
    )


# =========================================================
# DASHBOARD
# =========================================================

def dashboard(request):

    student = get_student(request)

    if not student:
        return redirect("register")


    results = student.quiz_results.order_by(
        "-created_at"
    )[:10]


    return render(
        request,
        "dashboard.html",
        {
            "student": student,
            "results": results,
        }
    )
    # =========================================================
# ADMIN DASHBOARD
# =========================================================

@staff_member_required
def admin_dashboard(request):

    students = StudentProfile.objects.order_by("-created_at")

    quiz_results = QuizResult.objects.select_related(
        "student"
    ).order_by("-created_at")

    chat_messages = ChatMessage.objects.select_related(
        "student"
    ).order_by("-created_at")

    total_students = students.count()
    total_quizzes = quiz_results.count()
    total_messages = chat_messages.count()

    return render(
        request,
        "admin_dashboard.html",
        {
            "students": students,
            "quiz_results": quiz_results,
            "chat_messages": chat_messages,
            "total_students": total_students,
            "total_quizzes": total_quizzes,
            "total_messages": total_messages,
        },
    )