import requests


def verified_tutor_response(message, language="Tamil", level="Beginner"):
    m = message.lower().strip()

    # Present Simple
    if "present tense" in m or "present simple" in m or "simple present" in m:
        return (
            "Present Simple Tense\n\n"
            "Use: We use the Present Simple for habits, routines, "
            "and things that are generally true.\n\n"
            "Example 1:\n"
            "I go to college every day.\n"
            "Tamil: நான் தினமும் கல்லூரிக்குச் செல்கிறேன்.\n\n"
            "Example 2:\n"
            "She studies English every day.\n"
            "Tamil: அவள் தினமும் ஆங்கிலம் படிக்கிறாள்."
        )

    # Present Continuous
    if "present continuous" in m:
        return (
            "Present Continuous Tense\n\n"
            "Use: We use the Present Continuous for an action "
            "that is happening now.\n\n"
            "Example 1:\n"
            "I am eating breakfast.\n"
            "Tamil: நான் காலை உணவு சாப்பிட்டுக் கொண்டிருக்கிறேன்.\n\n"
            "Example 2:\n"
            "They are playing cricket.\n"
            "Tamil: அவர்கள் கிரிக்கெட் விளையாடிக் கொண்டிருக்கிறார்கள்."
        )

    # Past Tense
    if "past tense" in m or "simple past" in m:
        return (
            "Past Simple Tense\n\n"
            "Use: We use the Past Simple for actions that "
            "happened in the past.\n\n"
            "Example:\n"
            "I went to college yesterday.\n"
            "Tamil: நான் நேற்று கல்லூரிக்குச் சென்றேன்."
        )

    # Future Tense
    if "future tense" in m or "simple future" in m:
        return (
            "Future Tense\n\n"
            "Use: We use the Future Tense for actions that "
            "will happen later.\n\n"
            "Example:\n"
            "I will go to college tomorrow.\n"
            "Tamil: நான் நாளை கல்லூரிக்குச் செல்வேன்."
        )

    return None


def ask_ai_tutor(message, language="Tamil", level="Beginner"):

    m = message.lower().strip()

    # -------------------------------------------------
    # Sentence Correction
    # -------------------------------------------------

    if (
        "correct this sentence:" in m
        or "correct my sentence:" in m
        or "correct this:" in m
    ):

        student_sentence = message.split(":", 1)[1].strip()

        # Verified correction
        if student_sentence.lower().rstrip(".!?") == "she go to college every day":
            return (
                "Sentence Correction\n\n"
                "Incorrect:\n"
                "She go to college every day.\n\n"
                "Correct:\n"
                "She goes to college every day.\n\n"
                "Explanation:\n"
                'With "She", we use "goes" in the Present Simple.\n\n'
                "Tamil Meaning:\n"
                "அவள் தினமும் கல்லூரிக்குச் செல்கிறாள்."
            )

        # Send other sentences to Qwen
        prompt = f"""
You are an English grammar tutor.

Correct this sentence:

{student_sentence}

Return ONLY:

Incorrect:
<original sentence>

Correct:
<correct sentence>

Explanation:
<one short and accurate grammar explanation>

Tamil Meaning:
<accurate Tamil meaning>

Rules:
- Do not invent Tamil words.
- Use natural standard Tamil.
- Do not use fake transliteration.
- Do not add a Rules section.
- Do not add extra commentary.
- Do not include URLs.
"""

        try:
            response = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json={
                    "model": "qwen2.5:1.5b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()

            data = response.json()
            answer = data.get("response", "").strip()

            if answer:
                return "Sentence Correction\n\n" + answer

        except Exception:
            return (
                "Sentence Correction\n\n"
                "The local AI tutor is currently unavailable."
            )

        return "Sorry, I could not correct the sentence."

    # -------------------------------------------------
    # Verified grammar topics
    # -------------------------------------------------

    verified_answer = verified_tutor_response(
        message,
        language,
        level
    )

    if verified_answer:
        return verified_answer

    # -------------------------------------------------
    # General Qwen AI Tutor
    # -------------------------------------------------

    prompt = f"""
You are VernacularAI, an English-learning tutor.

Student native language: {language}
Student level: {level}

Rules:
1. Teach English accurately.
2. Use simple English.
3. Do not invent Tamil words.
4. Do not invent translations.
5. Do not provide fake transliterations.
6. Do not include URLs.
7. Keep answers short.
8. Give correct English examples.

Student question:
{message}
"""

    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()
        answer = data.get("response", "").strip()

        if answer:
            return answer

        return "Sorry, I could not generate an answer."

    except Exception:
        return (
            "The local AI tutor is currently unavailable. "
            "Please make sure Ollama is running."
        )