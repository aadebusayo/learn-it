export type LearningStage =
  | "discover"
  | "diagnose"
  | "learn"
  | "apply"
  | "explain"
  | "challenge"
  | "retain";

export type KnowledgeDepth = 0 | 1 | 2 | 3 | 4 | 5;

export type ConceptStatus = "strong" | "developing" | "weak" | "missing";

export interface ConceptNode {
  id: string;
  label: string;
  depth: KnowledgeDepth;
  status: ConceptStatus;
  retrievalHealth: number;
  nextReviewAt: string;
}

export interface ConceptEdge {
  source: string;
  target: string;
  relation: "prerequisite" | "supports" | "contrasts" | "implements";
  confidence: number;
}

export interface LearningPathStep {
  id: string;
  conceptId: string;
  stage: LearningStage;
  title: string;
  learnerAction: string;
  estimatedMinutes: number;
}

export interface DashboardSnapshot {
  understandingScore: number;
  conceptsMasteredThisWeek: number;
  retentionRate: number;
  implementationCompletion: number;
  concepts: ConceptNode[];
  edges: ConceptEdge[];
  path: LearningPathStep[];
}
