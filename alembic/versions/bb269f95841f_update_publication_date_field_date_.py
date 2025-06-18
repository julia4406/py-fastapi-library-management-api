"""Update publication_date field: date instead datetime

Revision ID: bb269f95841f
Revises: 0ddf206ee366
Create Date: 2025-06-18 11:45:39.436480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb269f95841f'
down_revision: Union[str, Sequence[str], None] = '0ddf206ee366'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # створюємо нову тимчасову таблицю з потрібною схемою (publication_date як Date)
    op.execute("""
        CREATE TABLE books_new (
            id INTEGER PRIMARY KEY,
            title VARCHAR NOT NULL,
            summary VARCHAR,
            publication_date DATE NOT NULL,
            author_id INTEGER,
            FOREIGN KEY(author_id) REFERENCES authors(id)
        )
    """)

    # копіюємо дані зі старої таблиці в нову
    op.execute("""
        INSERT INTO books_new (id, title, summary, publication_date, author_id)
        SELECT id, title, summary, publication_date, author_id FROM books
    """)

    # видаляємо стару таблицю
    op.execute("DROP TABLE books")

    # перейменовуємо нову таблицю у стару назву
    op.execute("ALTER TABLE books_new RENAME TO books")


def downgrade() -> None:
    """Downgrade schema."""
    # повертаємо назад зміни (publication_date як DATETIME)
    op.execute("""
        CREATE TABLE books_old (
            id INTEGER PRIMARY KEY,
            title VARCHAR NOT NULL,
            summary VARCHAR,
            publication_date DATETIME NOT NULL,
            author_id INTEGER,
            FOREIGN KEY(author_id) REFERENCES authors(id)
        )
    """)
    op.execute("""
        INSERT INTO books_old (id, title, summary, publication_date, author_id)
        SELECT id, title, summary, publication_date, author_id FROM books
    """)
    op.execute("DROP TABLE books")
    op.execute("ALTER TABLE books_old RENAME TO books")
