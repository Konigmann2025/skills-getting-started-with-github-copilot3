from urllib.parse import quote

from src.app import activities as activities_store


def test_get_activities(app_client):
    response = app_client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity(app_client):
    activity = "Chess Club"
    email = "test@student.edu"
    url = f"/activities/{quote(activity)}/signup?email={quote(email)}"

    response = app_client.post(url)

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in activities_store[activity]["participants"]


def test_signup_duplicate_rejected(app_client):
    activity = "Chess Club"
    email = activities_store[activity]["participants"][0]
    url = f"/activities/{quote(activity)}/signup?email={quote(email)}"

    response = app_client.post(url)

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_participant(app_client):
    activity = "Chess Club"
    email = activities_store[activity]["participants"][0]
    url = f"/activities/{quote(activity)}/participants?email={quote(email)}"

    response = app_client.delete(url)

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in activities_store[activity]["participants"]


def test_unregister_missing_participant(app_client):
    activity = "Chess Club"
    email = "missing@student.edu"
    url = f"/activities/{quote(activity)}/participants?email={quote(email)}"

    response = app_client.delete(url)

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
