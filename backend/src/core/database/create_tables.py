from src.core.database.connection import get_db_connection


def create_tables():
    """Creates all the tables and relationships if they do not exist."""

    create_extension_uuid = """
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """

    create_hand_table = """
    CREATE TABLE IF NOT EXISTS hands (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        has_ended BOOLEAN NOT NULL,
        number_of_players INT NOT NULL,
        small_blind_idx INT NOT NULL,
        big_blind_idx INT NOT NULL,
        dealer_idx INT NOT NULL,
        stack_size INT NOT NULL,
        big_blind_size INT NOT NULL
    );
    """

    create_player_table = """
    CREATE TABLE IF NOT EXISTS players (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        hand_id UUID NOT NULL,
        player_idx INT NOT NULL,
        stack_size INT NOT NULL,
        hole_cards TEXT NOT NULL,
        winnings INT DEFAULT 0,
        FOREIGN KEY (hand_id) REFERENCES hands (id) ON DELETE CASCADE
    );
    """

    create_action_table = """
    CREATE TABLE IF NOT EXISTS actions (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        hand_id UUID NOT NULL,
        action_type VARCHAR(50) NOT NULL,
        amount INT DEFAULT 0,
        raise_amount INT DEFAULT 0,
        card_string TEXT DEFAULT '',
        FOREIGN KEY (hand_id) REFERENCES hands (id) ON DELETE CASCADE
    );
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(create_extension_uuid)
            cursor.execute(create_hand_table)
            cursor.execute(create_player_table)
            cursor.execute(create_action_table)

        conn.commit()

        print("Tables created successfully.")
