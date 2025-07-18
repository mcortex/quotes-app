from typing import Annotated
from fastapi import APIRouter, Depends, Query, HTTPException, Response
from sqlmodel import Session, select
from api.models.quote import Quote, Character
from api.config.db import engine
from api.config.utils import create_character_with_quotes

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.get("/quotes", response_model=list[Quote], tags=["quotes"])
def read_quotes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ):
    """Retrieve a list of quotes with pagination.
    Args:
        session (Session): Database session dependency.
        offset (int): The number of records to skip.
        limit (int): The maximum number of records to return.
    Returns:
        list[Quote]: A list of quotes.
    """
    quotes = session.exec(select(Quote).offset(offset).limit(limit)).all()
    return quotes

@router.get("/quotes/all", tags=["quotes"])
def read_quotes_full(
    session: SessionDep
    # offset: int = 0,
    # limit: Annotated[int, Query(le=100)] = 100
    ) -> list[dict]:
    """Retrieve a list of quotes with pagination.
    Args:
        session (Session): Database session dependency.
    Returns:
        list[Quote]: A list of quotes.
    """
    quotes = session.exec(select(Quote, Character).where(Quote.character_id == Character.id)).all()
    quotes_full = []
    for quote, character in quotes:
        quote_full = {
            "id": quote.id,
            "quote": quote.quote,
            "character": character.name if character else None
        }
        quotes_full.append(quote_full)
    return quotes_full

# @router.get("/quotes/{quote_id}", response_model=Quote, tags=["quotes"])
# def read_quote(quote_id: int, session: SessionDep):
#     """Retrieve a single quote by its ID.
#     Args:
#         quote_id (int): The ID of the quote to retrieve.
#         session (Session): Database session dependency.
#     Returns:
#         Quote: The requested quote.
#     """
#     quote = session.get(Quote, quote_id)
#     if not quote:
#         raise HTTPException(status_code=404, detail="Quote not found")
#     return quote

@router.get("/quotes/{quote_id}", tags=["quotes"])
def read_quote(quote_id: int, session: SessionDep) -> dict:
    """Retrieve a single quote by its ID.
    Args:
        quote_id (int): The ID of the quote to retrieve.
        session (Session): Database session dependency.
    Returns:
        Quote: The requested quote.
    """
    quote = session.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    character = session.get(Character, quote.character_id) if quote else None
    if character:
        quote_full = {"id": quote.id, "quote": quote.quote, "character": character.name}
    else:
        quote_full = {"id": quote.id, "quote": quote.quote, "character": None}
    return quote_full

@router.post("/quotes", response_model=Quote, tags=["quotes"])
def create_quote(quote: Quote, session: SessionDep):
    """Create a new quote.
    Args:
        quote (Quote): The quote to create.
        session (Session): Database session dependency.
    Returns:
        Quote: The created quote.
    """
    session.add(quote)
    session.commit()
    session.refresh(quote)
    return quote

@router.delete("/quotes/{quote_id}", status_code=204, tags=["quotes"])
def delete_quote(quote_id: int, session: SessionDep):
    """Delete a quote by its ID.
    Args:
        quote_id (int): The ID of the quote to delete.
        session (Session): Database session dependency.
    """
    quote = session.get(Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    session.delete(quote)
    session.commit()
    return Response(status_code=204)

@router.get("/characters", response_model=list[Character], tags=["characters"])
def read_characters(session: SessionDep):
    """Retrieve a list of characters.
    Args:
        session (Session): Database session dependency.
    Returns:
        list[Character]: A list of characters.
    """
    characters = session.exec(select(Character)).all()
    return characters

@router.get("/characters/{character_id}", response_model=Character, tags=["characters"])
def read_character(character_id: int, session: SessionDep):
    """Retrieve a single character by its ID.
    Args:
        character_id (int): The ID of the character to retrieve.
        session (Session): Database session dependency.
    Returns:
        Character: The requested character.
    """
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@router.post("/characters", response_model=Character, tags=["characters"])
def create_character(character: Character, session: SessionDep):
    """Create a new character.
    Args:
        character (Character): The character to create.
        session (Session): Database session dependency.
    Returns:
        Character: The created character.
    """
    session.add(character)
    session.commit()
    session.refresh(character)
    return character

@router.delete("/characters/{character_id}", status_code=204, tags=["characters"])
def delete_character(character_id: int, session: SessionDep):
    """Delete a character by its ID.
    Args:
        character_id (int): The ID of the character to delete.
        session (Session): Database session dependency.
    """
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    session.delete(character)
    session.commit()
    return Response(status_code=204)

@router.get("/characters/{character_id}/quotes", response_model=list[Quote])
def get_quotes_by_character(character_id: int, session: Session = Depends(get_session)):
    """Get all quotes for a specific character.
    Args:
        character_id (int): The ID of the character.
        session (Session): Database session dependency.
    Returns:
        list[Quote]: A list of quotes associated with the character.
    """
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    quotes = session.exec(select(Quote).where(Quote.character_id == character_id)).all()
    return quotes

@router.post("/quotes/character", response_model=Character, tags=["quotes","characters"])
def create_character_with_quotes_endpoint(character_data: dict,session: SessionDep):
    """Create a character with associated quotes.
    Args:
        session (Session): Database session dependency.
        character_data (dict): A dictionary containing character data.
            Expected keys:
            - "name": The name of the character.
            - "quote": A list of quotes associated with the character.
    Example:
        {
            "name": "Yoda",
            "quote": [
                "Do or do not, there is no try.", 
                "Fear leads to suffering."
            ]
        }    
    Returns:
        Character: The created character with associated quotes.
    """
    return create_character_with_quotes(session, character_data["name"], character_data["quote"])

@router.get("/health")
def health_check():
    """Enpoint to check the health of the API."""
    return {"status": "healthy", "message": "API is running"}