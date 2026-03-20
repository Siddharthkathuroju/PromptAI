'use client'

import { useState } from 'react'
import { InputForm } from '@/components/input-form'
import { ResultsDisplay } from '@/components/results-display'
import { AnalyzePlanResult } from '@/lib/types'
import { analyzePlan } from '@/lib/api-client'
import { AlertCircle } from 'lucide-react'
import { Card } from '@/components/ui/card'

export default function Home() {
  const [result, setResult] = useState<AnalyzePlanResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (idea: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await analyzePlan({ idea })
      setResult({
        ...response,
        original_idea: idea,
      })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred. Please try again.')
      setResult(null)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-background via-background to-background py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-12 text-center">
          <h1 className="text-4xl sm:text-5xl font-bold text-foreground mb-3 text-balance">
            Intuitive Draft
          </h1>
          <p className="text-lg text-muted-foreground text-balance">
            Transform your vague ideas into clear, actionable plans powered by AI
          </p>
        </div>

        {/* Main Content */}
        <div className="space-y-8">
          {/* Input Section */}
          <Card className="p-8 border border-border bg-card shadow-lg">
            <InputForm onSubmit={handleSubmit} isLoading={isLoading} />
          </Card>

          {/* Error State */}
          {error && (
            <Card className="p-4 border border-destructive/30 bg-destructive/5 animate-in fade-in duration-300">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-destructive mb-1">Error</h3>
                  <p className="text-sm text-muted-foreground">{error}</p>
                  <p className="text-xs text-muted-foreground mt-2">
                    Make sure the backend API is running at {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
                  </p>
                </div>
              </div>
            </Card>
          )}

          {/* Results Section */}
          {result && (
            <>
              <div className="text-center">
                <button
                  onClick={() => setResult(null)}
                  className="text-sm text-primary hover:text-primary/80 font-medium transition-colors"
                >
                  ← Start over with a new idea
                </button>
              </div>
              <ResultsDisplay result={result} />
            </>
          )}

          {/* Empty State */}
          {!result && !isLoading && !error && (
            <Card className="p-8 border border-dashed border-border bg-muted/20 text-center">
              <div className="space-y-2">
                <p className="text-muted-foreground">
                  Enter an idea above to get started
                </p>
              </div>
            </Card>
          )}
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-xs text-muted-foreground">
          <p>Powered by AI • Built with Next.js</p>
        </div>
      </div>
    </main>
  )
}
