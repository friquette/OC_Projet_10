from django.urls import path
from .views import (
    CreateAndListProjects,
    ProjectsDetails,
    CreateAndListContributors,
    deleteContributors,
    CreateAndListIssues,
    UpdateAndDeleteIssues,
    CreateAndListComments,
    CommentsDetails
)
from .models import Contributors

contributors = Contributors.user_id
urlpatterns = [
    path('projects/', CreateAndListProjects.as_view()),
    path('projects/<int:pk>/', ProjectsDetails.as_view()),
    path('projects/<int:pk>/users/', CreateAndListContributors.as_view()),
    path('projects/<int:project_id>/users/<str:user_id>', deleteContributors),
    path('projects/<int:project_id>/issues/', CreateAndListIssues.as_view()),
    path('projects/<int:project_id>/issues/<int:pk>', UpdateAndDeleteIssues.as_view()),
    path('projects/<int:project_id>/issues/<int:pk>/comments', CreateAndListComments.as_view()),
    path(
        'projects/<int:project_id>/issues/<int:pk>/comments/<int:comment_id>',
        CommentsDetails.as_view()
    ),
]
