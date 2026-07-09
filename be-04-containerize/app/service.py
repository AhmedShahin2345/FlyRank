from app.repository import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def list_users(self):
        return self.repo.get_all()

    def create_user(self, name: str, email: str):
        return self.repo.add(name, email)
