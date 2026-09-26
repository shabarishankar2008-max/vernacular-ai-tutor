from django.contrib import admin
from .models import StudentProfile, ChatMessage, QuizResult


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "native_language",
        "level",
        "grammar_score",
        "vocabulary_score",
        "reading_score",
        "writing_score",
        "speaking_score",
        "created_at",
    )

    list_filter = (
        "level",
        "native_language",
        "created_at",
    )

    search_fields = (
        "name",
        "native_language",
    )

    ordering = (
        "-created_at",
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "short_user_message",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "student__name",
        "user_message",
        "tutor_response",
    )

    ordering = (
        "-created_at",
    )

    def short_user_message(self, obj):
        if len(obj.user_message) > 60:
            return obj.user_message[:60] + "..."
        return obj.user_message

    short_user_message.short_description = "Student Question"


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "topic",
        "score",
        "total",
        "percentage_display",
        "created_at",
    )

    list_filter = (
        "topic",
        "created_at",
    )

    search_fields = (
        "student__name",
        "topic",
    )

    ordering = (
        "-created_at",
    )

    def percentage_display(self, obj):
        return f"{obj.percentage()}%"

    percentage_display.short_description = "Percentage"