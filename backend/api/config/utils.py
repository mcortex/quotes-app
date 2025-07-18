from sqlmodel import Session

from api.models.quote import Character, Quote


def create_character_with_quotes(session: Session, character_name: str, quotes_list: list[str]):
    """Create a character with associated quotes.
    Args:
        session (Session): Database session dependency.
        character_name (str): The name of the character.
        quotes_list (list[str]): A list of quotes associated with the character.
    Returns:
        Character: The created character with associated quotes.
    """
    character = Character(name=character_name)
    session.add(character)
    session.commit()
    session.refresh(character)
    
    for quote_text in quotes_list:
        quote = Quote(quote=quote_text, character_id=character.id)
        session.add(quote)
    
    session.commit()
    return character