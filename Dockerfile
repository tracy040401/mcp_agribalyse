# Étape 1 : Builder avec uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# Permet la compilation des .pyc et évite les liens symboliques
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Installer uniquement les dépendances à partir des fichiers de lock
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Ajouter le code de l’application et installer le projet lui-même
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# Étape 2 : image finale, minimaliste
FROM python:3.12-slim-bookworm

# Installer git pour potentiels accès à des dépendances via git+
# Installer git + Node.js + npm + autres outils requis
RUN apt-get update && apt-get install -y \
    git \
    curl \
    python3-venv \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier l’environnement installé depuis le builder
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder /app /app

# Ajouter le venv dans le PATH
ENV PATH="/app/.venv/bin:$PATH"

RUN pip install uv

EXPOSE 6274
EXPOSE 6277

# Entrée du conteneur
ENTRYPOINT ["mcp", "dev", "server/server.py"]
