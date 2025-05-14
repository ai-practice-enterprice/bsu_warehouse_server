#!/bin/bash

# YOU MIGHT HAVE TO CHANGE THIS FILE LINE ENDINGS FROM WINDOWS LINE ENDINGS (/r/n) to LINUX LINE ENDINGS (/n)
# normally i use "dos2unix" in the dockerfile to be sure but if you encounter some prombloms

# if problems with docker compose occur change the permissions of this file to exectubale rights

# https://prisma-client-py.readthedocs.io/en/stable/getting_started/quickstart/
# The db push command also generates the client for you. 
# If you want to generate the client without modifying your database, use the following command: prisma generate --watch
# Generate Prisma client
prisma generate

# Push changes to DB
# https://www.prisma.io/docs/orm/prisma-migrate/workflows/prototyping-your-schema#choosing-db-push-or-prisma-migrate
prisma db push

# This command tells ARQ to load the configuration from ArqWorker.py's WorkerSettings class 
# and start listening for jobs on the default Redis queue.
arq arq_worker.ArqWorker.WorkerSettings --watch ./arq_worker &

# remove "--reload" in production because uvicorn will ignore the "--workers" argument then
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --workers 4
    