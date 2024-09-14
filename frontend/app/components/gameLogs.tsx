'use client';

import { useGameStore } from "../store/gameState";

export default function GameLogs() {
    const logs = useGameStore((state) => state.logs);
    console.log(logs, 'logs');
  return (
    <div className="text-[8px] p-2">
      {logs.map((log, index) => (
          <p
            key={index}
            className={`${log.isBold ? 'font-bold' : 'font-normal'} text-black`}
          >
            {log.log}
          </p>
        ))}
    </div>
  );
}
