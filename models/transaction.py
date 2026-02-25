from database import Database


class Transaction:
    def __init__(
        self,
        user_id,
        amount,
        category,
        transaction_type,
        description=None,
        transaction_id=None,
        created_at=None,
    ):
        self.id = transaction_id
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.type = transaction_type
        self.description = description
        self.created_at = created_at
        self.db = Database()

    # -----------------------------
    # Create Transaction
    # -----------------------------
    def save(self):
        query = """
        INSERT INTO transactions (user_id, amount, category, type, description)
        VALUES (?, ?, ?, ?, ?)
        """
        params = (self.user_id, self.amount, self.category, self.type, self.description)

        transaction_id = self.db.execute(query, params)
        self.id = transaction_id
        return transaction_id

    # -----------------------------
    # Delete Transaction
    # -----------------------------
    @classmethod
    def delete(cls, transaction_id, user_id):
        db = Database()
        db.execute(
            "DELETE FROM transactions WHERE id = ? AND user_id = ?",
            (transaction_id, user_id),
        )

    # ------------------------------
    # Update Transaction    

    @classmethod
    def update(cls, transaction_id, user_id, amount, category, transaction_type, description):
        db = Database()

        query = """
        UPDATE transactions
        SET amount = ?, category = ?, type = ?, description = ?
        WHERE id = ? AND user_id = ?
        """

        db.execute(
            query,
            (amount, category, transaction_type, description, transaction_id, user_id)
        )

    # -----------------------------
    # Fetch All Transactions for User
    # -----------------------------
    @classmethod
    def get_all_by_user(cls, user_id):
        db = Database()
        rows = db.fetch_all(
            "SELECT * FROM transactions WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )

        return [
            cls(
                user_id=row["user_id"],
                amount=row["amount"],
                category=row["category"],
                transaction_type=row["type"],
                description=row["description"],
                transaction_id=row["id"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    # -----------------------------
    # Filter by Category
    # -----------------------------
    @classmethod
    def get_by_category(cls, user_id, category):
        db = Database()
        rows = db.fetch_all(
            """
            SELECT * FROM transactions
            WHERE user_id = ? AND category = ?
            ORDER BY created_at DESC
            """,
            (user_id, category),
        )

        return [
            cls(
                user_id=row["user_id"],
                amount=row["amount"],
                category=row["category"],
                transaction_type=row["type"],
                description=row["description"],
                transaction_id=row["id"],
                created_at=row["created_at"],
            )
            for row in rows
        ]
    
    # -----------------------------
    # Filter by Month
    # -----------------------------

    @classmethod
    def get_by_month(cls, user_id, year, month):
        db = Database()
        month_string = f"{year}-{month:02d}"

        rows = db.fetch_all(
            """
            SELECT * FROM transactions
            WHERE user_id = ?
            AND strftime('%Y-%m', created_at) = ?
            ORDER BY created_at DESC
            """,
            (user_id, month_string),
        )

        return [
            cls(
                user_id=row["user_id"],
                amount=row["amount"],
                category=row["category"],
                transaction_type=row["type"],
                description=row["description"],
                transaction_id=row["id"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    # -----------------------------
    # String Representation
    # -----------------------------
    def __str__(self):
        return (
            f"[{self.created_at}] "
            f"{self.type.upper()} | "
            f"{self.category} | "
            f"{self.amount} | "
            f"{self.description or ''}"
        )
