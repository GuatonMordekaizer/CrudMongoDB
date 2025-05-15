FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Santiago \
    PATH="/opt/venv/bin:$PATH"

# 1) Instala Python, venv y herramientas mínimas
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      python3 python3-venv python3-pip \
      vim curl git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) Crea un venv en /opt/venv e instala ahí las dependencias
RUN python3 -m venv /opt/venv && \
    pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copia el código
COPY src/ ./src/

EXPOSE 5000

# 4) Al arrancar, corre tests y luego la aplicación
ENTRYPOINT ["bash", "-c", "pytest --maxfail=1 --disable-warnings -q && exec python3 src/main.py"]