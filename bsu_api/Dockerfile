FROM python:3.13-slim AS builder
WORKDIR /app

# we install nodejs so that we can run prisma studio (a GUI) for having interface to the DB
RUN apt-get update && apt-get install -y \
    libzbar0 \
    nodejs \
    dos2unix \
    npm && \
    rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN chmod +x /app/api-entrypoint.sh
RUN dos2unix /app/api-entrypoint.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "/app/api-entrypoint.sh" ]
# CMD ["/bin/bash","/app/api-entrypoint.sh" ]
