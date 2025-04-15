# bsu_warehouse_setup
root repository to setup all the entities in our warehouse:
- Apache server (frontend)
- API server (backend)
  - FastAPI
  - ARQ
  - Prisma 
- ROS2 server (ROS2 <-> API server communication)
- MySQL server (database)
- Redis

The steps that you need to take in order for it all to work are explained inside the 
[Docker-Compose file](./docker-compose.yaml)

# clone repositories
Because currently this repository uses git submodules you'll have to run the command
```
cd bsu_warehouse_server
git submodule update --init --recursive
```
