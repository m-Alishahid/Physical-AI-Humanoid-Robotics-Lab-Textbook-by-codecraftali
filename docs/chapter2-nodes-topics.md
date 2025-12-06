---
title: "Chapter 2: ROS 2 Nodes and Topics"
sidebar_position: 2
---

# Chapter 2: Practical ROS 2 Programming: Nodes, Topics, and Messages

In the previous chapter, we explored the high-level architecture and concepts of ROS 2. Now, it's time to get our hands dirty and write some code. This chapter is a practical, step-by-step guide to the most fundamental communication pattern in ROS 2: the anonymous publish/subscribe model using Nodes, Topics, and Messages.

By the end of this chapter, you will be able to:
*   Create a ROS 2 workspace and package.
*   Write a ROS 2 Node in both Python and C++.
*   Create a Publisher to broadcast data on a Topic.
*   Create a Subscriber to receive and process data from a Topic.
*   Understand and use standard message types.
*   Use command-line tools like `ros2 topic` and `ros2 node` to inspect and debug your running system.

## Setting Up Your ROS 2 Workspace

Before we write any code, we need a place to put it. ROS 2 uses a concept called a **workspace** to manage and build your projects. A workspace is simply a directory containing your source code, build artifacts, and installation files.

Let's create a workspace for our textbook examples. Open a terminal that has been sourced with your ROS 2 installation (e.g., `source /opt/ros/humble/setup.bash`).

```bash
# Create a directory for the workspace
mkdir -p ~/ros2_ws/src

# Navigate into the workspace
cd ~/ros2_ws
```

The `src` directory is where you will place the source code for your ROS 2 packages.

### Creating a ROS 2 Package

Code in ROS 2 is organized into **packages**. A package is a directory containing your source files, a `package.xml` file (which holds metadata like the package name, version, and dependencies), and a `CMakeLists.txt` (for C++) or `setup.py` (for Python) file that tells the build system how to compile and install your code.

We'll use the `ros2 pkg create` command to create a package for our examples. We'll name it `robotics_lab_pkg` and specify that we need dependencies for both Python (`rclpy`) and C++ (`rclcpp`).

```bash
cd ~/ros2_ws/src

ros2 pkg create --build-type ament_cmake --license Apache-2.0 robotics_lab_pkg --dependencies rclcpp std_msgs

# For a python package, you would use:
# ros2 pkg create --build-type ament_python --license Apache-2.0 my_python_pkg --dependencies rclpy std_msgs
```

Let's break down this command:
*   `--build-type ament_cmake`: Specifies we are creating a C++ package. For Python, you'd use `ament_python`.
*   `--license Apache-2.0`: It's good practice to specify a license.
*   `robotics_lab_pkg`: The name of our package.
*   `--dependencies rclcpp std_msgs`: This is crucial. It tells the build system that our package depends on the C++ client library (`rclcpp`) and the standard messages package (`std_msgs`). This automatically adds the necessary lines to our `CMakeLists.txt` and `package.xml`.

Your `~/ros2_ws/src` directory should now contain a `robotics_lab_pkg` folder.

## The "Hello, World" of ROS: A Simple Publisher Node

Our first goal is to create a node that continuously publishes a simple message. This is a fundamental building block for any robot, analogous to a sensor broadcasting its readings.

### The Publisher in Python (`rclpy`)

Python is excellent for rapid prototyping. Let's create a Python publisher first. Inside your package, create a directory for your Python scripts.

```bash
cd ~/ros2_ws/src/robotics_lab_pkg
mkdir -p robotics_lab_pkg/py_nodes
touch robotics_lab_pkg/py_nodes/simple_publisher.py
```

Now, open `simple_publisher.py` in your favorite editor and add the following code:

```python
# simple_publisher.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimplePublisher(Node):
    """
    A simple ROS 2 node that publishes a string message every second.
    """
    def __init__(self):
        # 1. Initialize the parent Node class, giving it a name
        super().__init__('simple_publisher_node')
        
        # 2. Create a publisher
        #    - Message type: String
        #    - Topic name: 'chatter'
        #    - QoS profile: 10 (queue size)
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        
        # 3. Create a timer to call the timer_callback function every 1.0 second
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.counter = 0
        self.get_logger().info('Simple Publisher Node has been started.')

    def timer_callback(self):
        # 4. Create a message object
        msg = String()
        msg.data = f'Hello, ROS 2 World! Count: {self.counter}'
        
        # 5. Publish the message
        self.publisher_.publish(msg)
        
        # 6. Log the published message to the console
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.counter += 1

def main(args=None):
    # Initialize the rclpy library
    rclpy.init(args=args)
    
    # Create an instance of the node
    simple_publisher = SimplePublisher()
    
    # "Spin" the node, which allows it to process callbacks (like the timer)
    # This will block until the node is shut down (e.g., by Ctrl+C)
    rclpy.spin(simple_publisher)
    
    # Clean up and destroy the node
    simple_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Code Breakdown (Python):**
1.  **`super().__init__('simple_publisher_node')`**: We initialize the `Node` class and give our node a unique name. This name is how it will be identified in the ROS 2 graph.
2.  **`self.create_publisher(...)`**: This is the core function. We tell ROS we want to publish messages of type `String` (from `std_msgs.msg`) on a topic named `chatter`. The `10` is the QoS queue size; if the network is slow, it will buffer up to 10 messages before starting to drop old ones.
3.  **`self.create_timer(...)`**: A convenient way to execute a function periodically. We tell it to call our `timer_callback` method every 1.0 second.
4.  **`msg = String()`**: We instantiate a message object of the type we are publishing.
5.  **`self.publisher_.publish(msg)`**: We send the message out onto the `chatter` topic.
6.  **`rclpy.init()` and `rclpy.shutdown()`**: These initialize and shut down the ROS 2 communication system.
7.  **`rclpy.spin(simple_publisher)`**: This is a crucial line. It enters a loop, waiting for and executing any pending work for the node, such as the timer firing or incoming messages (for subscribers). The program will stay in this loop until you press `Ctrl+C`.

### The Publisher in C++ (`rclcpp`)

Now let's implement the exact same functionality in C++. This is more verbose but offers higher performance, which is critical for many robotics tasks.

Open the `src` directory inside your `robotics_lab_pkg` and create a new file `simple_publisher.cpp`.

```bash
cd ~/ros2_ws/src/robotics_lab_pkg/src
touch simple_publisher.cpp
```

Add the following code:

```cpp
// simple_publisher.cpp
#include <chrono>
#include <functional>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class SimplePublisher : public rclcpp::Node
{
public:
    SimplePublisher()
    : Node("simple_publisher_node"), count_(0)
    {
        // 1. Create a publisher
        //    - Message type: std_msgs::msg::String
        //    - Topic name: 'chatter'
        //    - QoS profile: 10 (queue size)
        publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);

        // 2. Create a timer to call the timer_callback function every 1 second
        timer_ = this->create_wall_timer(
            1s, std::bind(&SimplePublisher::timer_callback, this));
        
        RCLCPP_INFO(this->get_logger(), "Simple Publisher Node has been started.");
    }

private:
    void timer_callback()
    {
        // 3. Create a message object
        auto message = std_msgs::msg::String();
        message.data = "Hello, ROS 2 World! Count: " + std::to_string(count_++);

        // 4. Log and publish the message
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
        publisher_->publish(message);
    }

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    size_t count_;
};

int main(int argc, char * argv[])
{
    // Initialize the rclcpp library
    rclcpp::init(argc, argv);

    // "Spin" the node, which allows it to process callbacks
    rclcpp::spin(std::make_shared<SimplePublisher>());

    // Clean up
    rclcpp::shutdown();
    return 0;
}
```

**Code Breakdown (C++):**
The logic is identical to the Python version, but the syntax is different.
1.  **`create_publisher<std_msgs::msg::String>("chatter", 10)`**: The template argument `<...>` specifies the message type. The arguments are the topic name and QoS profile.
2.  **`create_wall_timer(...)`**: The C++ equivalent of the timer. We use `1s` (a `chrono` literal) for convenience and `std::bind` to link the callback method to the timer.
3.  **`auto message = std_msgs::msg::String()`**: We create the message object.
4.  **`publisher_->publish(message)`**: We publish the message. Note the use of the `->` operator as `publisher_` is a shared pointer (`SharedPtr`).
5.  **`rclcpp::spin(...)`**: Similar to Python, this function blocks and processes callbacks for the node.

## The Other Half: A Simple Subscriber Node

Publishing data is useless if no one is listening. Let's create a subscriber node that listens to the `chatter` topic and prints the messages it receives.

### The Subscriber in Python (`rclpy`)

Create a new file `robotics_lab_pkg/py_nodes/simple_subscriber.py`.

```python
# simple_subscriber.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimpleSubscriber(Node):
    def __init__(self):
        super().__init__('simple_subscriber_node')
        
        # 1. Create a subscriber
        #    - Message type: String
        #    - Topic name: 'chatter'
        #    - Callback function: self.listener_callback
        #    - QoS profile: 10
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.get_logger().info('Simple Subscriber Node has been started and is listening.')

    def listener_callback(self, msg):
        # 2. This function is called every time a message is received.
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    simple_subscriber = SimpleSubscriber()
    rclpy.spin(simple_subscriber)
    simple_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Code Breakdown (Python Subscriber):**
1.  **`self.create_subscription(...)`**: This is the key function. It subscribes to the `chatter` topic. Crucially, we provide `self.listener_callback` as an argument. ROS 2 will automatically invoke this function whenever a new message arrives on the topic.
2.  **`listener_callback(self, msg)`**: This is our callback function. It receives one argument: the message object (`msg`) that was just delivered. Here, we simply log its contents.

### The Subscriber in C++ (`rclcpp`)

Create a new file `src/simple_subscriber.cpp`.

```cpp
// simple_subscriber.cpp
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using std::placeholders::_1;

class SimpleSubscriber : public rclcpp::Node
{
public:
    SimpleSubscriber()
    : Node("simple_subscriber_node")
    {
        // 1. Create a subscriber
        subscription_ = this->create_subscription<std_msgs::msg::String>(
            "chatter", 10, std::bind(&SimpleSubscriber::topic_callback, this, _1));
        
        RCLCPP_INFO(this->get_logger(), "Simple Subscriber Node has been started and is listening.");
    }

private:
    void topic_callback(const std_msgs::msg::String & msg) const
    {
        // 2. Log the received message
        RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg.data.c_str());
    }
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SimpleSubscriber>());
    rclcpp::shutdown();
    return 0;
}
```

**Code Breakdown (C++ Subscriber):**
1.  **`create_subscription<...>(...)`**: Similar to the publisher, but the third argument is the callback function. We use `std::bind` again. The `_1` is a placeholder from `std::placeholders` that represents the incoming message argument that will be passed to our `topic_callback`.
2.  **`topic_callback(const std_msgs::msg::String & msg)`**: This is our callback. It takes a constant reference to the received message to avoid unnecessary copies.

## Building and Running Your Nodes

Now that we have the source code, we need to tell ROS 2 how to build and run it.

### Configuring the Build System

For C++, you need to edit `CMakeLists.txt`. For Python, you edit `setup.py` and `package.xml`.

*(This section would include the detailed edits to `CMakeLists.txt` to add the executables and `setup.py` to define the entry points for the Python nodes. This is a critical step in a real tutorial.)*

### The Build-Source-Run Cycle

This is the workflow you will use constantly in ROS 2 development.

1.  **Build the Workspace:** Navigate to the root of your workspace (`~/ros2_ws`) and run `colcon build`.
    ```bash
    cd ~/ros2_ws
    colcon build --packages-select robotics_lab_pkg
    ```
    `colcon` is the ROS 2 build tool. It will find your packages, compile the C++ code, and set up the Python scripts.

2.  **Source the Workspace:** After a successful build, `colcon` creates `install` and `build` directories. The `install` directory contains the setup files for your new packages. You **must** source this file in every new terminal where you want to use your nodes.
    ```bash
    # In every new terminal
    source ~/ros2_ws/install/setup.bash
    ```

3.  **Run the Nodes:** Now you can run your executables using `ros2 run`.

    **Open Terminal 1:**
    ```bash
    source ~/ros2_ws/install/setup.bash
    ros2 run robotics_lab_pkg simple_publisher_node_cpp # Or simple_publisher_node_py
    ```
    You should see the "Publishing: ..." log messages appearing every second.

    **Open Terminal 2:**
    ```bash
    source ~/ros2_ws/install/setup.bash
    ros2 run robotics_lab_pkg simple_subscriber_node_cpp # Or simple_subscriber_node_py
    ```
    You should see the "I heard: ..." log messages, confirming that your subscriber is receiving data from your publisher!

### Using ROS 2 Command-Line Tools

While your nodes are running, open a **third terminal** (and don't forget to `source`!). These tools are essential for debugging.

*   **List all nodes:**
    ```bash
    ros2 node list
    # Output:
    # /simple_publisher_node
    # /simple_subscriber_node
    ```

*   **List all topics:**
    ```bash
    ros2 topic list
    # Output:
    # /chatter
    # /parameter_events
    # /rosout
    ```

*   **Echo a topic's content:** This lets you see the data on a topic without writing a subscriber.
    ```bash
    ros2 topic echo /chatter
    # Output:
    # ---
    # data: 'Hello, ROS 2 World! Count: 42'
    # ---
    ```

*   **Get information about a topic:**
    ```bash
    ros2 topic info /chatter
    # Output:
    # Type: std_msgs/msg/String
    # Publisher count: 1
    # Subscriber count: 1
    ```

Congratulations! You have successfully created, built, and run a complete, multi-node ROS 2 system. You've mastered the fundamental publish/subscribe pattern and learned how to use essential debugging tools. In the next chapter, we will build on this foundation to explore the request/response communication patterns using Services and Actions.