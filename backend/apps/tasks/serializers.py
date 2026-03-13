from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.teams.models import TeamMember
from .models import Task

User = get_user_model()


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'project',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'due_date',
        ]

    def validate_title(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("任务标题至少 2 个字符")
        return value

    def validate(self, attrs):
        project = attrs.get('project')
        assignee = attrs.get('assignee')

        if assignee:
            is_team_member = TeamMember.objects.filter(
                team=project.team,
                user=assignee
            ).exists()

            if not is_team_member:
                raise serializers.ValidationError("负责人必须是该项目所属团队成员")

        return attrs


class TaskListSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    assignee_username = serializers.CharField(
        source='assignee.username',
        read_only=True,
        default=None
    )
    creator_username = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'project',
            'project_name',
            'assignee',
            'assignee_username',
            'creator_username',
            'due_date',
            'created_at',
        ]


class TaskDetailSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    assignee_username = serializers.CharField(
        source='assignee.username',
        read_only=True,
        default=None
    )
    creator_username = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'project',
            'project_name',
            'assignee',
            'assignee_username',
            'creator',
            'creator_username',
            'due_date',
            'created_at',
            'updated_at',
        ]