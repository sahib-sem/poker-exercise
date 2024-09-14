import { Button } from '@/components/ui/button'
import React from 'react'

export default function ActionButtons() {
  return (
    <div className="flex w-full flex-wrap space-x-2 text-[14px] space-y-1">
          <Button className="rounded-[4px] border border-gray-700 bg-sky-500 px-4 mt-[4px] text-black w-16 h-6 text-xs p-0">
            fold
          </Button>
          <Button
            size="sm"
            className="rounded-[4px] border border-gray-700 bg-lime-300 text-black w-16 h-6 text-xs p-0"
          >
            check
          </Button>

          <Button className="rounded-[4px] border border-gray-700 bg-lime-300 px-4 text-black w-16 h-6 text-xs p-0">
            call
          </Button>
          <Button className="rounded-[6px] text-[12px] border border-gray-700 bg-yellow-800 text-black w-10 h-6 text-xs p-0">
            -
          </Button>
          <Button className="rounded-[4px] border border-gray-700 bg-yellow-800 px-4 text-black w-16 h-6 text-xs p-0">
            bet 20
          </Button>
          <Button className="rounded-[6px] text-[12px] border border-gray-700 bg-yellow-800 text-black w-10 h-6 text-xs p-0">
            +
          </Button>
          <Button className="rounded-[6px] text-[12px] border border-gray-700 bg-yellow-800 text-black w-10 h-6 text-xs p-0">
            -
          </Button>
          <Button className="rounded-[4px] border border-gray-700 bg-yellow-800 text-black w-20 h-6 text-xs p-0">
            raise 40
          </Button>
          <Button className="rounded-[6px] text-[12px] border border-gray-700 bg-yellow-800 text-black w-10 h-6 text-xs p-0">
            +
          </Button>
          <Button className="rounded-[4px] border border-gray-700 bg-red-500 text-black w-16 h-6 text-xs p-0">
            All in
          </Button>
        </div>
  )
}
