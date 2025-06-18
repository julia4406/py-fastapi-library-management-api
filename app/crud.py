from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Author
from app.schemas import (
    AuthorDetailSchema,
    AuthorCreateSchema,
    AuthorUpdateSchema,
    AuthorCreateResponseSchema
)


async def create_author(
        session: AsyncSession,
        data: AuthorCreateSchema
) -> AuthorCreateResponseSchema:
    new_author = Author(**data.model_dump())
    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)
    return AuthorCreateResponseSchema.model_validate(new_author)


async def get_all_authors(session: AsyncSession) -> list[AuthorDetailSchema]:
    result = await session.execute(
        select(Author).options(selectinload(Author.books))
    )
    authors = result.scalars().all()
    return [AuthorDetailSchema.model_validate(author) for author in
            authors]


async def get_author(session: AsyncSession, author_id: int) -> AuthorDetailSchema:
    result = await session.execute(
        select(Author)
        .options(selectinload(Author.books))
        .where(Author.id == author_id)
    )
    author = result.scalars().first()
    if author:
        return AuthorDetailSchema.model_validate(author)
    else:
        raise HTTPException(status_code=404, detail="Author not found")


async def update_author(
        session: AsyncSession,
        author_id: int,
        data: AuthorUpdateSchema
) -> AuthorDetailSchema:
    result = await session.execute(
        select(Author)
        .options(selectinload(Author.books))
        .where(Author.id == author_id)
    )
    author = result.scalars().first()

    if author:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(author, key, value)

        await session.commit()
        await session.refresh(author)
        return AuthorDetailSchema.model_validate(author)
    else:
        raise HTTPException(status_code=404, detail="Author not found")


async def delete_author(
        session: AsyncSession,
        author_id: int
) -> None:
    result = await session.execute(
        select(Author).where(Author.id == author_id)
    )
    author = result.scalars().first()

    if author:
        await session.delete(author)
        await session.commit()
    else:
        raise HTTPException(status_code=404, detail="Author not found")
