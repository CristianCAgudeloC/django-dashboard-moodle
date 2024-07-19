from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import StudentSerializer, CourseSerializer, AttendanceSerializer
import os
import pandas as pd
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def load_data(source, data_type):
    file_path = settings.DATA_DIR / source / f'{data_type}.csv'
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    df = pd.read_csv(file_path)
    if data_type == 'students':
        df['lastaccess'] = pd.to_datetime(df['lastaccess'], unit='s').dt.tz_localize('UTC').dt.tz_convert('America/Bogota')
    if data_type == 'attendance':
        for col in df.columns:
            if col.startswith('attendance_'):
                df[col] = pd.to_datetime(df[col], unit='s').dt.tz_localize('UTC').dt.tz_convert('America/Bogota')
    return df


class StudentList(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        source = self.kwargs['source']
        students_df = load_data(source, 'students')
        return students_df.to_dict('records')


class StudentDetail(generics.RetrieveAPIView):
    serializer_class = StudentSerializer

    def get_object(self):
        source = self.kwargs['source']
        username = self.kwargs['username']
        students_df = load_data(source, 'students')
        student = get_object_or_404(students_df[students_df['username'] == username])
        return student


class CourseList(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        source = self.kwargs['source']
        courses_df = load_data(source, 'courses')
        return courses_df.to_dict('records')


class CourseDetail(generics.RetrieveAPIView):
    serializer_class = CourseSerializer

    def get_object(self):
        source = self.kwargs['source']
        param = self.kwargs['param']
        courses_df = load_data(source, 'courses')
        course = courses_df[(courses_df['id'] == int(param)) |
                            (courses_df['shortname'] == param) |
                            (courses_df['fullname'].str.contains(param, case=False, na=False))]
        return get_object_or_404(course.to_dict('records'))


class AttendanceList(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        source = self.kwargs['source']
        attendance_df = load_data(source, 'attendance')
        return attendance_df.to_dict('records')


class AttendanceDetail(generics.RetrieveAPIView):
    serializer_class = AttendanceSerializer

    def get_object(self):
        source = self.kwargs['source']
        param = self.kwargs['param']
        attendance_df = load_data(source, 'attendance')
        attendance = attendance_df[(attendance_df['course_id'] == int(param)) |
                                   (attendance_df['course_shortname'] == param) |
                                   (attendance_df['course_fullname'].str.contains(param, case=False, na=False)) |
                                   (attendance_df['username'] == param)]
        return get_object_or_404(attendance.to_dict('records'))
