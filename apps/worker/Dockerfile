FROM python:3.13.11-alpine3.22
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY packages/agents /app/packages/agents
COPY packages/graph /app/packages/graph
COPY apps/worker /app/apps/worker
RUN pip install --no-cache-dir -e /app/packages/agents -e /app/packages/graph -e /app/apps/worker
CMD ["python", "-m", "worker.main"]
