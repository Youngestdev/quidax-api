def user_helper(user):
    return {
        "username": user['username'],
        "full_name": user['fullname'],
        "user_email": user['email'],
    }


def check_duplicate(parent, username) -> bool:
    for uid in parent:
        _user = user_helper(uid)
        if _user["username"] == username:
            raise Exception("Username exists, do use another one.")
    return False
