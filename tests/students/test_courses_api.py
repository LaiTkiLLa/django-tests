import pytest
from rest_framework.test import APIClient
from model_bakery import baker

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

###проверка получения 1го курса
@pytest.mark.django_db
def test_oneCourse(client, course_factory):

    course = course_factory(_quantity = 5)

    response = client.get('/api/v1/courses/4/')

    assert response.json()['id'] == 4


#### проверка получения списка курсов
@pytest.mark.django_db
def test_listCourse(client, course_factory):

    course = course_factory(_quantity = 5)

    response = client.get('/api/v1/courses/')

    assert len(response.json()) == 5

###тест успешного создания курса
@pytest.mark.django_db
def test_createCourse(client):

    base = Course.objects.count()

    response = client.post('/api/v1/courses/', data={'name': 'C1', 'students': []})

    assert response.status_code == 201
    assert Course.objects.count() == base + 1

###тест успешного обновления курса
@pytest.mark.django_db
def test_patchCourse(client):

    response_post = client.post('/api/v1/courses/', data={'name': 'C1', 'students': []})
    response_get = client.get('/api/v1/courses/')

    response_patch = client.patch('/api/v1/courses/12/', data={'name': 'C2'})

    assert response_patch.status_code == 200

###тест успешного удаления курса
@pytest.mark.django_db
def test_deleteCourse(client):

    base = Course.objects.count()

    response_post = client.post('/api/v1/courses/', data={'name': 'C1', 'students': []})

    assert Course.objects.count() == base + 1

    response_delete = client.delete('/api/v1/courses/13/')

    assert response_delete.status_code == 204
    assert Course.objects.count() == base

###проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filterIdCourse(client, course_factory):

    course = course_factory(_quantity = 6)

    response = client.get('/api/v1/courses/?id=16')

    assert response.status_code == 200

###проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filterNameCourse(client, course_factory):

    course = course_factory(_quantity = 6)

    response = client.get('/api/v1/courses/?name=C2')

    assert response.status_code == 200

###Ограничить число студентов на курсе
@pytest.mark.django_db
def test_StudentsNumber(client, course_factory):

    course = course_factory(_quantity=20)

    # student = student_factory(_quantity = 25)

    response = client.post('/api/v1/courses/', data={'name': course})

    if len(course) > 20:

        for request in response.json()['non_field_errors']:

            assert request == 'Курсов слишком много'

    else:

        assert response.status_code == 201





