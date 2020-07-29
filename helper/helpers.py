def user_helper(user):
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.fullname,
        "user_email": user.email,
    }


def check_duplicate(parent, username) -> bool:
    for uid in parent.keys():
        _user = user_helper(parent[uid])
        if _user["username"] == username:
            raise Exception("Username exists, do use another one.")
    return False
