# 📲 Flask File & Folder Receiver

A simple Flask server that receives files and folders from a remote client (e.g. a PC) and saves them to the local directory on your Android phone or any other device.

---

## 🔧 Features

- ✅ Accept file uploads via `POST /upload`
- 📁 Create folders via `POST /create-folder`
- 💾 Saves files inside a `received_files/` folder (created automatically)
- 🔒 Minimal setup and no external dependencies required

---

## 🚀 How to Run

1. Install Flask (if you haven't):
   ```bash
   pip install flask
