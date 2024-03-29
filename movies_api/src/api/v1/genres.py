from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from movies_api.src.schemas import GenreSchema
from movies_api.src.services import GenresService, get_genres_service
from movies_api.src.services.auth import security_jwt

router = APIRouter()


@router.get('/',
            response_model=List[GenreSchema],
            summary='All genres',
            description='List of all genres',
            response_description='List of genres',
            dependencies=[Depends(security_jwt)])
async def list_of_genres(genre_service: GenresService = Depends(get_genres_service)):
    """
    Return a list of all genres.
    """
    genres, _ = await genre_service.get_many()
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not Found')

    return [GenreSchema(uuid=genre.uuid, name=genre.name) for genre in genres]


@router.get('/{genre_id}',
            response_model=GenreSchema,
            summary='Genre info',
            description='Search a genre by id',
            response_description='UUID and name',
            dependencies=[Depends(security_jwt)])
async def genre_details(genre_id: UUID4, genre_service: GenresService = Depends(get_genres_service)):
    """
    Return info about genre by uuid.
    """
    genre = await genre_service.get_by_id(str(genre_id))
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not Found')

    return GenreSchema.parse_obj(genre)
