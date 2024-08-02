projects = [("705981142221725696",), ("705981455884361728",)]


def test_projects(default_client):
    projects = default_client.projects()
    assert isinstance(projects, list)
    assert projects
    keys = ["id", "account_id", "name", "type", "project_settings"]
    for k in keys:
        for project in projects:
            assert k in project, f"{k} not in project"


# @pytest.mark.parametrize("project", )
def test_project(default_client):
    profile = default_client.profile.profile()
    keys = [
        "id",
        "account_id",
        "username",
        "global_role",
        "created_on",
        "active",
        "is_confirmed",
        "two_factor",
        "modified_on",
        "personal_settings",
        "projects",
        "group_projects",
    ]
    for k in keys:
        assert k in profile, f"{k} not in profile"


def test_account(default_client):
    account = default_client.profile.account()
    keys = [
        "id",
        "account_settings",
        "global_account",
        "created_on",
        "modified_on",
        "active",
        "name",
        "type",
        "limits",
    ]
    for k in keys:
        assert k in account, f"{k} not in account"
