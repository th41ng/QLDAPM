from ..models import User


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_by_email(email):
    query = User.query.filter_by(email=(email or "").strip().lower())
    return query.first()
