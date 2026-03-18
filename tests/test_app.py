def test_root_redirects_to_static_index(fastapi_client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = fastapi_client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_all_activities(fastapi_client):
    # Arrange
    response_before = fastapi_client.get("/activities")
    assert response_before.status_code == 200
    activities_snapshot = response_before.json()

    # Act
    response = fastapi_client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == activities_snapshot


def test_signup_for_activity_succeeds_and_updates_participants(fastapi_client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"

    # Act
    response = fastapi_client.post(
        f"/activities/{activity_name}/signup", params={"email": new_email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}

    # Ensure state was updated
    activities_after = fastapi_client.get("/activities").json()
    assert new_email in activities_after[activity_name]["participants"]


def test_signup_for_activity_already_signed_up_returns_400(fastapi_client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = fastapi_client.post(
        f"/activities/{activity_name}/signup", params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_not_found_returns_404(fastapi_client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "anyone@mergington.edu"

    # Act
    response = fastapi_client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_succeeds_and_updates_participants(fastapi_client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    # Act
    response = fastapi_client.delete(
        f"/activities/{activity_name}/participants", params={"email": participant_email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {participant_email} from {activity_name}"}

    activities_after = fastapi_client.get("/activities").json()
    assert participant_email not in activities_after[activity_name]["participants"]


def test_unregister_from_activity_not_signed_up_returns_400(fastapi_client):
    # Arrange
    activity_name = "Chess Club"
    not_signed_email = "not-in-list@mergington.edu"

    # Act
    response = fastapi_client.delete(
        f"/activities/{activity_name}/participants", params={"email": not_signed_email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_from_activity_not_found_returns_404(fastapi_client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "anyone@mergington.edu"

    # Act
    response = fastapi_client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
