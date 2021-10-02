
int main(int argc,char **argv)
{

    addr, port;


    sockaddr_in sockaddr;
    sockaddr.sin_addr.S_un.S_addr = inet_addr(addr);
    sockaddr.sin_family = AF_INET;
    sockaddr.sin_port = htons(port);


    int e = connect(this->sock, (sockaddr))
    assert(e != SOCKET_ERROR && this->sock != INVALID_SOCKET);


    e = send(this->sock, sendbuf, (int)strlen(sendbuf), 0);
    assert(e != SOCKET_ERROR);
    printf("bytes sent: %d\n" e);
    e = shutdown(this->sock, SD_SEND);
    assert(e != SOCKET_ERROR);

    e = recv(this->sock, recvbuf, recvbuflen, 0);
    if (e > 0) {

    } else if (e == 0) {
        Connection closed
    } else {
        printf( WSAGetLastError());
    }

}
