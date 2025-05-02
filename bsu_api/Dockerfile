FROM python:3.13-slim AS builder
WORKDIR /app

# we install nodejs so that we can run prisma studio (a GUI) for having interface to the DB
RUN apt-get update && apt-get install -y \
    libzbar0 \
    nodejs \
    npm && \
    rm -rf /var/lib/apt/lists/*

COPY . .
RUN chmod 777 ./entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["/bin/sh","entrypoint.sh" ]
