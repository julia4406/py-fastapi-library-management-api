from http.client import HTTPResponse

from fastapi import FastAPI, APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app import crud
from app.database import get_async_session
from app.schemas import (
    AuthorCreateSchema,
    AuthorDetailSchema,
    AuthorUpdateSchema,
    AuthorCreateResponseSchema
)

app = FastAPI(
    title="Library management"
)
router = APIRouter()

@router.post("/authors", status_code=status.HTTP_201_CREATED)
async def create_author(
        data: AuthorCreateSchema,
        session: AsyncSession = Depends(get_async_session)
) -> AuthorCreateResponseSchema:
    """
        Creates author in library with incoming data
    """
    return await crud.create_author(session=session, data=data)


@router.get("/authors", response_model=list[AuthorDetailSchema])
async def get_all_authors(
        session: AsyncSession = Depends(get_async_session)
) -> list[AuthorDetailSchema]:
    """
        Returns list of all authors in library
    """
    return await crud.get_all_authors(session=session)


@router.get("/authors/{author_id}", response_model=AuthorDetailSchema)
async def get_author_by_id(
        author_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> AuthorDetailSchema:
    """
        Returns author in library with particular ID
    """
    return await crud.get_author(session=session, author_id=author_id)


@router.post("/authors/{author_id}", response_model=AuthorDetailSchema)
async def update_author(
        author_id: int,
        data: AuthorUpdateSchema,
        session: AsyncSession = Depends(get_async_session)
) -> AuthorDetailSchema:
    """
        Fully or partially updates author's fields in library
    """
    return await crud.update_author(
        session=session, author_id=author_id, data=data
    )


@router.delete(
    "/authors/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_author(
        author_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> None:
    """
        Fully or partially updates author's fields in library
    """
    await crud.delete_author(session=session, author_id=author_id)
app.include_router(router)
