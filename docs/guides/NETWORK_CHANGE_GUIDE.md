# Network Change Guide 🌐

This guide explains how to update the project configuration when your network IP address changes (e.g., moving from home to school Wi-Fi).

## 1. Find Your New IP Address
1. Open a new terminal.
2. Run the following command:
   ```cmd
   ipconfig
   ```
3. Look for **IPv4 Address** under your active connection (Wi-Fi or Ethernet).
   * Example: `192.168.0.190` or `10.0.11.154`

---

## 2. Update Configuration Files

You need to update **2 files** with your new IP address.

### File 1: Frontend Config (`Vue/.env`)
This tells the frontend where to find the backend API.

1. Open `Vue/.env`.
2. Update `VITE_API_BASE_URL` with your new IP.
3. Update `VITE_RASA_URL` with your new IP.

```dotenv
# Example: If new IP is 192.168.1.50
VITE_API_BASE_URL=http://192.168.1.50:8000/api
VITE_RASA_URL=http://192.168.1.50:5005
```

### File 2: Backend Config (`Django/.env`)
This allows the backend to accept connections from your new IP.

1. Open `Django/.env`.
2. Update `DJANGO_ALLOWED_HOSTS` (comma-separated list).
3. Update `CORS_ALLOWED_ORIGINS` (list of full URLs).

```dotenv
# Example: If new IP is 192.168.1.50
DJANGO_ALLOWED_HOSTS=192.168.1.50,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://192.168.1.50:5173,http://localhost:5173,http://127.0.0.1:5173
```

> **Note:** Ideally, keep `localhost` and `127.0.0.1` in the lists so it still works locally.

---

## 3. Restart Servers with Correct Flags

To make the system accessible from other devices (like your phone), use these startup commands.

### Terminal 1: Django (Backend)
Use `0.0.0.0:8000` to listen on all network interfaces.
```bash
cd Django
python manage.py runserver 0.0.0.0:8000
```

### Terminal 2: Vue (Frontend)
Use `--host` to expose the frontend server.
```bash
cd Vue
npm run dev -- --host
```

### Terminal 3: Rasa (Chatbot - Optional)
Ensure CORS is enabled.
```bash
cd Rasa
rasa run --enable-api --cors "*"
```

---

## checklist for Network Change
- [ ] Run `ipconfig` to get new IP.
- [ ] Update `Vue/.env`.
- [ ] Update `Django/.env`.
- [ ] Restart Django with `0.0.0.0:8000`.
- [ ] Restart Vue with `--host`.
