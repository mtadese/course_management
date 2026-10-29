from django.contrib import admin
from .models import Student, Course, Enrollment, Result

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_number",
        "get_first_name",
        "get_last_name",
        "get_email",
        "date_of_birth",
    )
    search_fields = (
        "student_number",
        "user__first_name",
        "user__last_name",
        "user__email",
    )
    readonly_fields = ("student_number", "created_at")

    @admin.display(description="First name", ordering="user__first_name")
    def get_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description="Last name", ordering="user__last_name")
    def get_last_name(self, obj):
        return obj.user.last_name

    @admin.display(description="Email", ordering="user__email")
    def get_email(self, obj):
        return obj.user.email


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "credits", "is_active")
    list_filter = ("is_active", "credits")
    search_fields = ("code", "title")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at")
    list_filter = ("course",)
    search_fields = (
        "student__student_number",
        "student__user__first_name",
        "student__user__last_name",
        "course__code",
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("get_student", "get_course", "score", "updated_at")
    list_filter = ("enrollment__course",)

    @admin.display(description="Student")
    def get_student(self, obj):
        return obj.enrollment.student

    @admin.display(description="Course")
    def get_course(self, obj):
        return obj.enrollment.course