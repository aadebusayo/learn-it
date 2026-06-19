import { Brain, Code2, Network, Repeat } from "lucide-react";

interface MetricStripProps {
  understandingScore: number;
  conceptsMasteredThisWeek: number;
  retentionRate: number;
  implementationCompletion: number;
}

const metrics = [
  { key: "understandingScore", label: "Understanding", icon: Brain, suffix: "%" },
  { key: "conceptsMasteredThisWeek", label: "Deepened this week", icon: Network, suffix: "" },
  { key: "retentionRate", label: "Retention", icon: Repeat, suffix: "%" },
  { key: "implementationCompletion", label: "Implementation", icon: Code2, suffix: "%" },
] as const;

export function MetricStrip(props: MetricStripProps) {
  return (
    <section className="grid gap-3 md:grid-cols-4" aria-label="Learning metrics">
      {metrics.map(({ key, label, icon: Icon, suffix }) => (
        <article key={key} className="rounded-lg border border-line bg-white px-4 py-4 shadow-surface">
          <div className="flex items-center justify-between gap-3">
            <span className="text-sm text-ink/65">{label}</span>
            <Icon className="h-4 w-4 text-sea" aria-hidden="true" />
          </div>
          <p className="mt-3 text-3xl font-semibold text-ink">
            {props[key]}
            {suffix}
          </p>
        </article>
      ))}
    </section>
  );
}
