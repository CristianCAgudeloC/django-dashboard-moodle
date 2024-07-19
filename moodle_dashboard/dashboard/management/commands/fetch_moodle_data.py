import os
import pandas as pd
from django.core.management.base import BaseCommand
from dashboard.services.moodle_db import get_students_from_db, get_courses_from_db, get_students_in_course, get_attendance_for_course, get_attendance_sessions_for_course

class Command(BaseCommand):
    help = 'Fetch data from Moodle API or DB and store it in CSV/Excel files'

    def add_arguments(self, parser):
        parser.add_argument('--source', type=str, help='Source of data: api or db')

    def handle(self, *args, **kwargs):
        source = kwargs['source']

        if source == 'db':
            students = get_students_from_db()
            courses = get_courses_from_db()
            self.store_data(courses, 'courses', source)
            for course in courses:
                course_id = course['id']
                course_students = get_students_in_course(course_id)
                attendance = get_attendance_for_course(course_id)
                sessions = get_attendance_sessions_for_course(course_id)
                self.store_attendance_data(course, course_students, attendance, sessions, source)
        else:
            self.stdout.write(self.style.ERROR('Invalid source. Choose "db".'))
            return

    def store_data(self, data, data_type, source):
        os.makedirs(f'data/{source}', exist_ok=True)
        df = pd.DataFrame(data)
        csv_path = f'data/{source}/{data_type}.csv'
        excel_path = f'data/{source}/{data_type}.xlsx'
        df.to_csv(csv_path, index=False)
        df.to_excel(excel_path, index=False)
        self.stdout.write(self.style.SUCCESS(f'Successfully stored {data_type} data to {csv_path} and {excel_path}'))

    def store_attendance_data(self, course, students, attendance, sessions, source):
        os.makedirs(f'data/{source}', exist_ok=True)

        session_dict = {session['id']: session['sessdate'] for session in sessions}

        attendance_matrix = []
        for student in students:
            student_attendance = {
                'course_id': course['id'],
                'course_fullname': course['fullname'],
                'course_shortname': course['shortname'],
                'student_id': student['id'],
                'username': student['username'],
                'idnumber': student['idnumber'],
                'firstname': student['firstname'],
                'lastname': student['lastname'],
                'email': student['email'],
                'lastaccess': student['lastaccess']
            }
            for session_id, sessdate in session_dict.items():
                record = next(
                    (att for att in attendance if att['studentid'] == student['id'] and att['sessionid'] == session_id),
                    None)
                student_attendance[f'attendance_{sessdate}'] = record['description'] if record else 'Absent'
            attendance_matrix.append(student_attendance)

        df = pd.DataFrame(attendance_matrix)
        csv_path = f'data/{source}/attendance.csv'
        excel_path = f'data/{source}/attendance.xlsx'
        if os.path.exists(csv_path):
            df.to_csv(csv_path, mode='a', header=False, index=False)
            with pd.ExcelWriter(excel_path, mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, index=False, header=False)
        else:
            df.to_csv(csv_path, index=False)
            df.to_excel(excel_path, index=False)
        self.stdout.write(self.style.SUCCESS(
            f'Successfully stored attendance data for course {course["id"]} to {csv_path} and {excel_path}'))
