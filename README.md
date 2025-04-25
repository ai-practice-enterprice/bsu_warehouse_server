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
