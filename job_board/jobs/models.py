from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    other_names = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'  # Use email as the username for authentication
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self) -> str:
        return f"{self.first_name} {self.other_names}"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "other_names": self.other_names,
            "email": self.email,
            "username": self.username,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
        }


class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "category": self.category,
            "posted_by": {
                "id": self.posted_by.id,
                "full_name": f"{self.posted_by.first_name} {self.posted_by.other_names}"
            },
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
        }


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "id": self.id,
            "job": {
                "title": self.job.title,
                "company": self.job.company,
                "location": self.job.location
            },
            "applicant": {
                "id": self.applicant.id,
                "full_name": f"{self.applicant.first_name} {self.applicant.other_names}"
            },
            "cover_letter": self.cover_letter,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
        }
