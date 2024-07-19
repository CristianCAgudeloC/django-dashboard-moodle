import requests

MOODLE_API_URL = 'https://tu-moodle.com/webservice/rest/server.php'


def get_students_from_api(token):
    params = {
        'wstoken': token,
        'wsfunction': 'core_user_get_users',
        'moodlewsrestformat': 'json',
        'criteria[0][key]': 'username',
        'criteria[0][value]': '%'
    }
    response = requests.get(MOODLE_API_URL, params=params)
    return response.json()


def get_courses_from_api(token):
    params = {
        'wstoken': token,
        'wsfunction': 'core_course_get_courses',
        'moodlewsrestformat': 'json'
    }
    response = requests.get(MOODLE_API_URL, params=params)
    return response.json()


def get_attendance_from_api(token, course_id):
    params = {
        'wstoken': token,
        'wsfunction': 'mod_attendance_get_attendance_log',
        'moodlewsrestformat': 'json',
        'courseid': course_id
    }
    response = requests.get(MOODLE_API_URL, params=params)
    return response.json()
