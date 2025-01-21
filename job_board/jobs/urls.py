from django.urls import path
from .views import LoginUserAPIView, RegisterUserAPIView, JobsAPIView, JobDetailAPIView, \
    JobApplicationDetailAPIView, JobApplicationsByOwnerAPIView, CreateJobApplicationAPIView, \
    SearchJobsAPIView

urlpatterns = [
    path('auth/login', LoginUserAPIView.as_view(), name='login'),
    path('auth/register_user', RegisterUserAPIView.as_view(), name='register_user'),
    path('jobs', JobsAPIView.as_view(), name='jobs'),
    path('jobs/<int:job_id>', JobDetailAPIView.as_view(), name='job_detail'),
    path('jobs/<int:job_id>/apply', CreateJobApplicationAPIView.as_view(), name='apply_for_job'),
    path('jobs/<int:job_id>/applications/owner', JobApplicationsByOwnerAPIView.as_view(), name='applications_for_job_owner'),
    path('applications/<int:application_id>', JobApplicationDetailAPIView.as_view(), name='application_detail'),
    path('search', SearchJobsAPIView.as_view(), name='search_jobs'),
]
