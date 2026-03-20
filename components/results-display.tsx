'use client';

import dynamic from 'next/dynamic';
import { useState } from 'react';
import { AnalyzePlanResult } from '@/lib/types';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckCircle2, Copy, Check } from 'lucide-react';

// Dynamically import jspdf to ensure it is only loaded on the client side
const jsPDF = dynamic(() => import('jspdf').then((mod) => mod.default), { ssr: false });

interface ResultsDisplayProps {
  result: AnalyzePlanResult;
}

export function ResultsDisplay({ result }: ResultsDisplayProps) {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const copyToClipboard = async (text: string, index: number) => {
    await navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const exportToPDF = async () => {
    const doc = new (await jsPDF)();
    const content = document.getElementById('results-content'); // Assuming the content has this ID
    if (content) {
      doc.text(content.innerText || '', 10, 10);
      doc.save('results.pdf');
    } else {
      console.error('Content not found');
    }
  };

  const clarityColor =
    result.clarity_score >= 80
      ? 'text-green-600'
      : result.clarity_score >= 60
      ? 'text-blue-600'
      : 'text-amber-600';

  return (
    <div className="w-full space-y-6 animate-in fade-in duration-300 relative">
      <button
        onClick={exportToPDF}
        className="absolute top-4 right-4 btn btn-primary"
      >
        Export to PDF
      </button>

      {/* Original Idea */}
      <Card className="p-6 border border-border bg-card">
        <h3 className="text-lg font-semibold text-foreground mb-2">Your Idea</h3>
        <p className="text-card-foreground italic">{result.original_idea}</p>
      </Card>

      {/* Clarity Score */}
      <Card className="p-6 border border-border bg-card">
        <div className="space-y-3">
          <h3 className="text-lg font-semibold text-foreground">Clarity Score</h3>
          <div className="flex items-end gap-4">
            <div className={`text-5xl font-bold ${clarityColor}`}>
              {result.clarity_score}
            </div>
            <div className="flex-1">
              <div className="w-full bg-muted rounded-full h-3 overflow-hidden">
                <div
                  className="bg-primary h-full transition-all duration-500"
                  style={{ width: `${result.clarity_score}%` }}
                />
              </div>
              <p className="text-sm text-muted-foreground mt-2">
                {result.clarity_score >= 80 ? 'Crystal clear!' : 
                 result.clarity_score >= 60 ? 'Pretty clear' : 
                 'Needs refinement'}
              </p>
            </div>
          </div>
        </div>
      </Card>

      {/* Structured Plan */}
      <Card className="p-6 border border-border bg-card">
        <h3 className="text-lg font-semibold text-foreground mb-4">Structured Plan</h3>
        <div className="space-y-4">
          <div>
            <h4 className="text-sm font-medium text-muted-foreground uppercase tracking-wide">Goal</h4>
            <p className="text-card-foreground mt-1">{result.structured_plan.goal}</p>
          </div>
          <div>
            <h4 className="text-sm font-medium text-muted-foreground uppercase tracking-wide">Method</h4>
            <p className="text-card-foreground mt-1">{result.structured_plan.method}</p>
          </div>
          <div>
            <h4 className="text-sm font-medium text-muted-foreground uppercase tracking-wide mb-2">Timeline</h4>
            <p className="text-card-foreground">{result.structured_plan.timeline}</p>
          </div>
          <div>
            <h4 className="text-sm font-medium text-muted-foreground uppercase tracking-wide mb-2">Steps</h4>
            <ol className="space-y-2">
              {result.structured_plan.steps.map((step, idx) => (
                <li key={idx} className="flex gap-3">
                  <span className="text-sm font-semibold text-primary flex-shrink-0">
                    {idx + 1}.
                  </span>
                  <div>
                    <p className="font-medium text-card-foreground">{step.title}</p>
                    <p className="text-sm text-muted-foreground">{step.description}</p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </Card>

      {/* Simplified Version */}
      <Card className="p-6 border border-border bg-card">
        <h3 className="text-lg font-semibold text-foreground mb-3">Simplified Version</h3>
        <p className="text-card-foreground leading-relaxed">{result.simplified_version}</p>
        <Button
          onClick={() => copyToClipboard(result.simplified_version, 0)}
          variant="outline"
          size="sm"
          className="mt-4"
        >
          {copiedIndex === 0 ? (
            <>
              <Check className="w-4 h-4 mr-2" />Copied
            </>
          ) : (
            <>
              <Copy className="w-4 h-4 mr-2" />Copy
            </>
          )}
        </Button>
      </Card>

      <div id="results-content">
        {/* The content to be exported */}
        {result.original_idea}
      </div>
    </div>
  );
}
