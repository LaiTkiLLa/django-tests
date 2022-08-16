import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from django_testing import settings
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

# @pytest.fixture
# def test_settings():
#     settings.MAX_STUDENTS_PER_COURSE = True

@pytest.mark.django_db
def test_oneCourse(client, course_factory):


    course = course_factory(_quantity = 5)

    for i in course:

        response = client.get('/api/v1/courses/'+str(i.id)+'/')

        assert response.json()['id'] == int(i.id)


@pytest.mark.django_db
def test_listCourse(client, course_factory):

    course = course_factory(_quantity = 5)

    response = client.get('/api/v1/courses/')

    assert len(response.json()) == len(course)

@pytest.mark.django_db
def test_createCourse(client, course_factory):

    course = course_factory(_quantity=5)

    for i in course:

        base = Course.objects.count()

        response = client.post('/api/v1/courses/', data={'name': i.name})

        assert response.json()['name'] == i.name
        assert response.status_code == 201
        assert Course.objects.count() == base + 1

@pytest.mark.django_db
def test_patchCourse(client, course_factory):

    course = course_factory(_quantity=5)

    for i in course:

        response_post = client.post('/api/v1/courses/', data={'name': i.name})

        response_patch = client.patch('/api/v1/courses/'+str(i.id)+'/', data={'name': 'C2'})

        assert response_patch.status_code == 200
        assert response_patch.json()['name'] == 'C2'

@pytest.mark.django_db
def test_deleteCourse(client, course_factory):


    course = course_factory(_quantity=5)

    base = Course.objects.count()

    for i in course:

        response_post = client.post('/api/v1/courses/', data={'name': i.name})

        assert Course.objects.count() == base + 1

        response_delete = client.delete('/api/v1/courses/'+str(i.id)+'/')

        assert response_delete.status_code == 204
        assert Course.objects.count() == base

@pytest.mark.django_db
def test_filterIdCourse(client, course_factory):

    course = course_factory(_quantity = 6)

    for i in course:

        response = client.get('/api/v1/courses/?id='+str(i.id))

        assert response.status_code == 200

@pytest.mark.django_db
def test_filterNameCourse(client, course_factory):

    course = course_factory(_quantity = 6)

    for i in course:

        response = client.get('/api/v1/courses/?name='+str(i.name))

        assert response.status_code == 200


# def test_StudentsNumber(client, course_factory, student_factory, settings):
#
#     courses = course_factory(_quantity=20)
#
#     students = student_factory(_quantity = 25)
#
#     for course in courses:
#         course_name = course.name
#
#     for student in students:
#         student_id = student.id
#
#     response = client.post('/api/v1/courses/', data={'name': course_name, 'students':student_id})
#
#
#     if len(students) > 20:
#
#
#         # for request in response.json()['non_field_errors']:
#         for request in response.json():
#             print(request[id])
#
#             # assert request == 'Студентов слишком много'
#
#     else:
#
#         assert response.status_code == 201
# #
#




