from sqlmodel import Session, select

from api.config.db import engine
from api.models.quote import Character
from api.config.utils import create_character_with_quotes


def seed_database():
    """Seed the database with initial data."""
    with Session(engine) as session:
        # Verify if the database is already seeded
        existing_characters = session.exec(select(Character)).first()
        if existing_characters:
            print("Database already seeded")
            return
        
        # Datos iniciales
        characters_data = [
            ("Yoda", ["Do or do not, there is no try.", "Fear leads to suffering.","Luminous beings are we, not this crude matter."]),
            ("Darth Vader", ["I find your lack of faith disturbing.", "The Force is strong with this one."]),
            ("Luke Skywalker", ["May the Force be with you.", "I am a Jedi, like my father before me."]),
            ("Qui-Gon Jinn", ["Your focus determines your reality.", "The ability to speak does not make you intelligent."]),
            ("Obi-Wan Kenobi", ["Hello there!", "The Force will be with you, always."]),
            ("Anakin Skywalker", ["I have the high ground!", "This is where the fun begins."]),
            ("Padmé Amidala", ["So this is how liberty dies, with thunderous applause.", "I will not let you give up on yourself."]),
            ("Han Solo", ["Never tell me the odds!", "I’ve got a bad feeling about this."]),
            ("Leia Organa", ["Help me, Obi-Wan Kenobi. You're my only hope.", "I am not a committee."]),
            ("C-3PO", ["We seem to be made to suffer. It's our lot in life.", "Oh my, how rude!"]),
            ("R2-D2", ["Beep boop beep!", "Whistle beep!"]),
            ("Chewbacca", ["Rrrrghhh!", "Aaaaarrrghhh!"])
        ]
        
        for char_name, quotes in characters_data:
            create_character_with_quotes(session, char_name, quotes)
        
        print("Database seeded successfully")

if __name__ == "__main__":
    seed_database()