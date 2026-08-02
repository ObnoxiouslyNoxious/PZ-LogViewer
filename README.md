# PZ Log Viewer

[![Latest Release](https://img.shields.io/github/v/release/ObnoxiouslyNoxious/PZ-LogViewer)](https://github.com/ObnoxiouslyNoxious/PZ-LogViewer/releases/latest)

A real-time log viewer for Project Zomboid client/server logs. Displays both client and server logs side-by-side with syntax highlighting for errors, warnings, and stack traces.

## Features

- **Real-time updates** — Auto-refreshes every 0.5 seconds
- **Dual-panel view** — Client log and server log side by side
- **Syntax highlighting** — Errors in yellow, stack traces in red
- **Resizable panels** — Drag the divider to adjust panel widths
- **Auto-scroll** — Automatically scrolls to bottom on new content

## Requirements

- Python 3.x (no external packages required)
- A web browser (Chrome, Edge, Firefox, etc.)
- Project Zomboid dedicated server logs

## Setup

1. **Download** — Clone or download this repository:
   ```
   git clone https://github.com/ObnoxiouslyNoxious/PZ-LogViewer.git
   ```
   Or download the ZIP from GitHub and extract it.

2. **Edit `config.json`** and set `logsDir` to your Zomboid Logs folder:

```json
{
    "version": "1.0.0",
    "logsDir": "SET_FILEPATH_HERE",
    "host": "127.0.0.1",
    "port": 8080
}
```

Common log locations:
- **Windows:** `C:\Users\<YourName>\Zomboid\Logs`
- **Linux:** `~/.zomboid/Logs`

2, **Run `start.bat`** (Windows) or execute:
   ```
   python server.py
   ```

3, **Open your browser** to `http://127.0.0.1:8080`

## Usage

| Button | Action |
|--------|--------|
| **Auto** | Toggle auto-refresh on/off |
| **Refresh** | Manually refresh logs |
| **STOP LOGGING** | Shut down the Python server |

## Configuration

Edit `config.json` to change settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `version` | `1.0.0` | Log Viewer version |
| `logsDir` | `SET_FILEPATH_HERE` | Path to your Zomboid Logs folder |
| `host` | `127.0.0.1` | Server bind address |
| `port` | `8080` | Server port |

## Notes

- The viewer reads the most recent log files matching `*_DebugLog.txt` (client) and `*_DebugLog-server.txt` (server)
- Logs are read from disk on each refresh. No files are modified
- The server runs on `127.0.0.1` (localhost) by default. It is not accessible from other devices on your network or the internet. No data is transferred externally. Everything stays on your machine.