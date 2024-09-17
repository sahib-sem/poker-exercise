"use client";

import { useGameStore } from "../store/gameState";
import { useEffect, useRef } from "react";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";

export default function HandHistory() {
  const getHandHistory = useGameStore((state) => state.getHandHistory);
  const handHistory = useGameStore((state) => state.handHistory);
  const scrollAreaRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
   
    getHandHistory();
  }, [getHandHistory]);

  useEffect(() => {

    const scrollAreaElement = scrollAreaRef.current?.querySelector('[data-radix-scroll-area-viewport]');
    if (scrollAreaElement) {
      scrollAreaElement.scrollTo({ top: scrollAreaElement.scrollHeight, behavior: 'smooth' });
    }
  }, [handHistory]);

  console.log(handHistory[handHistory.length - 1], 'handHistory');

  return (
    <div className="bg-sky-50 p-3 border text-gray-500 rounded-[4px] h-[90vh]">
      <h1>Hand History</h1>

      <ScrollArea className="h-[80vh] pr-4" ref={scrollAreaRef}>
        <div className="text-black text-[12px] mx-2">

          {handHistory.map((item, index) => {
            const playerWinnings = item.players.map((player, index) => {
              return `Player ${player.player_idx + 1}: ${player.winnings}`;
            });
            const playerHoleCards = item.players.map((player, index) => {
              return `Player ${player.player_idx + 1}: ${player.hole_cards}`;
            });
            return (
              <div key={item.hand_id} className="bg-blue-200 p-2 my-2 ml-1">
                <ScrollArea  className="w-[30vw] whitespace-nowrap">
                  <div className="p-2">
                    <div>{`Hand  #${item.hand_id}`}</div>
                    <div>{`Stack  ${item.stack_size}; Dealer: Player ${
                      item.dealer_idx + 1
                    };  Player ${item.small_blind_idx + 1} Small blind;  Player ${
                      item.big_blind_idx + 1
                    } Big blind `}</div>
                    <div>{`Hands:  ${playerHoleCards.join(";  ")}`}</div>
                    <div>{`Actions:  ${item.action_string}`}</div>
                    <div>{`Winnings: ${playerWinnings.join(";  ")}`}</div>
                  </div>
                  <ScrollBar orientation="horizontal" className="h-[6px]" />
                </ScrollArea>
              </div>
            );
          })}
        </div>

        
        <ScrollBar orientation="vertical" className="w-[6px]" />
      </ScrollArea>
    </div>
  );
}
