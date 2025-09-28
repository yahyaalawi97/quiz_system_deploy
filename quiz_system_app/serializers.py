from rest_framework import serializers
from .models import Quiz

class QuizSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'desc', 'created_by', 'created_at']
# to print first name and last name insted of id in created_by 
    def get_created_by(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"
