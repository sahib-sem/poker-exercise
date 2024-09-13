

from src.features.hands.domain.entities.player import Player
from src.features.hands.data.repositories.player_repo import PlayerRepository
from src.features.hands.domain.entities.action import Action
from src.features.hands.presentation.schema.action import ActionCreate, ActionResponse
from src.features.hands.data.repositories.action_repo import ActionRepository
from src.features.hands.data.repositories.hand_repo import HandRepository
from src.features.hands.presentation.schema.hand import CreateHand
from src.features.hands.domain.entities.hand import Hand
from .pokerkit_service import PokerKitService


class HandService:

    def __init__(self, action_repo: ActionRepository, hand_repo: HandRepository, player_repo:PlayerRepository):
        self.action_repo = action_repo
        self.hand_repo = hand_repo
        self.player_repo = player_repo
    
    def start_game(self, hand_data: CreateHand) -> Hand:

        hand = Hand(**hand_data.model_dump())

        # Create a new hand in the database
        hand = self.hand_repo.create_hand(hand)

        # create the poker state 
        poker_service = PokerKitService([], [], hand.stack_size, hand.small_blind_idx, hand.big_blind_idx, hand.number_of_players)

        hole_cards = poker_service.get_hole_cards()

        for idx, card in enumerate(hole_cards):
            player = Player(hand.id, idx, hand.stack_size, card)
            self.player_repo.create_player(player)

        hand = self.hand_repo.get_hand_by_id(hand.id)

        return hand


    def add_action(self, action: ActionCreate) -> ActionResponse:

        hand = self.hand_repo.get_hand_by_id(action.hand_id)

        if hand is None:
            return ActionResponse(success=False, message='Hand not found')
        
        if hand.has_ended:
            return ActionResponse(success=False, message='Hand has ended')

        hole_cards = [player.hole_cards for player in sorted(hand.players, key=lambda x: x.player_idx)] 

        poker_service = PokerKitService(hole_cards, hand.actions, hand.stack_size, hand.small_blind_idx, hand.big_blind_idx, hand.number_of_players)

        valid = poker_service.validate_action(action)

        if not valid:
            return ActionResponse(success=False, message='Invalid action')
        
        action_entity = Action(**action.model_dump())
        self.action_repo.create_action(action_entity)
        poker_service.apply_action(action)

        state = poker_service.get_state()

        if state.can_burn_card():
            state.burn_card()
            burn_action = Action(hand_id = action.hand_id,  action_type='burn', card_string= state.burn_cards[-1].rank + state.burn_cards[-1].suit)
            self.action_repo.create_action(burn_action)

            state.deal_board()

            card_string = ''
            cards = [card.rank + card.suit for card in state.get_board_cards(0)]
            if state.street_index == 1:
                card_string = "".join(cards[0:3])
            
            else:
                card_string = cards[-1]
            
            deal_action = Action(hand_id = action.hand_id,  action_type='deal', card_string= card_string)

            self.action_repo.create_action(deal_action)

            return ActionResponse(success=True, next_actor=poker_service.get_actor_index(), possible_moves=poker_service.get_possible_actions(), minimum_bet=poker_service.get_min_bet(), maximum_bet=poker_service.get_max_bet(), game_ended= state.street_index == None, street_idx=poker_service.get_street_index(), card_string=card_string)
        
        game_ended = state.street_index == None

        if game_ended:
            hand.has_ended = True
            self.hand_repo.update_hand(hand)

            for player in hand.players:
                player.winnings = state.stacks[player.player_idx] - player.initial_stack_size
                self.player_repo.update_player(player)
    
        return ActionResponse(success=True, next_actor=poker_service.get_actor_index(), possible_moves=poker_service.get_possible_actions(), minimum_bet=poker_service.get_min_bet(), maximum_bet=poker_service.get_max_bet(), game_ended= state.street_index == None, street_idx=state.street_index, card_string='')

    def get_hands_by_status(self, status: bool) -> list[Hand]:
        return self.hand_repo.get_hands_by_status(status)
    
    

        







        
