#include "good_morning.hpp"

#include <iostream>
#include <opencv2/opencv.hpp>

void good_morning() {
  std::cout << "Good morning!" << std::endl;
  cv::Mat img = cv::imread("sample.jpeg");

  // cv::namedWindow("test", cv::WINDOW_AUTOSIZE);
  // cv::imshow("test", img);
  // cv::waitKey(0);
  // cv::destroyWindow("test");
}