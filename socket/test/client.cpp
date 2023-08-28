// client.cpp

#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#include <iostream>

using namespace std;

int main() {
  // ソケットを作成します。
  int sockfd = socket(AF_UNIX, SOCK_STREAM, 0);
  if (sockfd == -1) {
    perror("socket");
    exit(1);
  }

  // アドレスを作成します。
  struct sockaddr_un addr;
  addr.sun_family = AF_UNIX;
  strcpy(addr.sun_path, "cpp.sock");

  // ソケットをアドレスに接続します。
  if (connect(sockfd, (struct sockaddr *)&addr, sizeof(addr)) == -1) {
    perror("connect");
    exit(1);
  }

  // ソケットにデータを送信します。
  char buf[] = "Hello, server!";
  int n = write(sockfd, buf, sizeof(buf));
  if (n == -1) {
    perror("write");
    exit(1);
  }

  // ソケットからデータを受信します。
  char recv_buf[1024];
  n = read(sockfd, recv_buf, sizeof(recv_buf));
  if (n == -1) {
    perror("read");
    exit(1);
  }

  // 受信したデータを表示します。
  cout << recv_buf << endl;

  // ソケットをクローズします。
  close(sockfd);

  return 0;
}