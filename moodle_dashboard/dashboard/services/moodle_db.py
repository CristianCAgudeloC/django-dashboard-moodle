from django.db import connections
from django.db.utils import OperationalError

def get_students_from_db():
    connection = connections['moodle']
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, idnumber, firstname, lastname, email, lastaccess FROM mdl_user")
        columns = [col[0] for col in cursor.description]
        students = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except OperationalError as e:
        raise e
    finally:
        cursor.close()
    return students

def get_courses_from_db():
    connection = connections['moodle']
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT c.id, c.fullname, c.shortname, COUNT(ue.id) as student_count "
                       "FROM mdl_course c "
                       "JOIN mdl_enrol e ON e.courseid = c.id "
                       "JOIN mdl_user_enrolments ue ON ue.enrolid = e.id "
                       "GROUP BY c.id, c.fullname, c.shortname")
        columns = [col[0] for col in cursor.description]
        courses = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except OperationalError as e:
        raise e
    finally:
        cursor.close()
    return courses

def get_students_in_course(course_id):
    connection = connections['moodle']
    try:
        cursor = connection.cursor()
        query = """
            SELECT u.id, u.username, u.idnumber, u.firstname, u.lastname, u.email, u.lastaccess
            FROM mdl_user u
            JOIN mdl_user_enrolments ue ON ue.userid = u.id
            JOIN mdl_enrol e ON e.id = ue.enrolid
            WHERE e.courseid = %s
        """
        cursor.execute(query, [course_id])
        columns = [col[0] for col in cursor.description]
        students = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except OperationalError as e:
        raise e
    finally:
        cursor.close()
    return students

def get_attendance_for_course(course_id):
    connection = connections['moodle']
    try:
        cursor = connection.cursor()
        query = """
            SELECT al.studentid, al.sessionid, al.statusid, ses.sessdate, s.description
            FROM mdl_attendance_log al
            JOIN mdl_attendance_statuses s ON s.id = al.statusid
            JOIN mdl_attendance_sessions ses ON ses.id = al.sessionid
            JOIN mdl_attendance a ON a.id = ses.attendanceid
            WHERE a.course = %s
        """
        cursor.execute(query, [course_id])
        columns = [col[0] for col in cursor.description]
        attendance = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except OperationalError as e:
        raise e
    finally:
        cursor.close()
    return attendance

def get_attendance_sessions_for_course(course_id):
    connection = connections['moodle']
    try:
        cursor = connection.cursor()
        query = """
            SELECT ses.id, ses.sessdate
            FROM mdl_attendance_sessions ses
            JOIN mdl_attendance a ON a.id = ses.attendanceid
            WHERE a.course = %s
        """
        cursor.execute(query, [course_id])
        columns = [col[0] for col in cursor.description]
        sessions = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except OperationalError as e:
        raise e
    finally:
        cursor.close()
    return sessions
