
int main(int argc, char **argv) {

    SOCKADDR_IN addr;
    addr.sin_family = AF_INET;
    addr.sin_addr.S_un.S_addr = htonl(INADDR_ANY);
    addr.sin_port = htons(6000);

    bind(serSocket, (SOCKADDR *)&addr, sizeof(SOCKADDR));
    listen(serSocket, 5);

    SOCKADDR_IN clientsocket;
    int len = sizeof(SOCKADDR);
    while (1) {
    SOCKET serConn = accept(serSocket, (SOCKADDR *)&clientsocket, &len);
    char sendBuf[100];

    sprintf(
        sendBuf, "hello, %s !",
        inet_ntoa(clientsocket.sin_addr));
    printf("Send:%s\n", sendBuf);
    send(serConn, sendBuf, strlen(sendBuf) + 1, 0);

    char receiveBuf[100];  //接收
    recv(serConn, receiveBuf, sizeof(receiveBuf), 0);
    printf("recv:%s\n", receiveBuf);
    }
}
