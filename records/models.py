import uuid

from django.conf import settings
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    student_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.student_number:
            self.student_number = (
                "STU-" + uuid.uuid4().hex[:10].upper()
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_number} - {self.user.get_full_name()}"


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.PositiveSmallIntegerField(default=3)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="enrollments",
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course",
            )
        ]

    def __str__(self):
        return f"{self.student} / {self.course}"


class Result(models.Model):
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.PROTECT,
        related_name="result",
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.enrollment} - {self.score}"