from rest_framework import serializers
from .models import Team, TeamMember

# 只负责创建团队时的数据校验。
class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description']

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("团队名称至少 2 个字符")
        return value.strip()

# 把团队成员信息序列化出来。
class TeamMemberSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = TeamMember
        fields = ['id', 'user_id', 'username', 'email', 'role', 'joined_at']

# 给团队列表页用，字段少一点。
class TeamListSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'owner_username', 'member_count', 'created_at']

    def get_member_count(self, obj):
        return obj.members.count()

# 给团队详情页用，字段更多，还包含 members。
class TeamDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    members = TeamMemberSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'description',
            'owner_username',
            'member_count',
            'created_at',
            'updated_at',
            'members',
        ]

    def get_member_count(self, obj):
        return obj.members.count()