# Table of Contents
- [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Frontend](#frontend)
    - [Backend](#backend)
    - [Load Balancing \& Rate Limiting](#load-balancing--rate-limiting)
    - [Database Architecture](#database-architecture)
  - [How to run](#how-to-run)
  - [Notes](#notes)
  - [Additional Considerations](#additional-considerations)


## Overview
This project is a URL shortener system that enables users to create shortened URLs and view analytics for their usage. It features a React-based frontend, a Python-Flask backend, and a robust infrastructure designed for scalability and reliability.


### Frontend
- React based application with 2 components
  - URL Shortener: Handles URL creation and shortening functionalities.
  ![alt text](Shorten.png)
  - URL Stats: Provides analytics and statistics for shortened URLs.
  ![alt text](Stats.png)

### Backend
- API Integration: The Flask API powers all frontend functionalities.
- Deployment: The backend leverages Gunicorn for scalability and enhanced performance.
- A `run_local.sh` script is provided for local testing and debugging purposes.

### Load Balancing & Rate Limiting
- Reverse Proxy: NGINX acts as a reverse proxy, routing requests to the URL-shortening service.
- Rate Limiting: Configured within NGINX to mitigate DoS attacks and ensure system reliability under load

### Database Architecture
- Redis (Caching): Writes are first made to Redis for faster response times.
- MongoDB (Primary Storage): Data is eventually written to MongoDB, allowing for eventual consistency.
- Document Locking: MongoDB uses document-level locks, enabling high-concurrency writes.
- Schema: URL info and statistics are stored together in a single document for efficient retrieval.

## How to run
- Ensure `WORK_DIR` and `ENV_DIR` environment variables are set to their absolute paths
- Backend config:
  - Rename `settings-copy.py` to `settings.py`
  - Update your MongoDb and Redis credentials in this file
- Frontend config:
  - Rename `.env.copy` to `.env`.
  - Set the backend API endpoint for the shortening service in REACT_APP_SHORTEN_ENDPOINT. If the frontend and backend are served from the same domain, you can set this to the root path (e.g., `/api`).
  
## Notes
- The frontend and backend build and deployment scripts are combined for simplicity. If needed, they can be separated.
- The tool is currently accessible via the server's IP address due to the lack of DNS configuration.
- SSL/TLS is not configured in this deployment, so the Copy to Clipboard functionality may not work on non-local environments. This feature can be fully tested on localhost.

## Additional Considerations
- Scalability: The system leverages caching, document-level locks, and a reverse proxy to handle high traffic.
- Security: Rate limiting and NGINX configuration mitigate common attack vectors.
- Future Enhancements:
  - DNS and SSL setup for better accessibility and security.
  - Separate build scripts for frontend and backend for more streamlined CI/CD workflows.