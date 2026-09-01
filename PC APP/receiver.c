#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 9090
#define BUFFER_SIZE 4096

void start_receiver_server() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};

    // 1. إنشاء السوكيت على البلايستيشن
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        printf("فشل إنشاء السوكيت\n");
        return;
    }

    // 2. ضبط خيارات المنفذ
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // 3. ربط المنفذ 9090
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        printf("فشل ربط المنفذ\n");
        return;
    }

    // 4. الاستماع للاتصالات القادمة من تطبيق الكمبيوتر
    if (listen(server_fd, 3) < 0) {
        printf("فشل وضع الاستماع\n");
        return;
    }

    printf("تطبيق البلايستيشن مستعد للاستقبال على المنفذ %d...\n", PORT);

    while(1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            continue;
        }

        // استقبال البيانات القادمة من الكمبيوتر
        int valread = read(new_socket, buffer, BUFFER_SIZE);
        printf("تم استقبال بيانات بحجم: %d بايت\n", valread);

        // هنا بنضيف معالجة الملف واستدعاء دالة التثبيت

        close(new_socket);
    }
}
