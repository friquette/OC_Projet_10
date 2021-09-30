from rest_framework import generics
from rest_framework.decorators import api_view
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


class CreateAndListProjects(generics.ListCreateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer


class ProjectsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer


class CreateAndListContributors(APIView):
    def get(self, request, pk):
        contributor = Contributors.objects.filter(project_id=pk)
        serializer = ContributorsSerializer(contributor, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ContributorsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                Projects.objects.get(
                    project_id=pk, author_user_id=serializer.validated_data['user_id']
                )
                serializer.validated_data['role'] = 'auth'
                serializer.validated_data['permission'] = 'upde'
            except Projects.DoesNotExist:
                serializer.validated_data['role'] = 'cont'
                serializer.validated_data['permission'] = 'cere'
            serializer.validated_data['project_id'] = Projects.objects.get(project_id=pk)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteContributors(project_id, user_id):
    contributor = Contributors.objects.get(project_id=project_id, user_id=user_id)
    contributor.delete()
    return Response(f"Contributor {contributor.user_id.first_name} {contributor.user_id.last_name} \
successfully deleted !")


class CreateAndListIssues(APIView):
    def get(self, request, project_id):
        issue = Issues.objects.filter(project_id=project_id)
        serializer = IssuesSerializer(issue, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        serializer = IssuesSerializer(data=request.data)
        if serializer.is_valid():
            project = Projects.objects.get(project_id=project_id)
            contributors = Contributors.objects.filter(project_id=project)
            serializer.validated_data['project_id'] = project
            serializer.validated_data['assignee_user_id'] = contributors
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAndDeleteIssues(APIView):
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
