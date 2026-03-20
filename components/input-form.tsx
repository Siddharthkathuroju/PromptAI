'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Spinner } from '@/components/ui/spinner'

interface InputFormProps {
  onSubmit: (idea: string) => Promise<void>
  isLoading: boolean
}

export function InputForm({ onSubmit, isLoading }: InputFormProps) {
  const [idea, setIdea] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!idea.trim()) return
    await onSubmit(idea)
  }

  return (
    <form onSubmit={handleSubmit} className="w-full space-y-4">
      <div className="space-y-2">
        <label htmlFor="idea" className="block text-sm font-medium text-foreground">
          Describe your idea
        </label>
        <textarea
          id="idea"
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          placeholder="What's your idea? Be as vague or detailed as you like..."
          disabled={isLoading}
          className="w-full h-40 px-4 py-3 rounded-lg border border-border bg-card text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary disabled:opacity-50 disabled:cursor-not-allowed resize-none"
        />
      </div>
      <Button
        type="submit"
        disabled={isLoading || !idea.trim()}
        className="w-full sm:w-auto bg-primary hover:bg-primary/90 text-primary-foreground"
      >
        {isLoading ? (
          <>
            <Spinner className="mr-2 h-4 w-4" />
            Analyzing...
          </>
        ) : (
          'Analyze Idea'
        )}
      </Button>
    </form>
  )
}
