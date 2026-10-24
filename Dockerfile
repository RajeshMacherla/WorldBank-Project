FROM python:3.12-slim
WORKDIR /app
COPY app ./app
COPY data ./data
RUN useradd --create-home assistant && chown -R assistant:assistant /app
USER assistant
# Server intentionally binds loopback. For a container demo use host networking on Linux.
CMD ["python", "-m", "app.server"]
