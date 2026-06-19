import type { SourceSummary } from "@learn-it/shared";
import { Files } from "lucide-react";

interface SourceListProps {
  sources: SourceSummary[];
}

export function SourceList({ sources }: SourceListProps) {
  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-surface" aria-labelledby="sources-title">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-medium uppercase tracking-normal text-plum">Sources</p>
          <h2 id="sources-title" className="mt-1 text-xl font-semibold text-ink">
            Ingested material
          </h2>
        </div>
        <Files className="h-5 w-5 text-sea" aria-hidden="true" />
      </div>
      <div className="mt-5 grid gap-3">
        {sources.length === 0 ? (
          <p className="rounded-lg border border-dashed border-line bg-panel p-4 text-sm leading-6 text-ink/70">
            Upload a Markdown, text, or PDF source to create a durable learning graph.
          </p>
        ) : (
          sources.map((source) => (
            <article key={source.id} className="rounded-lg border border-line bg-panel p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="text-base font-semibold text-ink">{source.title}</h3>
                  <p className="mt-1 text-sm leading-6 text-ink/70">{source.summary}</p>
                </div>
                <div className="shrink-0 rounded-md border border-line bg-white px-2 py-1 text-xs text-ink/70">
                  {source.concept_count} concepts
                </div>
              </div>
            </article>
          ))
        )}
      </div>
    </section>
  );
}
