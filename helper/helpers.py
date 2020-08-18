def user_helper(user) -> dict:
    return {
        "id": str(user['_id']),
        "username": user['username'],
        "full_name": user['fullname'],
        "user_email": user['email'],
    }

def book_helper(book) -> dict:
    return {
        "id": str(book['_id']),
        "name": book['name'],
        "author": book['author'],
        "availability": book['availability'],
        "label": book['label'],
        "likes": book['likes'],
        "reads": book['reads'],
        "year": book['year'],
        "rating": book['rating'],
        "genre": book['genre'],
        "book_cover": book['book_cover']
    }