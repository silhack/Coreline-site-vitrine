# ── Build / deps stage ─────────────────────────────────────
FROM python:3.12-alpine AS builder

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Production stage ────────────────────────────────────────
FROM python:3.12-alpine

WORKDIR /app

# ✅ Non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# ✅ Copy only installed packages from builder
COPY --from=builder /install /usr/local

# ✅ Copy app source
COPY --chown=appuser:appgroup . .

# ✅ No write access to source
RUN chmod -R 550 /app

USER appuser

EXPOSE 8000

# ✅ Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:8000/health || exit 1

# ✅ Gunicorn + Uvicorn workers (not uvicorn alone)
CMD ["gunicorn", "main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "2", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "30", \
     "--forwarded-allow-ips", "*"]
