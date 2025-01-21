from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserSchema, LoginSchema, JobSchema, JobApplicaitonSchema
from .models import User, Job, JobApplication
from datetime import datetime
import logging

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


"""
    USERS APIs
"""
# API to register a user
class RegisterUserAPIView(APIView):
    def post(self, request):
        try:
            logger.info("RegisterUserAPIView: Registration request received.")
            
            try:
                data = UserSchema(**request.data)
                logger.debug(f"RegisterUserAPIView: Data validated: {data}")
            except Exception as validation_error:
                logger.error(f"Validation Error: {validation_error.errors()}")
                return Response({
                    "success": False,
                    "message": "Validation errors occurred.",
                    "errors": str(validation_error.errors())
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = User.objects.create(
                    first_name=data.first_name,
                    other_names=data.other_names,
                    email=data.email,
                    username=data.username,
                    password=make_password(data.password),
                    date_created=datetime.now()
                )
                logger.info(f"User created successfully: {user.username}")
                return Response({
                    "success": True,
                    "message": "User registered successfully!",
                    "data": user.to_dict()
                }, status=status.HTTP_201_CREATED)
                
            except Exception as db_error:
                logger.error(f"Database Error: {db_error}")
                return Response({
                    "success": False,
                    "message": "An error occurred while creating the user.",
                    "errors": db_error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            logger.error(f"Internal Server Error: {e}", exc_info=True)
            return Response({
                "success": False,
                "message": "An unexpected error occurred. Please try again later.",
                "errors": e
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API to log in a user
class LoginUserAPIView(APIView):
    def post(self, request):
        try:
            logger.info("LoginUserAPIView: Login request received.")
            
            try:
                data = LoginSchema(**request.data)
            except Exception as validation_error:
                logger.error(f"Validation Error: {validation_error.errors()}")
                return Response({
                    "success": False,
                    "message": "Validation errors occurred.",
                    "errors": str(validation_error.errors())
                }, status=status.HTTP_400_BAD_REQUEST)
            
            identifier = data.identifier
            password = data.password
            
            try:
                if '@' in identifier:
                    user = User.objects.filter(email=identifier).first()
                else:
                    user = User.objects.filter(username=identifier).first()
                
                if user and check_password(password, user.password):
                    refresh = RefreshToken.for_user(user)
                    logger.info(f"LoginUserAPIView: Login successfully for user: {user.username}")
                    return Response({
                        "success": True,
                        "message": "Login successfully!",
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                    }, status=status.HTTP_200_OK)
                else:
                    logger.info("LoginUserAPIView: Login failed: Invalid username or password.")
                    return Response({
                        "success": False,
                        "message": "Invalid username or password!"
                    }, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as db_error:
                logger.error(f"LoginUserAPIView: Database Error during login: {db_error}")
                return Response({
                    "success": False,
                    "message": "An error occurred while authenticating the user.",
                    "errors": db_error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            logger.error(f"LoginUserAPIView: Internal Server Error: {e}", exc_info=True)
            return Response({
                "success": False,
                "message": "An unexpected error occurred. Please try again later.",
                "errors": e
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



"""
    JOBS APIs
"""

# View to retrieve, create jobs
class JobsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    """
        Retrieve all jobs.
    """
    def get(self, request):
        try:
            logger.info("JobsAPIView: Get jobs request received.")
            jobs = Job.objects.all()
            jobs_list = [job.to_dict() for job in jobs]
            
            if len(jobs_list) == 0:
                logger.info("JobsAPIView: Jobs not found!")
                return Response({
                    "success": False,
                    "message": "Jobs not found!"
                }, status=status.HTTP_404_NOT_FOUND)
                
            logger.info("JobsAPIView: Jobs found successfully!")
            return Response({
                "success": True, 
                "message": "Jobs found successfully!",
                "data": jobs_list
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"JobsAPIView: Error retrieving jobs: {e}")
            return Response({
                "success": False, 
                "message": "An unexpected error occurred. Please try again later."
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    """
        Create a new job posting.
    """
    def post(self, request):
        try:
            logger.info("JobsAPIView: Create a job post request received.")
            
            try:
                data = JobSchema(**request.data)
                logger.debug(f"JobsAPIView: Data validated: {data}")
                
            except Exception as validation_error:
                logger.error(f"Validation Error: {str(validation_error.errors())}")
                return Response({
                    "success": False,
                    "message": "Validation errors occurred.",
                    "errors": str(validation_error.errors())
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # Check authenticated user
            if not isinstance(request.user, User):
                logger.error(f"Authenticated user is not a valid User instance: {request.user}")
                return Response({
                    "success": False,
                    "message": "Authentication error. User is not valid."
                }, status=status.HTTP_401_UNAUTHORIZED)

            logger.debug(f"Authenticated user: {request.user} (ID: {request.user.id})")
                
            job = Job.objects.create(
                title=data.title,
                company=data.company,
                location=data.location,
                description=data.description,
                category=data.category,
                posted_by=request.user,
                date_created=datetime.now()
            )
            return Response({
                "success": True, 
                "message": "Job created successfully!", 
                "data": job.to_dict()
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"JobsAPIView: Internal Server Error: {e}", exc_info=True)
            return Response({
                "success": False,
                "message": "An unexpected error occurred. Please try again later.",
                "errors": e
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    """
        Retrieve details of a specific job.
    """
    def get(self, request, job_id):
        try:
            logger.info(f"JobDetailAPIView: GET /jobs/{job_id} - Retrieving job details")
            job = Job.objects.filter(id=job_id).first()
            
            if not job:
                logger.info(f"JobDetailAPIView: GET /jobs/{job_id} - Job not found!")
                return Response({
                    "success": False, 
                    "message": "Job not found!"
                }, status=status.HTTP_404_NOT_FOUND)
                
            logger.info(f"JobDetailAPIView: GET /jobs/{job_id} - Retrieved job details: {job.to_dict()}.")
            return Response({
                "success": True, 
                "data": job.to_dict()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"JobDetailAPIView: Error retrieving job details: {e}")
            return Response({
                "success": False, 
                "message": "AAn unexpected error occurred. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    """
        Update a specific job.
    """
    def put(self, request, job_id):
        try:
            logger.info(f"JobDetailAPIView: PUT /jobs/{job_id} - Updating job details")
            job = Job.objects.filter(id=job_id).first()
            
            if not job:
                logger.info(f"JobDetailAPIView: PUT /jobs/{job_id} - Job not found!")
                return Response({
                    "success": False, 
                    "message": "Job not found!"
                }, status=status.HTTP_404_NOT_FOUND)
                
            for attr, value in request.data.items():
                setattr(job, attr, value)
            job.save()
            
            logger.info(f"JobDetailAPIView: PUT /jobs/{job_id} - Job updated successfully: {job.to_dict()}.")
            return Response({
                "success": True, 
                "message": "Job updated successfully!", 
                "data": job.to_dict()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"JobDetailAPIView: Error updating job: {e}")
            return Response({
                "success": False, 
                "message": "An unexpected error occurred. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

    """
        Delete a specific job.
    """
    def delete(self, request, job_id):
        try:
            logger.info(f"JobDetailAPIView: DELETE /jobs/{job_id} - Deleting job.")
            job = Job.objects.filter(id=job_id).first()
            
            if not job:
                logger.info(f"JobDetailAPIView: DELETE /jobs/{job_id} - Job not found!")
                return Response({
                    "success": False, 
                    "message": "Job not found!"
                }, status=status.HTTP_404_NOT_FOUND)
            job.delete()
            
            logger.info(f"JobDetailAPIView: DELETE /jobs/{job_id} - Job deleted successfully.")
            return Response({
                "success": True, 
                "message": "Job deleted successfully."
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"JobDetailAPIView: Error deleting job: {e}")
            return Response({
                "success": False, 
                "message": "An unexpected error occurred. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            

"""
    JOB APPLICATION APIs
"""

# API to create a job application
class CreateJobApplicationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        logger.info(f"CreateJobApplicationAPIView: POST /jobs/{job_id}/apply - Job application request received.")
        try:
            # Validate job existence
            job = Job.objects.filter(id=job_id).first()
            
            if not job:
                logger.info(f"CreateJobApplicationAPIView: POST /jobs/{job_id}/apply - Job not found!")
                return Response({
                    "success": False, 
                    "message": "Job not found!"
                }, status=status.HTTP_404_NOT_FOUND)

            # Validate request data
            try:
                data = JobApplicaitonSchema(**request.data)
                logger.debug(f"CreateJobApplicationAPIView: Data validated: {data}")
                
            except Exception as validation_error:
                logger.error(f"Validation Error: {validation_error.errors()}")
                return Response({
                    "success": False,
                    "message": "Validation errors occurred.",
                    "errors": str(validation_error.errors())
                }, status=status.HTTP_400_BAD_REQUEST)
                
            
            if job.posted_by == request.user:
                logger.info(f"CreateJobApplicationAPIView: The applicant can't apply to the job that they posted!")
                return Response({
                    "success": False,
                    "message": "The applicant can't apply to the job that they posted!"
                }, status=status.HTTP_409_CONFLICT)
            
            # Ensure user hasn't already applied
            existing_application = JobApplication.objects.filter(job=job, applicant=request.user).first()
            
            if existing_application:
                logger.info(f"CreateJobApplicationAPIView: User {request.user.id} already applied for job {job_id}.")
                return Response({
                    "success": False,
                    "message": "You have already applied for this job."
                }, status=status.HTTP_409_CONFLICT)

            # Create job application
            application = JobApplication.objects.create(
                job=job,
                applicant=request.user,
                cover_letter=data.cover_letter,
                date_created=datetime.now()
            )

            logger.info(f"CreateJobApplicationAPIView: Job application created successfully for job {job_id}.")
            return Response({
                "success": True,
                "message": "Application submitted successfully!",
                "data": application.to_dict()
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error while creating job application: {e}", exc_info=True)
            return Response({
                "success": False,
                "message": "An internal error occurred. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# API to get all applications for a specific job (for job poster)
class JobApplicationsByOwnerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        logger.info(f"JobApplicationsByOwnerAPIView: GET /jobs/{job_id}/applications/owner - Retrieving applications for job posted by user.")
        try:
            # Check if the job exists
            job = Job.objects.filter(id=job_id).first()
            
            if not job:
                logger.info(f"JobApplicationsByOwnerAPIView: GET /jobs/{job_id}/applications/owner - Job not found!")
                return Response({
                    "success": False, 
                    "message": "Job not found!"
                }, status=status.HTTP_404_NOT_FOUND)

            # Check if the user requesting is the owner of the job
            if job.posted_by != request.user:
                logger.info(f"JobApplicationsByOwnerAPIView: Unauthorized access by user {request.user.id} for job {job_id} applications.")
                return Response({
                    "success": False,
                    "message": "You are not authorized to view applications for this job."
                }, status=status.HTTP_403_FORBIDDEN)

            # Retrieve all applications for the job
            applications = JobApplication.objects.filter(job=job)
            applications_list = [app.to_dict() for app in applications]
            
            if len(applications_list) == 0:
                logger.info("JobApplicationsByOwnerAPIView: Job doesn't have applications yet!")
                return Response({
                    "success": False,
                    "message": "Job doesn't have applications yet!"
                }, status=status.HTTP_404_NOT_FOUND)
                

            logger.info(f"JobApplicationsByOwnerAPIView: Retrieved {len(applications_list)} applications successfully for job {job_id}.")
            return Response({
                "success": True,
                "message": "Job applications found successfully!",
                "data": applications_list
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"JobApplicationsByOwnerAPIView: Error while retrieving applications for job {job_id}: {e}", exc_info=True)
            return Response({
                "success": False,
                "message": "An internal error occurred. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API to get details of a specific application
class JobApplicationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id):
        logger.info(f"JobApplicationDetailAPIView: GET /applications/{application_id} - Retrieving job application details.")
        try:
            # Retrieve the application
            application = JobApplication.objects.filter(id=application_id).first()
            
            if not application:
                logger.info(f"JobApplicationDetailAPIView: GET /applications/{application_id} - Job application not found!")
                return Response({
                    "success": False, 
                    "message": "Job application not found!"
                }, status=status.HTTP_404_NOT_FOUND)

            # Check if the user is authorized to view the application
            if application.job.posted_by != request.user and application.applicant != request.user:
                logger.info(f"JobApplicationDetailAPIView: Unauthorized access to application {application_id} by user {request.user.id}.")
                return Response({
                    "success": False,
                    "message": "You are not authorized to view this application."
                }, status=status.HTTP_403_FORBIDDEN)

            logger.info(f"JobApplicationDetailAPIView: Application details retrieved successfully for application {application_id}.")
            return Response({
                "success": True,
                "message": "Job application found successfully!",
                "data": application.to_dict()
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"JobApplicationDetailAPIView: Error while retrieving application {application_id}: {e}", exc_info=True)
            return Response({
                "success": False,
                "message": "An internal error occurred. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
"""
    Search API
"""            
class SearchJobsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info("SearchJobsAPIView: Search request received.")

        try:
            # Retrieve query parameters
            title = request.query_params.get("title")
            company = request.query_params.get("company")
            location = request.query_params.get("location")
            keywords = request.query_params.get("keywords")

            # Build query using Q objects for flexible filtering
            query = Q()
            if title:
                query &= Q(title__icontains=title)
            if company:
                query &= Q(company__icontains=company)
            if location:
                query &= Q(location__icontains=location)
            if keywords:
                query &= Q(description__icontains=keywords)

            # Fetch jobs based on the query
            jobs = Job.objects.filter(query)
            jobs_list = [job.to_dict() for job in jobs]

            if not jobs_list:
                logger.info("SearchJobsAPIView: No jobs found matching search criteria.")
                return Response({
                    "success": False,
                    "message": "No jobs found matching search criteria."
                }, status=status.HTTP_404_NOT_FOUND)

            logger.info(f"SearchJobsAPIView: Found {len(jobs_list)} job(s) matching criteria.")
            return Response({
                "success": True,
                "message": "Jobs found successfully!",
                "data": jobs_list
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"SearchJobsAPIView: Error during search: {e}", exc_info=True)
            return Response({
                "success": False,
                "message": "An unexpected error occurred during the search. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)