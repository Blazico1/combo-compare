# Production deployment notes

This file documents a simple, reproducible local production deployment using Docker.

Build and run locally (Docker required):

1. Build and start the services:

```bash
docker-compose build --pull
docker-compose up -d
```

2. The frontend will be available at: http://localhost:5173
   The backend API will be available at: http://localhost:8000

Notes:
- The backend reads `ALLOWED_ORIGINS` from the environment. The docker-compose file sets it to `http://localhost:5173` by default.
- The backend will serve the built frontend if `frontend/dist` is present (useful if you prefer serving static files from backend directly).
- For production, consider adding TLS termination (nginx/traefik) and a process manager for uvicorn (Gunicorn+UvicornWorker).

VPS deployment checklist
1. Copy the stats files to the server
   - Place your `kartParam.bin` and `driverParam.bin` files into the `backend/` directory in the repository on the VPS, alongside `main.py`. If you use limitless variants, also copy `limitless_kartParam.bin` and `limitless_driverParam.bin`.
   - These files must be present inside the backend container at runtime for the API to report healthy and to return vehicle/character lists.

2. Configure environment
   - Create a `.env` file on the VPS (keep it out of git) and set the variables from `.env.example`.
     Example `.env`:
     ```ini
     ALLOWED_ORIGINS=https://your-frontend.example.com
     UVICORN_WORKERS=2
     LOG_LEVEL=INFO
     ```

3. Build and run with Docker Compose (recommended):
   ```bash
   docker-compose build --pull
   docker-compose up -d
   docker-compose logs -f
   ```

4. Verify the service
   - Health: `GET /api/health` should return `healthy` and `vanilla_loaded: true`.
   - Vehicles: `GET /api/vehicles?mode=vanilla` should return a non-empty list.

5. Configure TLS & reverse proxy
   - Use nginx, Traefik, or a managed platform to terminate TLS and proxy to the frontend/backend services.
   - Alternatively, deploy the frontend to Vercel/Netlify and point the backend to the correct origin.

6. Optional: create a systemd unit to ensure docker-compose starts on boot
   - Example unit (`/etc/systemd/system/combo-compare.service`):
     ```ini
     [Unit]
     Description=Combo Compare (docker-compose)
     After=docker.service

     [Service]
     Type=oneshot
     RemainAfterExit=yes
     WorkingDirectory=/opt/combo-compare  # set to where repo is checked out
     ExecStart=/usr/bin/docker-compose up -d
     ExecStop=/usr/bin/docker-compose down

     [Install]
     WantedBy=multi-user.target
     ```

Notes
- Keep your `.env` and stats binaries out of the repository; mount them or copy them onto the host before starting the containers.
- If you plan to scale the backend horizontally, prefer a shared storage for stats or bake them into your backend image at build time.

Next steps (recommended):
- Add pinned dependency versions in `backend/requirements.txt` for reproducible builds.
- Configure log aggregation and monitoring.
- Harden CORS and environment variables for production environments.
