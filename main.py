import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def browse_file():
    # دالة لفتح نافذة اختيار ملف الـ PKG
    filename = filedialog.askopenfilename(
        title="Select Package File",
        filetypes=(("PKG files", "*.pkg"), ("All files", "*.*"))
    )
    if filename:
        pkg_entry.delete(0, tk.END)
        pkg_entry.insert(0, filename)

def send_package():
    # دالة زر الإرسال (هنا حنربط كود الاتصال بالبلايستيشن لاحقاً)
    target_ip = ip_entry.get()
    target_port = port_entry.get()
    pkg_file = pkg_entry.get()
    print(f"جاري الإرسال إلى البلايستيشن: {target_ip}:{target_port}")
    print(f"الملف: {pkg_file}")

# 1. إعداد النافذة الرئيسية
root = tk.Tk()
root.title("PS4 REMOTE")
root.geometry("600x400")
root.resizable(False, False)

# إضافة العناوين العلوية
title_label = tk.Label(root, text="PS4 REMOTE ODAI", font=("Arial", 16, "bold"))
title_label.pack(anchor="w", padx=10, pady=(10, 0))

subtitle_label = tk.Label(root, text="PS4 package and payload remote sender", font=("Arial", 10))
subtitle_label.pack(anchor="w", padx=10, pady=(0, 10))

# 2. إعداد نظام التبويبات (Tabs)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=5)

# إنشاء التبويبات
tab_pkg = ttk.Frame(notebook)
tab_payload = ttk.Frame(notebook)

notebook.add(tab_pkg, text=" Pkg Sender ")
notebook.add(tab_payload, text=" Payload Listener ")

# ==========================================
# 3. تصميم تبويب (Pkg Sender)
# ==========================================

# إعدادات الـ IP والـ Port
ip_frame = tk.Frame(tab_pkg)
ip_frame.pack(fill="x", padx=10, pady=10)

tk.Label(ip_frame, text="Target IP address").grid(row=0, column=0, sticky="w")
ip_entry = tk.Entry(ip_frame, width=40)
ip_entry.insert(0, "192.168.1.100") # قيمة افتراضية
ip_entry.grid(row=1, column=0, padx=(0, 20))

tk.Label(ip_frame, text="Port").grid(row=0, column=1, sticky="w")
port_entry = tk.Entry(ip_frame, width=15)
port_entry.insert(0, "12800") # منفذ افتراضي للـ Remote Package Installer
port_entry.grid(row=1, column=1)

# إعدادات اختيار ملف PKG
pkg_frame = tk.Frame(tab_pkg)
pkg_frame.pack(fill="x", padx=10, pady=10)

tk.Label(pkg_frame, text="Package file").grid(row=0, column=0, sticky="w")
pkg_entry = tk.Entry(pkg_frame, width=55)
pkg_entry.grid(row=1, column=0, padx=(0, 10))
tk.Button(pkg_frame, text="Browse...", command=browse_file, width=10).grid(row=1, column=1)

# إعدادات رابط الـ URL
url_frame = tk.Frame(tab_pkg)
url_frame.pack(fill="x", padx=10, pady=10)

tk.Label(url_frame, text="From URL (.pkg)").grid(row=0, column=0, sticky="w")
url_entry = tk.Entry(url_frame, width=55)
url_entry.grid(row=1, column=0, padx=(0, 10))
tk.Button(url_frame, text="From URL", width=10).grid(row=1, column=1)

# زر الإرسال الرئيسي
send_btn = tk.Button(tab_pkg, text="SEND PACKAGE TO PS4", bg="#1064a3", fg="white", font=("Arial", 10, "bold"), command=send_package)
send_btn.pack(fill="x", padx=10, pady=20)

# ==========================================
# 4. تشغيل الواجهة
# ==========================================
root.mainloop()
