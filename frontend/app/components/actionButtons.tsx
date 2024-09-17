'use client';
import { Button } from '@/components/ui/button'
import React from 'react'
import { BIG_BLIND_SIZE, MINIMUM_BET, useGameStore } from '../store/gameState'; 

export default function ActionButtons() {
  const {
    actions, 
    currentBet,
    currentRaise,
    performAction, 
    incrementBetOrRaise,
    decrementBetOrRaise,
    raiseBetMax
  } = useGameStore()

  const betButtonDisabled = !actions.includes('bet')
  const raiseButtonDisabled = !actions.includes('raise')

  const handleAction = (actionType: string, amount: number = 0, raiseAmount:number = 0) => {
    performAction(actionType, amount, raiseAmount)
  }

  return (
    <div className="flex w-full flex-wrap space-x-2 text-[14px] space-y-1 mt-4">

      <Button
        className="rounded-[4px] border border-gray-700 bg-sky-500 px-4 mt-[4px] text-black w-16 h-6 text-xs p-0"
        disabled={!actions.includes('fold')}
        onClick={() => handleAction('fold')}
      >
        fold
      </Button>


      <Button
        size="sm"
        className="rounded-[4px] border bg-lime-300 text-black w-16 h-6 text-xs p-0"
        disabled={!actions.includes('check')}
        onClick={() => handleAction('check')}
      >
        check
      </Button>

      <Button
        className="rounded-[4px] border bg-lime-300 px-4 text-black w-16 h-6 text-xs p-0"
        disabled={!actions.includes('call')}
        onClick={() => handleAction('call')}
      >
        call
      </Button>

      <Button
        className="rounded-[6px] text-[12px] border bg-yellow-800 text-black w-10 h-6 text-xs p-0"
        disabled={betButtonDisabled || (currentBet - BIG_BLIND_SIZE < MINIMUM_BET) }
        onClick={() => decrementBetOrRaise('bet')}
      >
        -
      </Button>

      <Button
        className="rounded-[4px] border bg-yellow-800 px-4 text-black w-20 h-6 text-xs p-0"
        disabled={!actions.includes('bet')}
        onClick={() => handleAction('bet', currentBet)}
      >
        bet {currentBet}
      </Button>

      <Button
        className="rounded-[6px] text-[12px] border bg-yellow-800 text-black w-10 h-6 text-xs p-0"
        disabled={betButtonDisabled || (currentBet + BIG_BLIND_SIZE > raiseBetMax)}
        onClick={() => incrementBetOrRaise('bet')}
      >
        +
      </Button>

      <Button
        className="rounded-[6px] text-[12px] border bg-yellow-800 text-black w-10 h-6 text-xs p-0"
        disabled={raiseButtonDisabled || (currentRaise - BIG_BLIND_SIZE < BIG_BLIND_SIZE)}
        onClick={() => decrementBetOrRaise('raise')}
      >
        -
      </Button>

      <Button
        className="rounded-[4px] border bg-yellow-800 text-black w-20 h-6 text-xs p-0"
        disabled={!actions.includes('raise')}
        onClick={() => handleAction('raise', 0,  currentRaise)}
      >
        raise {currentRaise}
      </Button>

      <Button
        className="rounded-[6px] text-[12px] border bg-yellow-800 text-black w-10 h-6 text-xs p-0"
        disabled={raiseButtonDisabled || (currentRaise + BIG_BLIND_SIZE > raiseBetMax)}
        onClick={() => incrementBetOrRaise('raise')}
      >
        +
      </Button>

      <Button
        className="rounded-[4px] border bg-red-500 text-black w-16 h-6 text-xs p-0"
        disabled={!actions.includes('all_in')}
        onClick={() => handleAction('all_in')}
      >
        All in
      </Button>
    </div>
  )
}
