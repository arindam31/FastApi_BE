# Mongo db useful tips and commands

Mongo db has been used here to save multiple configs

To access it on container, use below (service name is mongo as per docker compose file):

### Example of adding a JSON document
```bash
docker exec -it mongo mongosh
```

```mongosh
use backend_config
db.configs.insertOne({
  env: "dev",
  users_url: "http://users:5000",
  orders_url: "http://orders:5001",
  logging_level: "INFO"
})
```