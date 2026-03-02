# Usamos uma imagem oficial e leve do Python
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Instala as dependências, fontconfig, e as fontes
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libffi-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    fontconfig \
    fonts-noto-color-emoji \
    fonts-hack \
    fonts-liberation \
    fonts-dejavu \
    && fc-cache -f -v \
    && rm -rf /var/lib/apt/lists/*  && rm -rf /var/lib/apt/lists/*
# Instala os pacotes Python
RUN pip install --no-cache-dir Markdown WeasyPrint Pygments

WORKDIR /workspace

# Copia o novo script Python
COPY entrypoint.py /usr/local/bin/entrypoint.py
RUN chmod +x /usr/local/bin/entrypoint.py

# Configura o script Python como comando padrão
ENTRYPOINT ["/usr/local/bin/entrypoint.py"]
