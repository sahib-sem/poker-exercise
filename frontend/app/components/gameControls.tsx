import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import React from 'react'

export default function GameControls() {
  return (
    <div className="flex w-full flex-wrap justify-start items-center space-x-5 space-y-2 pt-3">
            <h2 className="flex-shrink-0 pr-5">Stack</h2>
            <Input
              type="number"
              placeholder="stacksize"
              defaultValue={10000}
              className="p-2 border border-gray-800 bg-sky-50 rounded-[4px] w-24 h-6 text-xs"
            />
            <Button
              variant="ghost"
              className="rounded-[4px] border border-gray-700 w-16 h-6 text-xs p-0"
            >
              Apply
            </Button>
            <Button className="rounded-[4px] border border-gray-700 bg-red-500 text-black w-16 h-6 text-xs p-0">
              Start
            </Button>
          </div>
  )
}
