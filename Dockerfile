# Estágio de Build Otimizado
FROM python:3.11-slim AS base
LABEL authors="edilson-barreto"

# Configurações de Ambiente
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Instala ferramentas de sistema necessárias (Postgres e compilação)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

# Configura o diretório de trabalho
WORKDIR /usr/src/app

# Cria e alterna para um usuário não-root (Segurança)
RUN useradd -ms /bin/bash appuser
USER appuser

# Copia apenas o diretório src/ (sem instalar nada)
COPY src/ /usr/src/app

# Instala as dependências como root (permissões necessárias)
USER root
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Volta para o usuário não-root
USER appuser
# Comando Padrão: Apenas aguarda comandos externos
CMD ["tail", "-f", "/dev/null"]