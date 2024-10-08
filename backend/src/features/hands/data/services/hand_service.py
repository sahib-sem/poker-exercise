from src.features.hands.data.repositories.action_repo import ActionRepository
from src.features.hands.data.repositories.hand_repo import HandRepository
from src.features.hands.data.repositories.player_repo import PlayerRepository
from src.features.hands.domain.entities.action import Action
from src.features.hands.domain.entities.hand import Hand
from src.features.hands.domain.entities.player import Player
from src.features.hands.presentation.schema.action import (
    ActionCreate,
    ActionResponse,
    DealtCards,
)
from src.features.hands.presentation.schema.hand import CreateHand

from .pokerkit_service import PokerKitService


class HandService:

    def __init__(
        self,
        action_repo: ActionRepository,
        hand_repo: HandRepository,
        player_repo: PlayerRepository,
    ):
        self.action_repo = action_repo
        self.hand_repo = hand_repo
        self.player_repo = player_repo

    def start_game(self, hand_data: CreateHand) -> Hand:

        hand = Hand(**hand_data.model_dump())

        # Create a new hand in the database
        hand = self.hand_repo.create_hand(hand)

        # create the poker state
        poker_service = PokerKitService(
            [],
            [],
            hand.stack_size,
            hand.small_blind_idx,
            hand.big_blind_idx,
            hand.number_of_players,
        )

        hole_cards = poker_service.get_hole_cards()

        for idx, card in enumerate(hole_cards):
            player = Player(hand.id, idx, hand.stack_size, card)
            self.player_repo.create_player(player)

        hand = self.hand_repo.get_hand_by_id(hand.id)

        return hand

    def add_action(self, action: ActionCreate) -> ActionResponse:

        hand = self.hand_repo.get_hand_by_id(action.hand_id)

        if hand is None:
            return ActionResponse(success=False, message="Hand not found")

        if hand.has_ended:
            return ActionResponse(success=False, message="Hand has ended")

        hole_cards = [
            player.hole_cards
            for player in sorted(hand.players, key=lambda x: x.player_idx)
        ]

        poker_service = PokerKitService(
            hole_cards,
            hand.actions,
            hand.stack_size,
            hand.small_blind_idx,
            hand.big_blind_idx,
            hand.number_of_players,
        )
        current_actor = poker_service.get_actor_index()

        if action.action_type == "all_in":
            action.amount = (
                poker_service.get_state().get_effective_stack(
                    current_actor
                    )
                )
        elif action.action_type == "raise":
            action.amount = max(poker_service.get_bets()) + action.raise_amount
        valid = poker_service.validate_action(action)

        if not valid:
            return ActionResponse(success=False, message="Invalid action")

        action_entity = Action(**action.model_dump())
        self.action_repo.create_action(action_entity)
        poker_service.apply_action(action)

        state = poker_service.get_state()
        dealt_cards = []

        while state.can_burn_card():
            street_idx = state.street_index
            state.burn_card()
            burn_action = Action(
                hand_id=action.hand_id,
                action_type="burn",
                card_string=(
                    state.burn_cards[-1].rank
                    + state.burn_cards[-1].suit
                ),
            )
            self.action_repo.create_action(burn_action)

            state.deal_board()

            cards = [
                card.rank +
                card.suit for card in state.get_board_cards(0)]
            if street_idx == 1:
                card_string = "".join(cards[0:3])

            else:
                card_string = cards[-1]

            dealt_cards.append(
                DealtCards(street_idx=street_idx, card_string=card_string)
            )

            deal_action = Action(
                hand_id=action.hand_id,
                action_type="deal",
                card_string=card_string,
            )

            self.action_repo.create_action(deal_action)

        game_ended = state.status is False

        if game_ended:
            hand.has_ended = True
            self.hand_repo.update_hand(hand)

            for player in hand.players:
                player.winnings = state.payoffs[player.player_idx]
                self.player_repo.update_player(player)

        return ActionResponse(
            success=True,
            current_actor=current_actor,
            next_actor=poker_service.get_actor_index(),
            possible_moves=(
                [] if game_ended else poker_service.get_possible_actions()),
            maximum_bet=poker_service.get_max_bet() -
            poker_service.get_min_bet(),
            game_ended=game_ended,
            dealt_cards=dealt_cards,
            pot_amount=poker_service.get_pot_amount(),
        )

    def get_hands_by_status(self, status: bool) -> list[Hand]:
        return self.hand_repo.get_hands_by_status(status)
