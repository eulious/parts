#include <fstream>
#include <iostream>

int main() {
  int i = 0;
  while (true) {
    std::string str;
    std::getline(std::cin, str);

    std::ofstream outfile("output.txt");
    outfile << str;
    outfile.close();
    std::cout << "JPEGファイルが" << i << "作成されました。" << std::endl;
    i = i + 1;
  }

  return 0;
}