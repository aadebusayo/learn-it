FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY packages/agents /app/packages/agents
COPY packages/graph /app/packages/graph
COPY apps/api /app/apps/api
RUN pip install --no-cache-dir -e /app/packages/agents -e /app/packages/graph -e /app/apps/api
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
