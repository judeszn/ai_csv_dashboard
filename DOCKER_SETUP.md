# Docker Setup for AI CSV Dashboard

This guide explains how to run the AI CSV Dashboard using Docker for a simplified and more reliable deployment.

## Why Docker?

Docker offers significant advantages for running this application:

1. **Consistency**: Same environment across all systems
2. **Isolation**: No conflicts with other applications or system libraries
3. **Simplified Dependencies**: All requirements are packaged inside containers
4. **Port Management**: Avoids port conflicts that you experienced
5. **Easy Distribution**: Share the application easily with colleagues
6. **Security**: Services run in isolated containers
7. **Version Control**: Easy to specify and update exact versions of dependencies

## Prerequisites

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) for Windows
2. Make sure your Google API key is available

## Quick Start

### 1. Set Up Environment Variables

Create or update your `.env` file in the project root directory:

```
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

### 2. Start the Application

Open a terminal in your project directory and run:

```bash
docker-compose up
```

This will:
- Build the backend and frontend containers
- Start both services
- Connect them in a private network
- Map the necessary ports

### 3. Access the Application

Open your browser and go to:
- Frontend: http://localhost:8501

### 4. Stop the Application

To stop the application, press `Ctrl+C` in the terminal, or run:

```bash
docker-compose down
```

## Troubleshooting Docker Setup

### Common Issues and Solutions

1. **Port conflicts**:
   - The Docker Compose file maps ports 8005->8000 for backend and 8501->8501 for frontend
   - If you still have conflicts, edit the first number in the port mappings in docker-compose.yml

2. **Container fails to start**:
   - Check logs with: `docker-compose logs backend` or `docker-compose logs frontend`
   - Ensure your `.env` file contains a valid GOOGLE_API_KEY

3. **Changes not reflected**:
   - Rebuild containers with: `docker-compose up --build`

4. **Resource issues**:
   - Increase memory/CPU allocation in Docker Desktop settings

## Advanced Docker Configuration

### Running in Background

To run containers in the background:

```bash
docker-compose up -d
```

### Viewing Logs

To see container logs:

```bash
docker-compose logs -f
```

### Rebuilding Containers

If you make code changes:

```bash
docker-compose up --build
```

### Cleaning Up

To remove containers and networks:

```bash
docker-compose down
```

To also remove built images:

```bash
docker-compose down --rmi local
```

## Docker Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/)
