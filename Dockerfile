# Stage 1: Build Frontend
FROM node:18 AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY code/frontend/web/web-2048-frontend/package*.json ./

# Install frontend dependencies
RUN npm install

# Copy frontend source code
COPY code/frontend/web/web-2048-frontend/ ./

# Build the frontend
RUN npm run build

# Stage 2: Build Backend
FROM python:3.12-slim AS backend-builder

WORKDIR /app/backend

# Install backend dependencies
COPY code/backend/dist/game_backend-0.1.2-py3-none-any.whl ./
RUN pip install --no-cache-dir game_backend-0.1.2-py3-none-any.whl

# Stage 3: Combine and Run
FROM python:3.12-slim

WORKDIR /app

# Copy backend from backend-builder
COPY --from=backend-builder /app/backend /app/backend

# Install the backend package in the final image
RUN pip install --no-cache-dir /app/backend/game_backend-0.1.2-py3-none-any.whl

# Copy frontend build from frontend-builder
COPY --from=frontend-builder /app/frontend/dist /app/frontend/build

# Expose port 8000
EXPOSE 8000

# Environment variables
ENV PYTHONUNBUFFERED=1

# Set entry point to run the backend module
CMD ["python3", "-m", "game_backend"]