from django.urls import path
from .views import StudentList, StudentDetail, CourseList, CourseDetail, AttendanceList, AttendanceDetail

urlpatterns = [
    path('students/<str:source>/', StudentList.as_view(), name='student-list'),
    path('students/<str:source>/<str:username>/', StudentDetail.as_view(), name='student-detail'),
    path('courses/<str:source>/', CourseList.as_view(), name='course-list'),
    path('courses/<str:source>/<str:param>/', CourseDetail.as_view(), name='course-detail'),
    path('attendance/<str:source>/', AttendanceList.as_view(), name='attendance-list'),
    path('attendance/<str:source>/<str:param>/', AttendanceDetail.as_view(), name='attendance-detail'),
]
