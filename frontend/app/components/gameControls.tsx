'use client';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useState } from 'react';
import { useGameStore } from "../store/gameState";

export default function GameControls() {
  const initializeGame = useGameStore((state) => state.initializeGame);
  const hasGameStartedOnce = useGameStore((state) => state.hasGameStartedOnce);
  const applyStackSize = useGameStore((state) => state.applyStackSize);
  const stackSize = useGameStore((state) => state.stackSize);

  const handleFormSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const newStackSize = Number(formData.get('stacksize'));

    console.log('newStackSize', newStackSize);
    
    if (newStackSize >= 100) {
      console.log('updated')
      applyStackSize(newStackSize);
    }

  };

  const handleStartResetGame = () => {
    initializeGame(stackSize); 
  };

  return (
    <div className="flex w-full flex-wrap justify-start items-center space-x-5 space-y-2 pt-3">
      <h2 className="flex-shrink-0 pr-5">Stack</h2>
      {/* Form for stack size input and Apply button */}
      <form className="flex items-center space-x-3" onSubmit={handleFormSubmit}>
        <Input
          type="number"
          name="stacksize"
          placeholder="stack size"
          defaultValue={stackSize}
          min={100}
          className="p-2 border border-gray-800 bg-sky-50 rounded-[4px] w-24 h-6 text-xs"
        />
        <Button
          type="submit"
          variant="ghost"
          className="rounded-[4px] border border-gray-700 w-16 h-6 text-xs p-0"
        >
          Apply
        </Button>
      </form>

      <Button
        className={`rounded-[4px] border border-gray-700 w-16 h-6 text-xs p-0 ${
          hasGameStartedOnce ? 'bg-red-500 text-black' : 'bg-green-500 text-black'
        }`}
        onClick={handleStartResetGame}
      >
        {hasGameStartedOnce ? 'Reset' : 'Start'}
      </Button>
    </div>
  );

}
