FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app

# Copy app
COPY . .

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["uv", "run", "gunicorn", "-w", "2", "-k", "gthread", "--threads", "4", "-b", "0.0.0.0:5000", "main:app"]
