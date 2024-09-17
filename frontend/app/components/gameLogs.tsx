"use client";

import { ScrollArea } from "@/components/ui/scroll-area";
import { useGameStore } from "../store/gameState";
import { useRef, useEffect } from "react";

export default function GameLogs() {
  const logs = useGameStore((state) => state.logs);

  const scrollAreaRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const scrollAreaElement = scrollAreaRef.current?.querySelector('[data-radix-scroll-area-viewport]');
    if (scrollAreaElement) {
        scrollAreaElement.scrollTo({ top: scrollAreaElement.scrollHeight, behavior: 'smooth' });
    }
  }, [logs]);

  

  return (
    <ScrollArea className="h-full text-[10px] p-2" ref={scrollAreaRef}>
      <div >
        {logs.map((log, index) => (
          <p
            key={index}
            className={`${log.isBold ? "font-bold" : "font-normal"} text-black`}
          >
            {log.log}
          </p>
        ))}
      </div>
    </ScrollArea>
  );
}
