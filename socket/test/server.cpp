// server.cpp

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

  // ソケットをアドレスにバインドします。
  if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) == -1) {
    perror("bind");
    exit(1);
  }

  // ソケットをリッスンモードにします。
  listen(sockfd, 5);

  // 接続を受け付けます。
  int clientfd = accept(sockfd, NULL, NULL);
  if (clientfd == -1) {
    perror("accept");
    exit(1);
  }

  // クライアントからデータを受信します。
  char buf[1024];
  int n = read(clientfd, buf, sizeof(buf));
  if (n == -1) {
    perror("read");
    exit(1);
  }

  // 受信したデータを表示します。
  cout << buf << endl;

  // クライアントにデータを送信します。
  n = write(clientfd, "Hello, world!", 12);
  if (n == -1) {
    perror("write");
    exit(1);
  }

  // ソケットをクローズします。
  close(sockfd);
  close(clientfd);

  return 0;
}