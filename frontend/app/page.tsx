import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import HandHistory from "./components/handHistory";
import GameControls from "./components/gameControls";
import ActionButtons from "./components/actionButtons";
import GameLogs from "./components/gameLogs";

export default function Home() {
  return (
    <div className="flex h-screen">
      <div className="w-7/12 h-screen pb-12 pt-6 px-5">
        <h2>Playing field log</h2>
        <div className="h-full flex flex-col justify-between text-[14px]">
          <div className="h-5/6">
            <GameControls />
            <GameLogs />
            
          </div>
          <ActionButtons />
        </div>
      </div>

      <div className="w-5/12 h-screen border-gray-600 border-l-4 p-5">
        <HandHistory />
      </div>
    </div>
  );
}
