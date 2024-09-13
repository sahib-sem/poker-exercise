import psycopg2
from typing import List, Optional
from src.features.hands.domain.entities.action import Action

class ActionRepository:
    def __init__(self, db_conn: psycopg2.extensions.connection):
        self.db_conn = db_conn

    def create_action(self, action: Action) -> Action:
        """Insert a new action into the database"""
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO actions (hand_id, action_type, amount, card_string)
                VALUES (%s, %s, %s, %s) RETURNING id;
            """, (action.hand_id, action.action_type, action.amount, action.card_string))
            self.db_conn.commit()
            action.id = cursor.fetchone()[0] 
        return action

    def get_actions_by_hand_id(self, hand_id: str) -> List[Action]:
        """Fetch all actions by hand_id"""
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, hand_id, action_type, amount, card_string 
                FROM actions 
                WHERE hand_id = %s;
            """, (hand_id,))
            rows = cursor.fetchall()

        actions = [Action(
            id=row[0], 
            hand_id=row[1], 
           
            
            action_type=row[2], 
            amount=row[3], 
            card_string=row[4]) 
            for row in rows]
        
        return actions
