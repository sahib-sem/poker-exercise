from pokerkit import Automation, NoLimitTexasHoldem

from src.features.hands.presentation.schema.action import ActionCreate, ActionEnum
from src.features.hands.domain.entities.action import Action

class PokerKitService:

    def __init__(self, hole_cards:list[str], actions:list[Action], stack_size=10000, small_blind_idx = 1, big_blind_idx = 2,num_players=6,  min_bet=40 ):
        

        blinds:tuple[int,...] = (0,) * num_players
        blinds[small_blind_idx] = min_bet // 2
        blinds[big_blind_idx] = min_bet


        self.state = NoLimitTexasHoldem.create_state(
            # Automations
            (
                Automation.ANTE_POSTING,
                Automation.BET_COLLECTION,
                Automation.BLIND_OR_STRADDLE_POSTING,
                Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                Automation.HAND_KILLING,
                Automation.CHIPS_PUSHING,
                Automation.CHIPS_PULLING,
            ),
            True,  # Uniform antes?
            0,  # Antes
            blinds,  # Blinds or straddles
            min_bet,  # Min-bet
            (stack_size,) * num_players,  # Starting stacks
            num_players,  # Number of players
        )


        if hole_cards:
            for card in hole_cards:
                self.state.deal_hole(card)
        else:
            for _ in range(num_players):
                self.state.deal_hole()
                self.state.deal_hole()
        
        for action in actions:

            if action.action_type == 'fold':
                self.state.fold()
            elif action.action_type == 'call' or action.action_type == 'check':
                self.state.check_or_call()
            elif action.action_type == 'raise' or action.action_type == 'all_in' or action.action_type == 'bet':
                self.state.complete_bet_or_raise_to(action.amount)
            elif action.action_type == 'burn':
                self.state.burn_card(action.card_string)
            elif action.action_type == 'deal':
                self.state.deal_board(action.card_string)

    def validate_action(self, action:ActionCreate) -> bool:
        
        if action.action_type == 'fold':
            return self.state.can_fold()
        elif action.action_type == 'call' or action.action_type == 'check':
            return self.state.can_check_or_call()
        elif action.action_type == 'raise' or action.action_type == 'all_in' or action.action_type == 'bet':
            return self.state.can_complete_bet_or_raise_to(action.amount)
        elif action.action_type == 'burn':
            return self.state.can_burn_card()
        elif action.action_type == 'deal':
            return self.state.can_deal_board()
        
        
        return False

    def get_possible_actions(self) -> list[ActionEnum]:
        actions = []
        if self.state.can_fold():
            actions.append(ActionEnum.FOLD)
        if self.state.can_check_or_call():
            actions.append(ActionEnum.CHECK)
            actions.append(ActionEnum.CALL)
        if self.state.can_complete_bet_or_raise_to():
            actions.append(ActionEnum.RAISE)
            actions.append(ActionEnum.BET)
            actions.append(ActionEnum.ALLIN)
        return actions
    def get_state(self):
        return self.state

    def get_hole_cards(self) -> list[str]:

        hole_cards = self.state.hole_cards

        return ["".join([card.rank + card.suit for card in cards]) for cards in hole_cards]

    def get_board_cards(self) -> list[str]:
        return [card.rank + card.suit for card in self.state.get_board_cards(0)]
    
    def get_stacks(self) -> list[int]:
        return self.state.stacks

    def get_actor_index(self) -> int | None:
        return self.state.actor_index

    def get_street_index(self) -> int | None:
        return self.state.street_index

    def get_min_bet(self) -> int:
        min_bet = self.state.min_completion_betting_or_raising_to_amount
        if min_bet == None:
            return 0
        return min_bet
    
    def get_max_bet(self) -> int: 
        max_bet = self.state.max_completion_betting_or_raising_to_amount

        if max_bet == None:
            return 0
        return max_bet

