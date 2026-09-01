import socket

def send_payload(ps4_ip, payload_path, port=9020):
    try:
        # قراءة ملف البايلود (bin أو elf) كبيانات ثنائية
        with open(payload_path, 'rb') as file:
            payload_data = file.read()

        # إنشاء اتصال Socket مع البلايستيشن
        print(f"جاري الاتصال بـ {ps4_ip} على المنفذ {port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10) # تحديد وقت أقصى للاتصال
        sock.connect((ps4_ip, port))

        # إرسال البيانات وإغلاق الاتصال
        sock.sendall(payload_data)
        sock.close()

        print("تم إرسال البايلود بنجاح يا زول!")
        return True

    except ConnectionRefusedError:
        print("خطأ: تم رفض الاتصال. تأكد من تفعيل Bin Loader في البلايستيشن.")
        return False
    except Exception as e:
        print(f"حدث خطأ غير متوقع: {e}")
        return False
