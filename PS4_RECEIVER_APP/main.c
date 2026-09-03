#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>

#define PAYLOAD_PORT 9090
#define PKG_PORT 12800
#define BUFFER_SIZE 8192

// دالة لمعالجة البايلود المستقَبل (.bin / .elf)
void handle_payload(int client_socket) {
    char buffer[BUFFER_SIZE];
    ssize_t bytes_read;
    FILE *fp = fopen("/data/payload_received.bin", "wb");
    if (!fp) {
        printf("[-] فشل فتح ملف البايلود للكتابة
");
        close(client_socket);
        return;
    }

    printf("[+] جاري استقبال ملف البايلود...
");

    while ((bytes_read = read(client_socket, buffer, sizeof(buffer))) > 0) {
        fwrite(buffer, 1, bytes_read, fp);
    }

    fclose(fp);
    printf("[+] تم استلام البايلود بنجاح وحفظه في /data/payload_received.bin
");
    close(client_socket);
}

// دالة لمعالجة أوامر الـ PKG
void handle_pkg_request(int client_socket) {
    char buffer[BUFFER_SIZE] = {0};
    ssize_t bytes_read = read(client_socket, buffer, sizeof(buffer) - 1);

    if (bytes_read > 0) {
        buffer[bytes_read] = '';
        printf("[+] تم استلام أمر تثبيت PKG:
%s
", buffer);
    }

    // الرد على تطبيق الكمبيوتر بنجاح العملية (JSON Response)
    const char *response = "HTTP/1.1 200 OK
Content-Type: application/json

{"status":"success"}";
    write(client_socket, response, strlen(response));

    close(client_socket);
}

// Thread لاستقبال البايلود
void *payload_server_thread(void *arg) {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    printf("[*] جاري تشغيل خادم البايلود على المنفذ %d...
", PAYLOAD_PORT);

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("[-] فشل إنشاء سوكيت البايلود");
        return NULL;
    }

    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PAYLOAD_PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("[-] فشل في ربط سوكيت البايلود");
        close(server_fd);
        return NULL;
    }

    if (listen(server_fd, 5) < 0) {
        perror("[-] فشل في الاستماع لسوكيت البايلود");
        close(server_fd);
        return NULL;
    }

    while (1) {
        new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
        if (new_socket >= 0) {
            printf("[+] اتصال جديد لاستقبال البايلود
");
            handle_payload(new_socket);
        }
    }

    return NULL;
}

// Thread لاستقبال أوامر PKG
void *pkg_server_thread(void *arg) {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    printf("[*] جاري تشغيل خادم PKG على المنفذ %d...
", PKG_PORT);

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("[-] فشل إنشاء سوكيت PKG");
        return NULL;
    }

    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PKG_PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("[-] فشل في ربط سوكيت PKG");
        close(server_fd);
        return NULL;
    }

    if (listen(server_fd, 5) < 0) {
        perror("[-] فشل في الاستماع لسوكيت PKG");
        close(server_fd);
        return NULL;
    }

    while (1) {
        new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
        if (new_socket >= 0) {
            printf("[+] اتصال جديد لأمر PKG
");
            handle_pkg_request(new_socket);
        }
    }

    return NULL;
}

// الدالة الرئيسية للتطبيق
int main() {
    printf("=========================================
");
    printf("   BISAN REMOTE RECEIVER - ALI ECOSYSTEM  
");
    printf("=========================================
");

    pthread_t payload_thread, pkg_thread;

    // تشغيل خادم البايلود في thread منفصل
    if (pthread_create(&payload_thread, NULL, payload_server_thread, NULL) != 0) {
        perror("[-] فشل إنشاء thread خادم البايلود");
        return -1;
    }

    // تشغيل خادم PKG في thread منفصل
    if (pthread_create(&pkg_thread, NULL, pkg_server_thread, NULL) != 0) {
        perror("[-] فشل إنشاء thread خادم PKG");
        return -1;
    }

    printf("[+] الخوادم تعمل بنجاح!
");
    printf("    - Payload Server: 0.0.0.0:%d
", PAYLOAD_PORT);
    printf("    - PKG Server: 0.0.0.0:%d
", PKG_PORT);

    // انتظار threads (لن ينتهي إلا بإغلاق التطبيق)
    pthread_join(payload_thread, NULL);
    pthread_join(pkg_thread, NULL);

    return 0;
}
