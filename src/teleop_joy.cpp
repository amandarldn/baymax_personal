#include <memory>
#include <iostream>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joy.hpp"
#include "geometry_msgs/msg/twist.hpp"

using std::placeholders::_1;

class TeleopJoy : public rclcpp::Node
{
  public:
    TeleopJoy()
    : Node("teleop_joy")
    {
      subscription_ = this->create_subscription<sensor_msgs::msg::Joy>(
      "/joy", 10, std::bind(&TeleopJoy::topic_callback, this, _1));
      publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);

    }

  private:
    void topic_callback(const sensor_msgs::msg::Joy::SharedPtr msg) const
    {
      horizontal = msg->axes[0];
      vertical = msg->axes[1];
      auto command = geometry_msgs::msg::Twist();
      command.linear.set__x(vertical);
      command.angular.set__z(horizontal);
      publisher_->publish(command);
    }

    rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr subscription_;
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    mutable float horizontal = 0.0;
    mutable float vertical = 0.0;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<TeleopJoy>());
  rclcpp::shutdown();
  return 0;
}