from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.teams.models import TeamMember
from .models import Task, Comment, TaskAttachment

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


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
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
        project = self.instance.project
        assignee = attrs.get('assignee')

        if assignee:
            is_team_member = TeamMember.objects.filter(
                team=project.team,
                user=assignee
            ).exists()

            if not is_team_member:
                raise serializers.ValidationError("负责人必须是该项目所属团队成员")

        return attrs


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']


class TaskPriorityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['priority']


class TaskAssigneeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['assignee']

    def validate_assignee(self, value):
        task = self.instance
        if value is None:
            return value

        is_team_member = TeamMember.objects.filter(
            team=task.project.team,
            user=value
        ).exists()

        if not is_team_member:
            raise serializers.ValidationError("负责人必须是该项目所属团队成员")

        return value


class TaskListSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    assignee_username = serializers.CharField(source='assignee.username', read_only=True, default=None)
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
    assignee_username = serializers.CharField(source='assignee.username', read_only=True, default=None)
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


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'task',
            'author',
            'author_username',
            'content',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'task',
            'author',
            'author_username',
            'created_at',
        ]


class TaskAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = TaskAttachment
        fields = [
            'id',
            'task',
            'uploaded_by',
            'uploaded_by_username',
            'file',
            'file_url',
            'file_name',
            'uploaded_at',
        ]
        read_only_fields = [
            'id',
            'task',
            'uploaded_by',
            'uploaded_by_username',
            'file_name',
            'uploaded_at',
        ]

    def get_file_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url


class ProjectMemberOptionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    role = serializers.CharField()


class TaskBoardCardSerializer(serializers.ModelSerializer):
    assignee_username = serializers.CharField(
        source='assignee.username',
        read_only=True,
        default=None
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'status',
            'priority',
            'assignee_username',
            'due_date',
            'created_at',
        ]