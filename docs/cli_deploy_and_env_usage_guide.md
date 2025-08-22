# Usage guidelines for deploying to staging environment (e.g demo, prod, testing etc)

## Supported Environments

| Environment | Description                 |
|------------|-----------------------------|
| `dev`      | Local development           |
| `demo`     | Demo/staging for presentations |
| `prod`     | Production                  |
| `testing`  | QA / automated testing      |

---

## Prerequisites

1. Python virtual environment is activated.
2. MongoDB is running and accessible.
3. The CLI scripts are available in the backend/cli folder.
4. For some, User credentials with appropriate permissions are needed (e.g to deploy)

---

## CLI Commands

### 1. Deploy on a platform

Authorized users can deploy working branch on any server.
**Command**
```bash
python -m cli.deploy dev
```

### 2. Find envirinments to deploy

If you are not sure what staging envs are available, you can list them
**Command**
```bash
python -m cli.manage_envs list-env
```

### 2. Other operations

You can add, remove or edit envs
**Command**
```bash
python -m cli.manage_envs list-env
{
  "env": "dev",
  "users_url": "http://users:5000",
  "orders_url": "http://orders:5001",
  "logging_level": "INFO"
}
```

### **For adding**:

If using powershell on Windows
```powershell
python -m cli.manage_envs create-env --env staging --server-ip 192.168.0.50 --users-url http://users-staging:5000 --orders-url http://orders-staging:5001 --logging-level DEBUG

Created new config for env=demo
{
  "env": "staging",
  "server_ip": "192.168.0.50",
  "users_url": "http://users-staging:5000",
  "orders_url": "http://orders-staging:5001",
  "logging_level": "DEBUG",
  "feature_flags": {
    "enable_api": true
  }
}
```

### **For updating a field**:
```powershell
(.venv) PS C:\Projects\Infra_Microservice_Demo\FastApi_BE\backend> python -m cli.manage_envs edit-env --env dev --field servep_ip --value 127.0.0.1
Updated env=dev
{
  "env": "dev",
  "users_url": "http://users:5000",
  "orders_url": "http://orders:5001",
  "logging_level": "INFO",
  "servep_ip": "127.0.0.1"
}
```