import { ConceptGraph } from "@/components/concept-graph";
import { LearningPath } from "@/components/learning-path";
import { MetricStrip } from "@/components/metric-strip";
import { sampleDashboard } from "@/lib/sample-dashboard";
import { BookOpen, FileUp, SearchCheck } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#fbfaf6] text-ink">
      <header className="border-b border-line bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-5 px-5 py-6 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm font-medium uppercase tracking-normal text-sea">Learn It</p>
            <h1 className="mt-2 text-3xl font-semibold text-ink md:text-4xl">Deliberate learning workspace</h1>
            <p className="mt-3 max-w-3xl text-base leading-7 text-ink/70">
              Transform dense material into prerequisite graphs, active recall, implementation work, teach-back, and retention.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <button className="inline-flex items-center gap-2 rounded-md bg-ink px-4 py-2 text-sm font-medium text-white" type="button">
              <FileUp className="h-4 w-4" aria-hidden="true" />
              Upload source
            </button>
            <button className="inline-flex items-center gap-2 rounded-md border border-line bg-white px-4 py-2 text-sm font-medium text-ink" type="button">
              <SearchCheck className="h-4 w-4" aria-hidden="true" />
              Run diagnosis
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-6 px-5 py-6">
        <MetricStrip
          understandingScore={sampleDashboard.understandingScore}
          conceptsMasteredThisWeek={sampleDashboard.conceptsMasteredThisWeek}
          retentionRate={sampleDashboard.retentionRate}
          implementationCompletion={sampleDashboard.implementationCompletion}
        />

        <section className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_390px]">
          <div className="rounded-lg border border-line bg-white p-5 shadow-surface">
            <div className="mb-4 flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-medium uppercase tracking-normal text-clay">Knowledge graph</p>
                <h2 className="mt-1 text-xl font-semibold text-ink">Attention prerequisites</h2>
              </div>
              <BookOpen className="h-5 w-5 text-sea" aria-hidden="true" />
            </div>
            <ConceptGraph concepts={sampleDashboard.concepts} edges={sampleDashboard.edges} />
          </div>

          <LearningPath steps={sampleDashboard.path} />
        </section>
      </div>
    </main>
  );
}
