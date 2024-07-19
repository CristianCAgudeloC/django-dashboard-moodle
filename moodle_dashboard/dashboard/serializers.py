from rest_framework import serializers
import datetime

class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=150)
    idnumber = serializers.CharField(max_length=150)
    firstname = serializers.CharField(max_length=150)
    lastname = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    lastaccess = serializers.SerializerMethodField()

    def get_lastaccess(self, obj):
        if obj['lastaccess']:
            return datetime.datetime.fromtimestamp(obj['lastaccess'], tz=datetime.timezone(datetime.timedelta(hours=-5))).strftime('%Y-%m-%d %H:%M:%S')
        return None

class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fullname = serializers.CharField(max_length=255)
    shortname = serializers.CharField(max_length=255)
    student_count = serializers.IntegerField()

class AttendanceSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    course_fullname = serializers.CharField(max_length=255)
    course_shortname = serializers.CharField(max_length=255)
    student_id = serializers.IntegerField()
    username = serializers.CharField(max_length=150)
    idnumber = serializers.CharField(max_length=150)
    firstname = serializers.CharField(max_length=150)
    lastname = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    lastaccess = serializers.SerializerMethodField()

    def get_lastaccess(self, obj):
        if obj['lastaccess']:
            return datetime.datetime.fromtimestamp(obj['lastaccess'], tz=datetime.timezone(datetime.timedelta(hours=-5))).strftime('%Y-%m-%d %H:%M:%S')
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for key, value in instance.items():
            if key.startswith('attendance_'):
                representation[key] = value
        return representation
