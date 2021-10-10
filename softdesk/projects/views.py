from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    ProjectsSerializer,
    ContributorsSerializer,
    IssuesSerializer,
    CommentsSerializer
)
from .models import Projects, Contributors, Issues, Comments


from rest_framework.views import APIView
from rest_framework import status


class CreateAndListProjects(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        project = Projects.objects.all()
        serializer = ProjectsSerializer(project, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectsSerializer(data=request.data)
        contributor = Contributors()
        if serializer.is_valid():
            serializer.validated_data['author_user_id'] = request.user
            serializer.save()

            project = Projects.objects.get(project_id=serializer.data['project_id'])
            contributor.user_id = request.user
            contributor.project_id = project
            contributor.permission = 'upde'
            contributor.role = 'auth'
            contributor.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectsDetails(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        project = Projects.objects.get(project_id=pk)
        serializer = ProjectsSerializer(project, data=request.data)
        if serializer.is_valid():
            if project.author_user_id == request.user:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                "You are not authorized to modify this project.",
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        contributors = Contributors.objects.filter(project_id=pk)
        if request.user in [c.user_id for c in contributors]:
            project = Projects.objects.get(project_id=pk)
            serializer = ProjectsSerializer(project)
            return Response(serializer.data)
        else:
            return Response(
                "You are not authorized to see the full details of this project",
                status=status.HTTP_401_UNAUTHORIZED
            )

    def delete(self, request, pk):
        project = Projects.objects.get(project_id=pk)
        if project.author_user_id == request.user:
            project.delete()
            return Response(f"Project {project} successfully deleted !")
        return Response(
            "You are not authorized to delete this project.",
            status=status.HTTP_401_UNAUTHORIZED
        )


class CreateAndListContributors(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        contributor = Contributors.objects.filter(project_id=pk)
        if request.user in [c.user_id for c in contributor]:
            serializer = ContributorsSerializer(contributor, many=True)
            return Response(serializer.data)
        else:
            return Response(
                "You are not authorized to see the contributors for this project",
                status=status.HTTP_401_UNAUTHORIZED
            )

    def post(self, request, pk):
        serializer = ContributorsSerializer(data=request.data)
        contributor = Contributors.objects.filter(project_id=pk, role='auth')
        if serializer.is_valid():
            if request.user in [c.user_id for c in contributor]:
                serializer.validated_data['project_id'] = Projects.objects.get(project_id=pk)
                if serializer.validated_data['role'] == 'auth':
                    serializer.validated_data['permission'] = 'upde'
                else:
                    serializer.validated_data['permission'] = 'cere'
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                "You are not authorized to add a contributor to this project",
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteContributors(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, project_id, user_id):
        auth_contributor = Contributors.objects.filter(project_id=project_id, role='auth')
        if request.user in [c.user_id for c in auth_contributor]:
            contributor = Contributors.objects.get(project_id=project_id, user_id=user_id)
            contributor.delete()
            return Response(
                f"Contributor {contributor.user_id.first_name} {contributor.user_id.last_name} \
successfully deleted !"
            )
        return Response(
            "You are not authorized to delete contributors for this project",
            status=status.HTTP_401_UNAUTHORIZED
        )


class CreateAndListIssues(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        contributors = Contributors.objects.filter(project_id=project_id)
        if request.user in [c.user_id for c in contributors]:
            issue = Issues.objects.filter(project_id=project_id)
            serializer = IssuesSerializer(issue, many=True)
            return Response(serializer.data)
        else:
            return Response(
                "You are not authorized to see the issues for this project",
                status=status.HTTP_401_UNAUTHORIZED
            )

    def post(self, request, project_id):
        contributors = Contributors.objects.filter(project_id=project_id)
        serializer = IssuesSerializer(data=request.data)
        print([c.user_id.user_id for c in contributors])
        if serializer.is_valid():
            if request.user in [c.user_id for c in contributors]:
                project = Projects.objects.get(project_id=project_id)
                contributors = Contributors.objects.filter(project_id=project)
                serializer.validated_data['project_id'] = project
                serializer.validated_data['assignee_user_id'] = [c.user_id for c in contributors]
                serializer.validated_data['author_user_id'] = request.user
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    "You are not authorized to create an issue for this project",
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAndDeleteIssues(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, project_id, pk):
        issue = Issues.objects.get(id=pk, project_id=project_id)
        serializer = IssuesSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, pk):
        issue = Issues.objects.get(id=pk, project_id=project_id)
        issue.delete()
        return Response(f"Issue {issue.title} for project {issue.project_id} \
successfully deleted !")


class CreateAndListComments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, pk):
        comment = Comments.objects.filter(issue_id=pk)
        serializer = CommentsSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request, project_id, pk):
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            issue = Issues.objects.get(id=pk, project_id=project_id)
            serializer.validated_data['issue_id'] = issue
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsDetails(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, project_id, pk, comment_id):
        comment = Comments.objects.get(comment_id=comment_id, issue_id=pk)
        serializer = CommentsSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, pk, comment_id):
        comment = Comments.objects.get(comment_id=comment_id, issue_id=pk)
        serializer = CommentsSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, project_id, pk, comment_id):
        comment = Comments.objects.get(comment_id=comment_id, issue_id=pk)
        comment.delete()
        return Response(f"Comment '{comment}' for project: {comment.issue_id}, \
successfully deleted !")
