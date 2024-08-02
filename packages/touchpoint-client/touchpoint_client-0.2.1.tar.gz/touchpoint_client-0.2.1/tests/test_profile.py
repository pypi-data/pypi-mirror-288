def test_profile(default_client):
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
