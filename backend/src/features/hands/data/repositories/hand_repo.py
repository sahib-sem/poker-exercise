import psycopg2
from typing import List, Optional
from src.features.hands.data.repositories.action_repo import ActionRepository
from src.features.hands.data.repositories.player_repo import PlayerRepository
from src.features.hands.domain.entities.hand import Hand

class HandRepository:
    def __init__(self, db_conn: psycopg2.extensions.connection, action_repo: ActionRepository, player_repo: PlayerRepository):
        self.db_conn = db_conn
        self.action_repo = action_repo
        self.player_repo = player_repo

    def get_hand_by_id(self, hand_id: str) -> Hand | None:
        """Fetch a hand by its ID along with its actions and its players"""
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, has_ended, number_of_players, small_blind_idx, big_blind_idx, dealer_idx, 
                       stack_size, big_blind_size
                FROM hands 
                WHERE id = %s;
            """, (hand_id,))
            row = cursor.fetchone()

        if row:
            hand = Hand(
                id=row[0], 
                has_ended=row[1], 
                number_of_players=row[2], 
                small_blind_idx=row[3], 
                big_blind_idx=row[4], 
                dealer_idx=row[5],
                stack_size=row[6], 
                big_blind_size=row[7]
            )

            hand.actions = self.action_repo.get_actions_by_hand_id(hand.id)
            hand.players = self.player_repo.get_players_by_hand_id(hand.id)
            
            return hand
        return None

    def create_hand(self, hand: Hand) -> Hand:
        """Create a new hand"""
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO hands (has_ended, number_of_players, small_blind_idx, big_blind_idx, 
                                   dealer_idx, stack_size, big_blind_size)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """, (hand.has_ended, hand.number_of_players, hand.small_blind_idx, hand.big_blind_idx,
                  hand.dealer_idx, hand.stack_size, hand.big_blind_size))
            self.db_conn.commit()
            hand.id = cursor.fetchone()[0]
        return hand

    def update_hand(self, hand: Hand) -> Hand:
        """Update a hand in the database"""
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                UPDATE hands
                SET has_ended = %s, number_of_players = %s, small_blind_idx = %s, big_blind_idx = %s,
                    dealer_idx = %s, stack_size = %s, big_blind_size = %s
                WHERE id = %s;
            """, (hand.has_ended, hand.number_of_players, hand.small_blind_idx, hand.big_blind_idx, 
                  hand.dealer_idx, hand.stack_size, hand.big_blind_size, hand.id))
            self.db_conn.commit()
        return hand

    def get_hands_by_status(self, status: bool) -> List[Hand]:
        """Get all hands by status (True if ended, False otherwise)"""
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, has_ended, number_of_players, small_blind_idx, big_blind_idx, dealer_idx, 
                       stack_size, big_blind_size
                FROM hands 
                WHERE has_ended = %s;
            """, (status,))
            rows = cursor.fetchall()

        hands = []
        for row in rows:
            hand = Hand(
                id=row[0], 
                has_ended=row[1], 
                number_of_players=row[2], 
                small_blind_idx=row[3], 
                big_blind_idx=row[4], 
                dealer_idx=row[5], 
                stack_size=row[6], 
                big_blind_size=row[7], 
            )
            
            hand.actions = self.action_repo.get_actions_by_hand_id(hand.id)
            hand.players = self.player_repo.get_players_by_hand_id(hand.id)
            hands.append(hand)

        return hands

    
