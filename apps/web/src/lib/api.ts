import type { ConceptEdge, ConceptNode, DashboardSnapshot, LearningPathStep } from "@learn-it/shared";
import { sampleDashboard } from "./sample-dashboard";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

type ApiConcept = {
  id: string;
  label: string;
  depth: ConceptNode["depth"];
  status: ConceptNode["status"];
  retrieval_health: number;
  next_review_at: string;
};

type ApiPathStep = {
  id: string;
  concept_id: string;
  stage: LearningPathStep["stage"];
  title: string;
  learner_action: string;
  estimated_minutes: number;
};

type ApiDashboard = {
  understanding_score: number;
  concepts_mastered_this_week: number;
  retention_rate: number;
  implementation_completion: number;
  active_source?: SourceSummary;
  concepts: ApiConcept[];
  edges: ConceptEdge[];
  path: ApiPathStep[];
};

export type SourceSummary = {
  id: string;
  title: string;
  filename: string;
  content_type: string;
  summary: string;
  created_at?: string;
  concept_count: number;
  chunk_count: number;
};

export type LiveDashboardSnapshot = DashboardSnapshot & {
  activeSource?: SourceSummary;
};

export async function getDashboard(): Promise<LiveDashboardSnapshot> {
  try {
    const response = await fetch(`${API_URL}/dashboard`, { cache: "no-store" });
    if (!response.ok) {
      return sampleDashboard;
    }
    const payload = (await response.json()) as ApiDashboard;
    return mapDashboard(payload);
  } catch {
    return sampleDashboard;
  }
}

export async function getSources(): Promise<SourceSummary[]> {
  try {
    const response = await fetch(`${API_URL}/sources`, { cache: "no-store" });
    if (!response.ok) {
      return [];
    }
    return (await response.json()) as SourceSummary[];
  } catch {
    return [];
  }
}

export function getApiUrl(): string {
  return API_URL;
}

function mapDashboard(payload: ApiDashboard): LiveDashboardSnapshot {
  return {
    understandingScore: payload.understanding_score,
    conceptsMasteredThisWeek: payload.concepts_mastered_this_week,
    retentionRate: payload.retention_rate,
    implementationCompletion: payload.implementation_completion,
    activeSource: payload.active_source,
    concepts: payload.concepts.map(mapConcept),
    edges: payload.edges,
    path: payload.path.map(mapPathStep),
  };
}

function mapConcept(concept: ApiConcept): ConceptNode {
  return {
    id: concept.id,
    label: concept.label,
    depth: concept.depth,
    status: concept.status,
    retrievalHealth: concept.retrieval_health,
    nextReviewAt: concept.next_review_at,
  };
}

function mapPathStep(step: ApiPathStep): LearningPathStep {
  return {
    id: step.id,
    conceptId: step.concept_id,
    stage: step.stage,
    title: step.title,
    learnerAction: step.learner_action,
    estimatedMinutes: step.estimated_minutes,
  };
}
