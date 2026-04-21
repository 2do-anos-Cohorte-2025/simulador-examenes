from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Exam
from .serializers import ExamSerializer

@api_view(['GET'])
def test_exam(request):
    exams = Exam.objects.all()
    serializer = ExamSerializer(exams, many=True)
    return Response(serializer.data)