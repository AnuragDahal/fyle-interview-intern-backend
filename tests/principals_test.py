from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_view_teachers(client, h_principal):
    # Arrange: Get the expected number of teachers
    expected_teacher_count = 3

    # Act: Send a GET request to the /principal/teachers endpoint
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    # Assert: Check that the response indicates success
    assert response.status_code == 200

    # Assert: Check that the number of teachers in the response matches the expected number
    data = response.json['data']
    assert len(data) == expected_teacher_count


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [
            AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 6,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


def test_grade_assignment_invalid_grade(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': 'F'
        },
        headers=h_principal
    )
    assert response.status_code == 422


def test_grade_assignment_invalid_assignment_id(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 100,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 404


def test_grade_assignment_no_grade(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
        },
        headers=h_principal
    )

    assert response.status_code == 422  # or 422, depending on your application
