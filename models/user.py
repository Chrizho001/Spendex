import hashlib
import secrets
from database import Database


class User:
    def __init__(self, username, password_hash=None, user_id=None, created_at=None):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at
        self.db = Database()

    # -----------------------------
    # Password Utilities
    # -----------------------------
    @staticmethod
    def _hash_password(password, salt=None):
        if salt is None:
            salt = secrets.token_hex(16)

        hash_obj = hashlib.sha256()
        hash_obj.update((salt + password).encode("utf-8"))
        hashed = hash_obj.hexdigest()

        return f"{salt}${hashed}"

    @staticmethod
    def _verify_password(stored_password, provided_password):
        salt, hashed = stored_password.split("$")
        verify_hash = hashlib.sha256(
            (salt + provided_password).encode("utf-8")
        ).hexdigest()
        return verify_hash == hashed

    # -----------------------------
    # Database Operations
    # -----------------------------
    def save(self, password):
        hashed_password = self._hash_password(password)

        try:
            user_id = self.db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (self.username, hashed_password),
            )
            self.id = user_id
            self.password_hash = hashed_password
            return True
        except Exception:
            return False

    @classmethod
    def get_by_username(cls, username):
        db = Database()
        row = db.fetch_one("SELECT * FROM users WHERE username = ?", (username,))

        if row:
            return cls(
                username=row["username"],
                password_hash=row["password_hash"],
                user_id=row["id"],
                created_at=row["created_at"],
            )
        return None

    @classmethod
    def authenticate(cls, username, password):
        user = cls.get_by_username(username)

        if user and cls._verify_password(user.password_hash, password):
            return user
        return None
