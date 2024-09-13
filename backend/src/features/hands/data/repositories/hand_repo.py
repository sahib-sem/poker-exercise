import psycopg2
from typing import List, Optional
from src.features.hands.domain.entities.hand import Hand
from src.features.hands.domain.entities.action import Action

class HandRepository:
    def __init__(self, db_conn: psycopg2.extensions.connection):
        self.db_conn = db_conn

    def get_hand_by_id(self, hand_id: str) -> Optional[Hand]:
        """Fetch a hand by its ID along with its actions"""
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, has_ended, number_of_players, small_blind_idx, big_blind_idx, dealer_idx, 
                       stack_size, big_blind_size, hole_cards, players_stack
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
                big_blind_size=row[7], 
                hole_cards=row[8], 
                players_stack=row[9]
            )

            # Fetch actions related to this hand
            hand.actions = self._get_actions_by_hand_id(hand_id)
            
            return hand
        return None

    def create_hand(self, hand: Hand) -> Hand:
        """Create a new hand"""
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO hands (has_ended, number_of_players, small_blind_idx, big_blind_idx, 
                                   dealer_idx, stack_size, big_blind_size, hole_cards, players_stack)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """, (hand.has_ended, hand.number_of_players, hand.small_blind_idx, hand.big_blind_idx,
                  hand.dealer_idx, hand.stack_size, hand.big_blind_size, hand.hole_cards, hand.players_stack))
            self.db_conn.commit()
            hand.id = cursor.fetchone()[0]  # Get the generated id from the database
        return hand

    def update_hand(self, hand: Hand) -> Hand:
        """Update a hand in the database"""
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                UPDATE hands
                SET has_ended = %s, number_of_players = %s, small_blind_idx = %s, big_blind_idx = %s,
                    dealer_idx = %s, stack_size = %s, big_blind_size = %s, hole_cards = %s, players_stack = %s
                WHERE id = %s;
            """, (hand.has_ended, hand.number_of_players, hand.small_blind_idx, hand.big_blind_idx, 
                  hand.dealer_idx, hand.stack_size, hand.big_blind_size, hand.hole_cards, hand.players_stack, hand.id))
            self.db_conn.commit()
        return hand

    def get_hands_by_status(self, status: bool) -> List[Hand]:
        """Get all hands by status (True if ended, False otherwise)"""
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, has_ended, number_of_players, small_blind_idx, big_blind_idx, dealer_idx, 
                       stack_size, big_blind_size, hole_cards, players_stack
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
                hole_cards=row[8], 
                players_stack=row[9]
            )
            
            # Fetch actions related to this hand
            hand.actions = self._get_actions_by_hand_id(hand.id)
            hands.append(hand)

        return hands

    def _get_actions_by_hand_id(self, hand_id: str) -> List[Action]:
        """Fetch all actions by hand_id"""
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, hand_id, player_idx, stack_idx, action_type, amount, card_string 
                FROM actions 
                WHERE hand_id = %s;
            """, (hand_id,))
            rows = cursor.fetchall()

        actions = [Action(
            id=row[0], 
            hand_id=row[1], 
            player_idx=row[2], 
            stack_idx=row[3], 
            action_type=row[4], 
            amount=row[5], 
            card_string=row[6]) 
            for row in rows]
        
        return actions
