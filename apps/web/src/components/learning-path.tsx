import type { LearningPathStep } from "@learn-it/shared";
import { ArrowRight, Clock, Target } from "lucide-react";

interface LearningPathProps {
  steps: LearningPathStep[];
}

export function LearningPath({ steps }: LearningPathProps) {
  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-surface" aria-labelledby="learning-path-title">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-medium uppercase tracking-normal text-clay">Current path</p>
          <h2 id="learning-path-title" className="mt-1 text-xl font-semibold text-ink">
            Diagnose before teaching
          </h2>
        </div>
        <Target className="h-5 w-5 text-sea" aria-hidden="true" />
      </div>
      <div className="mt-5 grid gap-3">
        {steps.map((step, index) => (
          <article key={step.id} className="rounded-lg border border-line bg-panel p-4">
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="flex flex-wrap items-center gap-2 text-xs font-medium uppercase tracking-normal text-ink/60">
                  <span>{index + 1}</span>
                  <ArrowRight className="h-3 w-3" aria-hidden="true" />
                  <span>{step.stage}</span>
                </div>
                <h3 className="mt-2 text-base font-semibold text-ink">{step.title}</h3>
                <p className="mt-2 text-sm leading-6 text-ink/70">{step.learnerAction}</p>
              </div>
              <div className="flex shrink-0 items-center gap-1 rounded-md border border-line bg-white px-2 py-1 text-xs text-ink/70">
                <Clock className="h-3 w-3" aria-hidden="true" />
                {step.estimatedMinutes}m
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
