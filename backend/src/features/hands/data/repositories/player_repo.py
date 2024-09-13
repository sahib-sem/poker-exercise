import psycopg2 
from src.features.hands.domain.entities.player import Player

class PlayerRepository:

    def __init__(self, db_conn: psycopg2.extensions.connection):
        self.db_conn = db_conn
    
    def create_player(self, player: Player) -> Player:

        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO players (hand_id, player_idx, stack_size, winnings, hole_cards)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """, (player.hand_id, player.player_idx, player.initial_stack_size,player.winnings,  player.hole_cards))
            self.db_conn.commit()
            player.id = cursor.fetchone()[0] 
        return player

    def get_players_by_hand_id(self, hand_id: str) -> list[Player]:

        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, hand_id, player_idx, stack_size, winnings, hole_cards
                FROM players
                WHERE hand_id = %s;
            """, (hand_id,))
            rows = cursor.fetchall()

        players = [Player( 
            hand_id=row[1], 
            player_idx=row[2], 
            initial_stack_size=row[3], 
            winnings=row[4], 
            hole_cards=row[5]) 
            for row in rows]
        
        return players

    def update_player(self, player: Player) -> Player:
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                UPDATE players
                SET stack_size = %s, winnings = %s
                WHERE id = %s;
            """, (player.initial_stack_size, player.winnings, player.id))
        return player