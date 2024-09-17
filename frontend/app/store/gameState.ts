import { create } from "zustand";
import api from "../lib/axios";

export const MINIMUM_BET = 20;
export const BIG_BLIND_SIZE = 40;
export const STACK_SIZE = 10000;
export const NUMBER_OF_PLAYERS = 6;
export const ACTION_TYPES = ["fold", "check", "call", "all_in", "bet", "raise"];

type Player = {
  hand_id: string;
  player_idx: number;
  initial_stack_size: number;
  hole_cards: string;
  winnings: number;
};

type HandHistoryItem = {
  hand_id: string;
  stack_size: number;
  dealer_idx: number;
  small_blind_idx: number;
  big_blind_idx: number;
  players: Player[];
  action_string: string;
}

type Logs = {
  log: string;
  isBold: boolean;
};

type GameState = {
  gameId: string | null;
  players: Player[];
  stackSize: number;
  bigBlindSize: number;
  raiseBetMax: number;
  currentBet: number;
  currentRaise: number;
  actions: string[];
  nextActor: number | null;
  logs: Logs[];
  handHistory: HandHistoryItem[];
  hasGameStartedOnce: boolean;
  gameHasEnded: boolean;
  initializeGame: (stackSize: number) => Promise<void>;
  performAction: (actionType: string, amount: number, raiseAmount:number) => Promise<void>;
  resetGame: () => void;
  getHandHistory: () => Promise<void>;
  applyStackSize: (stackSize: number) => void;
  incrementBetOrRaise: (type: string) => void;
  decrementBetOrRaise: (type: string) => void;
};

const formatAction = (actionType: string) => {
  if (actionType == "fold") {
    return "folds";
  } else if (actionType == "check") {
    return "checks";
  } else if (actionType == "call") {
    return "calls";
  } else if (actionType == "all_in") {
    return "went all in";
  } else if (actionType == "bet") {
    return "bets";
  }
  return "raises to";
};

const formatGamePhase = (street_idx: number) => {
  if (street_idx == 1) {
    return "Flop cards dealt: ";
  } else if (street_idx == 2) {
    return "Turn card dealt: ";
  }
  return "River card dealt: ";
};

export const useGameStore = create<GameState>((set, get) => ({
  gameId: null,
  players: [],
  stackSize: STACK_SIZE,
  bigBlindSize: BIG_BLIND_SIZE,
  raiseBetMax: STACK_SIZE - BIG_BLIND_SIZE,
  currentBet: MINIMUM_BET,
  currentRaise: BIG_BLIND_SIZE,
  actions: [],
  nextActor: null,
  logs: [],
  handHistory: [],
  hasGameStartedOnce: false,
  gameHasEnded: false,

  initializeGame: async (stackSize: number) => {

    let state = get()
    state.resetGame()
    try {
      const response = await api.post("/hands", {
        stack_size: stackSize,
        number_of_players:NUMBER_OF_PLAYERS,
      });

      const { id, players, small_blind_idx, big_blind_idx, dealer_idx } =
        response.data;

      let startGameLogs: Logs[] = [];

      players.forEach((player: Player) => {
        startGameLogs.push({
          log: `Player ${player.player_idx + 1} is dealt ${player.hole_cards}.`,
          isBold: false,
        });
      });
      startGameLogs.push({ log: "- - -", isBold: false });
      startGameLogs.push({
        log: `Player ${dealer_idx + 1} is the dealer.`,
        isBold: false,
      });
      startGameLogs.push({
        log: `Player ${small_blind_idx + 1} posts the small blind - 20 chips.`,
        isBold: false,
      });
      startGameLogs.push({
        log: `Player ${big_blind_idx + 1} posts the big blind - 40 chips.`,
        isBold: false,
      });
      startGameLogs.push({ log: "- - -", isBold: false });
      set({
        gameId: id,
        players,
        actions: ["fold", "raise", "all_in", "call"],
        hasGameStartedOnce: true,
        logs: [...startGameLogs],
      });
    } catch (error) {
      console.error("Failed to initialize game:", error);
    }
  },

  performAction: async (actionType: string, amount: number, raiseAmount:number) => {
    const { gameId } = get();
    if (!gameId) return;

    try {
      const response = await api.post(`/hands/${gameId}/actions`, {
        hand_id: gameId,
        action_type: actionType,
        raise_amount: raiseAmount,
        amount,
      });

      const {
        success,
        current_actor,
        maximum_bet,
        next_actor,
        possible_moves,
        game_ended,
        dealt_cards,
        pot_amount
      } = response.data;

      if (success) {
        let actionLogs: Logs[] = [];

        if (
          actionType == "fold" ||
          actionType == "check" ||
          actionType == "call" ||
          actionType == "all_in"
        ) {
          actionLogs.push({
            log: `Player ${current_actor + 1}  ${formatAction(actionType)}.`,
            isBold: false,
          });
        } else if (actionType == "bet") {
          actionLogs.push({
            log: `Player ${current_actor + 1} ${formatAction(
              actionType
            )} ${amount}.`,
            isBold: false,
          });
        }

        else if (actionType == "raise") {
          actionLogs.push({
            log: `Player ${current_actor + 1} ${formatAction(
              actionType
            )} ${raiseAmount}.`,
            isBold: false,
          });
        }

         for ( var dealt_card of dealt_cards) {
          actionLogs.push({
            log: `${formatGamePhase(dealt_card.street_idx)}${dealt_card.card_string}.`,
            isBold: true,
          });
        }

        if (game_ended) {
          actionLogs.push({ log: `Hand #${gameId} ended.`, isBold: true });
          actionLogs.push({
            log: `final pot was ${pot_amount}.`,
            isBold: true,
          });
          get().getHandHistory();
        }

        set({
          actions: possible_moves,
          raiseBetMax: maximum_bet,
          gameHasEnded: game_ended,
          nextActor: next_actor,
          currentBet: MINIMUM_BET,
          currentRaise: BIG_BLIND_SIZE,
          logs: [...get().logs, ...actionLogs],
        });
      }
    } catch (error) {
      console.error("Failed to perform action:", error);
    }
  },

  resetGame: () => {
    set({
      gameId: null,
      players: [],
      stackSize: 10000,
      actions: [],
      hasGameStartedOnce: false,
      logs: [],
      nextActor: null,
      gameHasEnded: false,
      currentBet: MINIMUM_BET,
      currentRaise: BIG_BLIND_SIZE,
      raiseBetMax: STACK_SIZE - BIG_BLIND_SIZE,
    });
  },



  applyStackSize: (stackSize: number) => {
    if (stackSize >= 100) {
      set({
        stackSize,
      });
    }
  },

  incrementBetOrRaise: (type: string) => {
    const { currentBet, currentRaise, raiseBetMax } = get();
    if (type == "bet") {
      if (currentBet + BIG_BLIND_SIZE <= raiseBetMax) {
        set({
          currentBet: currentBet + BIG_BLIND_SIZE,
        });
      }
    } else {
      if (currentRaise + BIG_BLIND_SIZE <= raiseBetMax) {
        set({
          currentRaise: currentRaise + BIG_BLIND_SIZE,
        });
      }
    }
  },

  decrementBetOrRaise: (type: string) => {
    const { currentBet, currentRaise } = get();
    if (type == "bet") {
      if (currentBet - BIG_BLIND_SIZE >= MINIMUM_BET) {
        set({
          currentBet: currentBet - BIG_BLIND_SIZE,
        });
      }
    } else {
      if (currentRaise - BIG_BLIND_SIZE >= BIG_BLIND_SIZE) {
        set({
          currentRaise: currentRaise - BIG_BLIND_SIZE,
        });
      }
    }
  },

  getHandHistory: async () => {
    

    try {
      const response = await api.get(`/hands?status=completed`);

      let handHistory: HandHistoryItem[] =  response.data.map((handItem:any) => {
        
        let actionStringArray: string[] = [];

        let actions: any[] = handItem.actions;

        actions.map((action:any, index) => {
          if (action.action_type == 'deal') {
            actionStringArray.push(` ${action.card_string} `);
          }  else if (action.action_type == 'bet') {
            actionStringArray.push(`b${action.amount}`);
          } else if (action.action_type == 'raise') {
            actionStringArray.push(`r${action.raise_amount}`);
          } else if (action.action_type == 'call') {
            actionStringArray.push(`c`);
          } else if (action.action_type == 'check') {
            actionStringArray.push(`x`);
          } else if (action.action_type == 'fold') {
            actionStringArray.push(`f`);
          } else if (action.action_type == 'all_in') {
            actionStringArray.push(`allin`);
          }

          
          if (index < actions.length - 1 && (index < actions.length - 1 && (ACTION_TYPES.includes(action.action_type) && ACTION_TYPES.includes(actions[index + 1].action_type)))) {
            actionStringArray.push(":");
          }
        });

        let actionString = actionStringArray.join("");

        let handHistoryItem: HandHistoryItem = {
          hand_id: handItem.id,
          stack_size: handItem.stack_size,
          dealer_idx: handItem.dealer_idx,
          small_blind_idx: handItem.small_blind_idx,
          big_blind_idx: handItem.big_blind_idx,
          players: handItem.players,
          action_string: actionString
        }

        return handHistoryItem;
      });

      set({
        handHistory: handHistory,
      });

      
    } catch (error) {
      console.error("Failed to get hand history:", error);
    }
  },
}

));