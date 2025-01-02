# Frontend
- React based application with 2 components
  - URL Shortener: Handles URL creation and shortening functionalities.
  ![alt text](Shorten.png)
  - URL Stats: Provides analytics and statistics for shortened URLs.
  ![alt text](Stats.png)
# Backend
- Python-Flask based API that is utilised by the frontend client.
- The backend is deployed on AWS using Gunicorn to ensure scalability and enhanced performance
- A `run_local.sh` script is provided for local testing and debugging purposes.

# Load Balancing & Rate Limiting
- Reverse Proxy: NGINX is used as a reverse proxy to route requests to the URL-shortening services.
- Rate Limiting: Configured within NGINX to mitigate DoS attacks and ensure system reliability under load

# Database (NoSQL)
- Locks in MongoDB are at document level which enables high volume of concurrent writes.
- URL Info and stats are contained within the same document.

# Notes
- Frontend and backend build/deploy scripts for the frontend and backend can be separated if needed, though they remain combined for simplicity in this assignment.
- Deployed tool is accessed via the server's IP address due to the absence of DNS configuration.
- Since the deployment is not via a DNS and SSL Security, the copyToClipboard functionality won't work. It can be tested on localhost.