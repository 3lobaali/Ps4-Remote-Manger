#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PAYLOAD_PORT 9090
#define PKG_PORT 12800
#define BUFFER_SIZE 8192

// دالة لمعالجة البايلود المستقَبل (.bin / .elf)
void handle_payload(int client_socket) {
    char buffer[BUFFER_SIZE];
    ssize_t bytes_read;

    printf("[+] جاري استقبال ملف البايلود...\n");

    // قراءة البيانات المستقبلة من تطبيق بايثون
    while ((bytes_read = read(client_socket, buffer, sizeof(buffer))) > 0) {
        // هنا بيتم كتابة البيانات في الذاكرة المباشرة أو تنفيذ البايلود
    }

    printf("[+] تم استلام البايلود بنجاح!\n");
    close(client_socket);
}

// دالة لمعالجة أوامر الـ PKG
void handle_pkg_request(int client_socket) {
    char buffer[BUFFER_SIZE] = {0};
    read(client_socket, buffer, sizeof(buffer));

    printf("[+] تم استلام أمر تثبيت PKG:\n%s\n", buffer);

    // الرد على تطبيق الكمبيوتر بنجاح العملية (JSON Response)
    char *response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\":\"success\"}";
    write(client_socket, response, strlen(response));

    close(client_socket);
}

// الدالة الرئيسية للتطبيق
int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    printf("=========================================\n");
    printf("   PS4 REMOTE RECEIVER - ODAI ECOSYSTEM  \n");
    printf("=========================================\n");

    // 1. إنشاء الـ Socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("[-] فشل إنشاء السوكيت");
        return -1;
    }

    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PAYLOAD_PORT);

    // 2. ربط المنفذ 9090
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("[-] فشل ربط المنفذ");
        return -1;
    }

    // 3. لبدء الاستماع
    if (listen(server_fd, 5) < 0) {
        perror("[-] فشل الاستماع");
        return -1;
    }

    printf("[+] التطبيق شغال وجاهز للاستقبال على المنفذ %d...\n", PAYLOAD_PORT);

    while (1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            continue;
        }

        // معالجة الاتصال القادم
        handle_payload(new_socket);
    }

    return 0;
}
