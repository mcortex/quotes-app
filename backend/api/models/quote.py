from sqlmodel import Field, Relationship, SQLModel

class Character(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    
    quotes: list["Quote"] =  Relationship(back_populates="character", cascade_delete=True)

class Quote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    quote: str = Field(max_length=255)
    character_id: int | None = Field(default=None, foreign_key="character.id", ondelete="CASCADE")
    
    character: Character | None = Relationship(back_populates="quotes")