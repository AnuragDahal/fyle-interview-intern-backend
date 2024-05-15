
def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1, json={
            "id": 6,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_for_empty_assignment(client, h_teacher_3):

    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_3
    )

    data = response.json
    assert response.status_code == 200
    assert data['data'] == []


def test_grade_assignment_success(client, h_teacher_2, reset_assignment_state_2):

    # set the state of the assignment to submitted
    reset_assignment_state_2(3, 'SUBMITTED')

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 3,
            "grade": "C"
        }
    )

    assert response.status_code == 200
    data = response.json

    assert data['data']['state'] == 'GRADED'
    assert data['data']['grade'] == 'C'


def test_invalid_route(client, h_teacher_1):
    # Act: Send a GET request to an invalid route
    response = client.get(
        '/invalid/route',
        headers=h_teacher_1
    )

    # Assert: Check that the response indicates not found
    assert response.status_code == 404


def test_invalid_headers(client):
    # Arrange: Set invalid headers
    invalid_headers = {'Authorization': 'InvalidToken'}

    # Act: Send a POST request to the /principal/assignments/grade endpoint with invalid headers
    response = client.post(
        '/teacher/assignments/grade',
        headers=invalid_headers
    )

    # Assert: Check that the response indicates unauthorized
    assert response.status_code == 401
