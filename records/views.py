from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import StudentRegistrationForm, StudentLoginForm, ResultForm
from .models import Student, Course, Enrollment, Result

User = get_user_model()


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = StudentRegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            user = form.save()
            student = Student.objects.create(
                user=user,
                date_of_birth=form.cleaned_data["date_of_birth"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
            )

            Enrollment.objects.bulk_create([
                Enrollment(student=student, course=course)
                for course in form.cleaned_data["courses"]
            ])

        messages.success(request, "Registration successful.")
        return redirect("login")

    return render(
        request, "records/register.html", {"form": form}
    )


def student_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = StudentLoginForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        identifier = form.cleaned_data["username"].strip()
        password = form.cleaned_data["password"]

        # Support login by student number as well as username.
        username = identifier
        if identifier.upper().startswith("STU-"):
            student = Student.objects.filter(
                student_number__iexact=identifier
            ).select_related("user").first()

            username = student.user.username if student else identifier

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if (
            user is not None
            and user.is_active
            and not user.is_staff
            and not user.is_superuser
        ):
            login(request, user)
            return redirect("dashboard")

        form.add_error(None, "Invalid student login details.")

    return render(request, "records/login.html", {"form": form})


@require_POST
def student_logout(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    # Staff accounts use Django Admin in this starter version.
    if request.user.is_staff:
        return redirect("/admin/")

    student = get_object_or_404(
        Student.objects.prefetch_related(
            "enrollments__course",
            "enrollments__result",
        ),
        user=request.user,
    )

    return render(
        request,
        "records/dashboard.html",
        {"student": student},
    )


def course_list(request):
    courses = Course.objects.filter(is_active=True).order_by("code")
    return render(
        request, "records/courses.html", {"courses": courses}
    )


@user_passes_test(is_staff_user)
def student_list(request):
    students = Student.objects.select_related("user").order_by(
        "student_number"
    )
    return render(
        request, "records/students.html", {"students": students}
    )


@user_passes_test(is_staff_user)
def results_by_course(request):
    courses = Course.objects.prefetch_related(
        "enrollments__student__user",
        "enrollments__result",
    ).order_by("code")

    return render(
        request, "records/results.html", {"courses": courses}
    )


@user_passes_test(is_staff_user)
def record_result(request, enrollment_id):
    enrollment = get_object_or_404(
        Enrollment.objects.select_related(
            "student__user", "course"
        ),
        pk=enrollment_id,
    )

    result = Result.objects.filter(
        enrollment=enrollment
    ).first()

    form = ResultForm(
        request.POST or None,
        instance=result,
    )

    if request.method == "POST" and form.is_valid():
        saved_result = form.save(commit=False)
        saved_result.enrollment = enrollment
        saved_result.save()
        messages.success(request, "Result saved.")
        return redirect("results")

    return render(
        request,
        "records/record_result.html",
        {"form": form, "enrollment": enrollment},
    )