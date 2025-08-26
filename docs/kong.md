# Integrating Kong as an API gateway

Kong will proxy traffic to Services. Clients will talk to Kong.
Kong will forward to our services.
The "backend" service will act as an aggregator.

Kong can take over the gateway responsibilities:

- Routing (/users → users service, /orders → orders service)
- Security (JWT, OIDC, API key, mTLS, RBAC)
- Cross-cutting concerns (rate limiting, CORS, logging, monitoring, retries, caching, etc.)

How it looks:
```bash
Client → Kong (/api/profile/123) → backend service
                                 → users + orders
```

## Testing Gateway via kong
```psh
(.venv) PS C:\Projects\Infra_Microservice_Demo\FastApi_BE> curl http://localhost:8000/api/profile/1


StatusCode        : 200
StatusDescription : OK
Content           : {"user":{"id":1,"name":"Adam","email":"adame@example.com"},"orders":[{"orderId":101,"userId":1,"total":49.99},{"orderId":10 
                    2,"userId":1,"total":19.99}]}
RawContent        : HTTP/1.1 200 OK
                    Connection: keep-alive
                    X-Kong-Upstream-Latency: 63
                    X-Kong-Proxy-Latency: 3962
                    X-Kong-Request-Id: 733eee785841d72cd9859e1adf7b8f17
                    Content-Length: 152
                    Content-Type: application/js...
Forms             : {}
Headers           : {[Connection, keep-alive], [X-Kong-Upstream-Latency, 63], [X-Kong-Proxy-Latency, 3962], [X-Kong-Request-Id,
                    733eee785841d72cd9859e1adf7b8f17]...}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : System.__ComObject
RawContentLength  : 152
```

In real setup, services would be available in different [IPs:Ports]. And our backend will server between kong and these
services.
This is how we could enlist them in a kong.yml file.

```yml
_format_version: "3.0"

services:
  # Backend aggregator (your FastAPI)
  - name: backend-service
    url: http://backend:8080
    routes:
      - name: backend-route
        paths:
          - /api
        
  # Optional: direct access to microservices (internal)
  - name: users-service
    url: http://10.0.1.5:5000
    routes:
      - name: users-route
        paths:
          - /_internal/users

  - name: orders-service
    url: http://10.0.1.5:5001
    routes:
      - name: orders-route
        paths:
          - /_internal/orders

  - name: payments-service
    url: http://10.0.1.5:5002
    routes:
      - name: payments-route
        paths:
          - /_internal/payments
```