#pragma once

#include <cstdio>
#include <string>
#include <assert.h>

#define WIN32

#ifdef WIN32
#include <winsock2.h>
#pragma comment(lib, "ws2_32.lib")
#else
#include <socket.h>
#endif

#define __FILENAME__ (strrchr(__FILE__, '\\') ? strrchr(__FILE__, '\\') + 1 : __FILE__)

namespace nrpc {

class RpcBase {
public:
    RpcBase();
private:
    SOCKET sock = INVALID_SOCKET;
}


RpcBase::RpcBase() {
    WSAData wsaData;
    int e = WSAStartup(MAKEWORD(2, 2), &wsaData);
    assert(e);

    this->sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    assert(this->sock != INVALID_SOCKET);

}


~RpcBase::RpcBase() {
    closesocket(sock);
    WSACleanup();
}


Server::Server() {
    sockaddr_in sock_addr;
    sockaddr.sin_family = AF_INET;
    sockaddr.sin_addr.s_addr = INADDR_ANY;
    sock_addr.sin_port = htons(port);

    if (bind(sock, (sockaddr*)&sock_addr, sizeof(sock_addr))) {
        printf("%s(%d): %d", __FILE__, __LINE__, WSAGetLastError());
    }
    e = listen(sock, 5);
    assert(e != SOCKET_ERROR);
    logger('LISTEN');

}

    while (1) {
        SOCKET conn = accept(this->sock, NULL, NULL);
    }


#define HEADERLEN   4
#define BUFSIZE     8192


int main(int argc, char* argv[])
{
    assert(argc == 2);
    int port = atoi(argv[1]);

    char buf[BUFSIZE + 1];
    // Wating for connections.
    while (1) {
        sockaddr_in conn_addr;
        int addrlen = sizeof(conn_addr);
        SOCKET conn = accept(sock, (sockaddr*)&conn_addr, &addrlen);

        if (conn == INVALID_SOCKET) {
            printf("%s(%d): %d", __FILE__, __LINE__, WSAGetLastError());
        }
        printf("Connected.\n");

        // Wating for packets.
        while (1) {
            int recv_size = recv(conn, buf, BUFSIZE, 0);
            if (!recv_size) {       // Remote socket closed.
                printf("Connection broken.\n");
                break;
            }
            char header[HEADERLEN + 1] = { 0 };
            strncpy(header, buf, HEADERLEN);
            int packlen = atoi(header);

            if (packlen > 0) {                  // header > 0: calls ltgpos and return the result.
                // if (packlen > BUFSIZE)       // This may not happen now.
                int total_size = recv_size;
                while (total_size - HEADERLEN != packlen) {     // Incomplete packet.
                    total_size += recv(conn, buf + total_size, BUFSIZE - total_size, 0);
                }
                buf[total_size] = 0;
                printf("Packet received.\n");
                char* output = ...;
                send(conn, output, strlen(output), 0);
                // TODO send exception
            } else if (packlen == -1) {         // header == -1: closes socket.
                closesocket(conn);
                break;
            } else if (packlen == -2) {         // header == -2: closes server.
                closesocket(conn);
                // goto l1;
                break;
            }
        }
    }
}
