from src import app as app_module


def test_signup_success_adds_participant(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_activity_not_found_returns_404(client):
    response = client.post("/activities/Nonexistent Activity/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_returns_400(client):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_signup_full_activity_returns_400(client):
    app_module.activities["Full Activity"] = {
        "description": "Activity with no available spots",
        "schedule": "Mondays, 4:00 PM - 5:00 PM",
        "max_participants": 1,
        "participants": ["full@mergington.edu"],
    }

    response = client.post(
        "/activities/Full Activity/signup",
        params={"email": "another@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Activity is full"}
