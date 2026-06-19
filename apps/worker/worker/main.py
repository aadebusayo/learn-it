from learning_graph.models import sample_learning_path


def main() -> None:
    print("Learn It worker ready")
    print("Planned background jobs:")
    print("- ingest_uploaded_sources")
    print("- extract_concept_graph")
    print("- generate_active_recall")
    print("- schedule_retention_reviews")
    print("Current seed path:")
    for step in sample_learning_path():
        print(f"- {step.stage.value}: {step.title}")


if __name__ == "__main__":
    main()
