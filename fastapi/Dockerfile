FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app

# Copy app
COPY . .

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
