# 🔍 Network Monitoring Tool

A lightweight Python-based network monitoring tool that continuously scans your local subnet using `nmap`, logs the status of connected devices, tracks online/offline timestamps, and saves the results in a structured CSV log.

## 📌 Features

- 🔄 Real-time device monitoring with automatic scans every 10 seconds
- 🖥️ Captures Hostname, IP Address, MAC Address, Status, and Response Time
- 📊 Logs online/offline transitions with accurate timestamps to `network_log.csv`
- 💡 Supports both Windows and Linux environments
- 📁 Automatically creates CSV file if it doesn't exist

---

## 🚀 How It Works

1. Scans your subnet (e.g., `192.168.1.0/24`) using `nmap`
2. Pings each active device to verify connectivity and response time
3. Records new devices and status changes (online/offline) in a CSV log
4. Keeps running until manually stopped (Ctrl+C)

---

## 📂 Project Structure

```
./
├── network_scanner.py      # Main monitoring script
├── network_log.csv         # Log file (generated on first run)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🧰 Requirements

- Python 3.6+
- Nmap installed on your system
- Required Python packages:

Install dependencies using:

```bash
pip install -r requirements.txt
```

> Note: On Linux, you may need to install `nmap` using `sudo apt install nmap`.

---

## 🛠️ Configuration

Before running, update the `subnet` variable in `network_scanner.py` with your local subnet range:

```python
subnet = '192.168.1.0/24'  # Replace with your subnet
```

You can find your subnet using:

- On Windows: `ipconfig`
- On Linux/macOS: `ifconfig` or `ip a`

---

## ▶️ Usage

Run the monitoring script:

```bash
python network_scanner.py
```

To stop monitoring, press `Ctrl + C`.

---

## 📈 Output

The output log is saved in `network_log.csv` with the following columns:

- **Hostname**
- **IP Address**
- **MAC Address**
- **IP Added Time**
- **Status** (`Connected` / `Failed`)
- **Response Time (ms)**
- **Offline At** (timestamp when device went offline)

---

## 📸 Sample CSV Row

```csv
Device1,192.168.1.15,00:1A:2B:3C:4D:5E,2025-06-17 10:20:35,Connected,5.32,
```

---

## 📜 License

This project is licensed under the MIT License. Feel free to modify and use it for personal or commercial purposes.

---

## 👨‍💻 Author

Developed with ❤️ by Mayank Aggarwal  
[GitHub Profile](https://github.com/Er-Mayank-Aggarwal)

---

## 🌐 Contributions

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.