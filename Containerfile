# Minimal runtime image; dependencies are installed before source to improve build caching.
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home appuser && mkdir -p /data && chown -R appuser:appuser /app /data
COPY --chown=appuser:appuser app ./app
COPY --chown=appuser:appuser ml ./ml
COPY --chown=appuser:appuser artifacts ./artifacts
USER appuser
VOLUME /data
EXPOSE 5000
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 'app:create_app()'"]
