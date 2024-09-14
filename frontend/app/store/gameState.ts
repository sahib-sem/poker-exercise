import { create } from "zustand";
import api from "../lib/axios";

export const MINIMUM_BET = 20;
export const BIG_BLIND_SIZE = 40;
export const STACK_SIZE = 10000;

type Player = {
  hand_id: string;
  player_idx: number;
  initial_stack_size: number;
  hole_cards: string;
  winnings: number;
};

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
  hasGameStartedOnce: boolean;
  gameHasEnded: boolean;
  initializeGame: (stackSize: number) => Promise<void>;
  performAction: (actionType: string, amount: number) => Promise<void>;
  resetGame: () => void;
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
  hasGameStartedOnce: false,
  gameHasEnded: false,

  initializeGame: async (stackSize: number) => {

    let state = get()
    state.resetGame()
    try {
      const response = await api.post("/hands", {
        stack_size: stackSize,
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

  performAction: async (actionType: string, amount: number) => {
    const { gameId } = get();
    if (!gameId) return;

    try {
      const response = await api.post(`/hands/${gameId}/actions`, {
        hand_id: gameId,
        action_type: actionType,
        amount,
      });

      const {
        success,
        current_actor,
        maximum_bet,
        next_actor,
        possible_moves,
        game_ended,
        street_idx,
        card_string,
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
        } else if (actionType == "bet" || actionType == "raise") {
          actionLogs.push({
            log: `Player ${current_actor + 1} ${formatAction(
              actionType
            )} ${amount}.`,
            isBold: false,
          });
        }

        if (card_string != "") {
          actionLogs.push({
            log: `${formatGamePhase(street_idx)}${card_string}.`,
            isBold: true,
          });
        }

        if (game_ended) {
          actionLogs.push({ log: `Hand #${gameId} ended.`, isBold: true });
          actionLogs.push({
            log: `final pot was ${pot_amount}.`,
            isBold: true,
          });
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
}));
