from django.db import models

class StudentProfile(models.Model):
    LEVELS = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]

    name = models.CharField(max_length=100)
    native_language = models.CharField(max_length=50, default="Tamil")
    level = models.CharField(max_length=20, choices=LEVELS, default="Beginner")
    grammar_score = models.PositiveIntegerField(default=0)
    vocabulary_score = models.PositiveIntegerField(default=0)
    reading_score = models.PositiveIntegerField(default=0)
    writing_score = models.PositiveIntegerField(default=0)
    speaking_score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def overall_score(self):
        scores = [
            self.grammar_score,
            self.vocabulary_score,
            self.reading_score,
            self.writing_score,
            self.speaking_score,
        ]
        return round(sum(scores) / len(scores), 1) if scores else 0

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="messages")
    user_message = models.TextField()
    tutor_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.created_at:%Y-%m-%d %H:%M}"


class QuizResult(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="quiz_results")
    topic = models.CharField(max_length=100)
    score = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def percentage(self):
        return round((self.score / self.total) * 100, 1) if self.total else 0

    def __str__(self):
        return f"{self.student.name} - {self.topic}"
