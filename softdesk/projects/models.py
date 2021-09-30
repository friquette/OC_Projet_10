from django.db import models
from django.utils import timezone

from users.models import User

TYPE_CHOICES = [
    ('be', 'Back-end'),
    ('fe', 'Front-end'),
    ('ios', 'iOS'),
    ('and', 'Android')
]

TAG_CHOICES = [
    ('bu', 'Bug'),
    ('am', 'Amélioration'),
    ('ta', 'Tâche')
]

PRIORITY_CHOICES = [
    ('fa', 'Faible'),
    ('mo', 'Moyenne'),
    ('el', 'Elevée')
]

STATUS_CHOICES = [
    ('af', 'A faire'),
    ('ec', 'En cours'),
    ('te', 'Terminé')
]

ROLE = [
    ('auth', 'Author'),
    ('cont', 'Contributor')
]

PERMISSION = [
    ('cere', 'Create/Read'),
    ('upde', 'Update/Delete')
]


class Projects(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Contributors(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, blank=True)
    permission = models.CharField(max_length=4, choices=PERMISSION, blank=True)
    role = models.CharField(max_length=4, choices=ROLE, blank=True)

    def __str__(self):
        return self.project_id.title


class Issues(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    tag = models.CharField(max_length=2, choices=TAG_CHOICES)
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    author_user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        blank=True
    )
    assignee_user_id = models.ManyToManyField(Contributors, related_name='assignee', blank=True)
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - {self.tag}"


class Comments(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=300)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE, blank=True)
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description
