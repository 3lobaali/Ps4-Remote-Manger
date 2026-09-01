import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import socket
import json
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

# ==========================================
# 1. المتغيرات العامة
# ==========================================
local_server = None

# ==========================================
# 2. دوال الخلفية (Backend) لإرسال الألعاب PKG
# ==========================================
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class PkgServer(threading.Thread):
    def __init__(self, directory, port=8080):
        super().__init__()
        self.directory = directory
        self.port = port
        self.daemon = True
        self.server = None

    def run(self):
        os.chdir(self.directory)
        handler = SimpleHTTPRequestHandler
        self.server = HTTPServer(("", self.port), handler)
        print(f"[+] الخادم المحلي شغال على البورت {self.port}...")
        self.server.serve_forever()

def send_package_action():
    global local_server
    target_ip = ip_entry_pkg.get().strip()
    target_port = port_entry_pkg.get().strip()
    pkg_filepath = pkg_entry.get().strip()

    if not pkg_filepath:
        messagebox.showwarning("تنبيه", "الرجاء اختيار ملف PKG أولاً يا زول!")
        return

    pkg_dir = os.path.dirname(pkg_filepath)
    pkg_filename = os.path.basename(pkg_filepath)
    safe_filename = urllib.parse.quote(pkg_filename)

    pc_ip = get_local_ip()
    server_port = 8080

    if local_server is None:
        local_server = PkgServer(directory=pkg_dir, port=server_port)
        local_server.start()
    else:
        os.chdir(pkg_dir)

    download_url = f"http://{pc_ip}:{server_port}/{safe_filename}"
    data = {"type": "direct", "packages": [download_url]}
    json_data = json.dumps(data).encode('utf-8')

    ps4_url = f"http://{target_ip}:{target_port}/api/install"

    try:
        req = urllib.request.Request(ps4_url, data=json_data, headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req, timeout=5)
        result = json.loads(response.read().decode('utf-8'))

        if result.get("status") == "success":
            messagebox.showinfo("نجاح", "تم بدء تثبيت اللعبة على البلايستيشن!")
        else:
            messagebox.showerror("خطأ", f"رد البلايستيشن: {result}")

    except Exception as e:
        messagebox.showerror("فشل الاتصال", f"تأكد أن تطبيق Remote Package Installer مفتوح في الـ PS4.\nالتفاصيل: {e}")

# ==========================================
# 3. دوال الخلفية (Backend) لإرسال البايلود .bin
# ==========================================
def send_payload_action():
    target_ip = ip_entry_payload.get().strip()
    target_port = int(port_entry_payload.get().strip())
    payload_filepath = payload_entry.get().strip()

    if not payload_filepath:
        messagebox.showwarning("تنبيه", "الرجاء اختيار ملف البايلود (.bin) أولاً!")
        return

    try:
        with open(payload_filepath, 'rb') as file:
            payload_data = file.read()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((target_ip, target_port))
        sock.sendall(payload_data)
        sock.close()

        messagebox.showinfo("نجاح", "تم إرسال وحقن البايلود بنجاح!")
    except Exception as e:
        messagebox.showerror("فشل الاتصال", f"تم رفض الاتصال. تأكد من تفعيل Bin Loader في إعدادات GoldHEN.\nالتفاصيل: {e}")

# ==========================================
# 4. دوال التصفح (Browse)
# ==========================================
def browse_pkg():
    filename = filedialog.askopenfilename(title="Select Package File", filetypes=(("PKG files", "*.pkg"), ("All files", "*.*")))
    if filename:
        pkg_entry.delete(0, tk.END)
        pkg_entry.insert(0, filename)

def browse_payload():
    filename = filedialog.askopenfilename(title="Select Payload File", filetypes=(("BIN files", "*.bin"),
    ("ELF Files (*.elf)", "*.elf"),
    ("All files", "*.*")))
    if filename:
        payload_entry.delete(0, tk.END)
        payload_entry.insert(0, filename)

# ==========================================
# 5. تصميم الواجهة الرسومية (GUI)
# ==========================================
root = tk.Tk()
root.title("BISAN GAMES")
root.geometry("600x400")
root.resizable(False, False)

# العناوين
tk.Label(root, text="BISAN GAMES PS4 REMOTE SENDER", font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
tk.Label(root, text="PS4 package and payload remote sender", font=("Arial", 10)).pack(anchor="w", padx=10, pady=(0, 10))

# التبويبات
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=5)

tab_pkg = ttk.Frame(notebook)
tab_payload = ttk.Frame(notebook)

notebook.add(tab_pkg, text=" Pkg Sender ")
notebook.add(tab_payload, text=" Payload Listener ")

# --- تصميم تبويب الألعاب (Pkg Sender) ---
ip_frame_pkg = tk.Frame(tab_pkg)
ip_frame_pkg.pack(fill="x", padx=10, pady=10)

tk.Label(ip_frame_pkg, text="Target IP address").grid(row=0, column=0, sticky="w")
ip_entry_pkg = tk.Entry(ip_frame_pkg, width=40)
ip_entry_pkg.insert(0, "192.168.1.100")
ip_entry_pkg.grid(row=1, column=0, padx=(0, 20))

tk.Label(ip_frame_pkg, text="Port").grid(row=0, column=1, sticky="w")
port_entry_pkg = tk.Entry(ip_frame_pkg, width=15)
port_entry_pkg.insert(0, "12800")
port_entry_pkg.grid(row=1, column=1)

pkg_frame = tk.Frame(tab_pkg)
pkg_frame.pack(fill="x", padx=10, pady=10)

tk.Label(pkg_frame, text="Package file").grid(row=0, column=0, sticky="w")
pkg_entry = tk.Entry(pkg_frame, width=55)
pkg_entry.grid(row=1, column=0, padx=(0, 10))
tk.Button(pkg_frame, text="Browse...", command=browse_pkg, width=10).grid(row=1, column=1)

tk.Button(tab_pkg, text="SEND PACKAGE TO PS4", bg="#1064a3", fg="white", font=("Arial", 10, "bold"), command=send_package_action).pack(fill="x", padx=10, pady=30)

# --- تصميم تبويب البايلود (Payload Listener) ---
ip_frame_payload = tk.Frame(tab_payload)
ip_frame_payload.pack(fill="x", padx=10, pady=10)

tk.Label(ip_frame_payload, text="Target IP address").grid(row=0, column=0, sticky="w")
ip_entry_payload = tk.Entry(ip_frame_payload, width=40)
ip_entry_payload.insert(0, "192.168.1.100")
ip_entry_payload.grid(row=1, column=0, padx=(0, 20))

tk.Label(ip_frame_payload, text="Port").grid(row=0, column=1, sticky="w")
port_entry_payload = tk.Entry(ip_frame_payload, width=15)
port_entry_payload.insert(0, "9090") # المنفذ الافتراضي للبايلود في GoldHEN
port_entry_payload.grid(row=1, column=1)

payload_frame = tk.Frame(tab_payload)
payload_frame.pack(fill="x", padx=10, pady=10)

tk.Label(payload_frame, text="Payload file (.bin)").grid(row=0, column=0, sticky="w")
payload_entry = tk.Entry(payload_frame, width=55)
payload_entry.grid(row=1, column=0, padx=(0, 10))
tk.Button(payload_frame, text="Browse...", command=browse_payload, width=10).grid(row=1, column=1)

tk.Button(tab_payload, text="INJECT PAYLOAD", bg="#28a745", fg="white", font=("Arial", 10, "bold"), command=send_payload_action).pack(fill="x", padx=10, pady=30)

# تشغيل الواجهة
root.mainloop()
