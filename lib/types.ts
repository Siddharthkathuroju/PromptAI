export interface PlanStep {
  title: string;
  description: string;
}

export interface AnalyzePlanRequest {
  idea: string;
}

export interface AnalyzePlanResponse {
  clarity_score: number;
  structured_plan: {
    goal: string;
    method: string;
    steps: PlanStep[];
    timeline: string;
  };
  missing_elements: string[];
  simplified_version: string;
  actionable_steps: string[];
}

export interface AnalyzePlanResult extends AnalyzePlanResponse {
  original_idea: string;
}
