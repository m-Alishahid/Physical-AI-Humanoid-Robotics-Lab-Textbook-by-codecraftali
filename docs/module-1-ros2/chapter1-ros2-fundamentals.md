# Chapter 1: ROS 2 Fundamentals

Welcome to the exciting world of ROS 2 (Robot Operating System 2)! This chapter will introduce you to the fundamental concepts and architecture of ROS 2, providing a solid foundation for building complex robotic applications. By the end of this chapter, you will understand how ROS 2 facilitates communication between different parts of a robot system and be able to set up a basic ROS 2 environment.

## 1.1 Introduction to ROS 2

ROS 2 is an open-source, flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot applications. Unlike its predecessor, ROS 1, ROS 2 was redesigned to address the requirements of modern robotics, including real-time control, multi-robot systems, and embedded platforms.

**Why ROS 2?**

Robots are inherently complex systems, often composed of numerous sensors, actuators, and computing units. Coordinating these diverse components efficiently and reliably is a significant challenge. ROS 2 provides a standardized way to:
*   **Modularize Software**: Break down complex robot behaviors into smaller, manageable software components (nodes).
*   **Facilitate Communication**: Enable these components to communicate with each other seamlessly, regardless of their programming language or physical location.
*   **Leverage a Rich Ecosystem**: Access a vast collection of existing tools, libraries, and algorithms developed by the global robotics community.
*   **Support Diverse Hardware**: Run on a wide range of hardware, from powerful workstations to resource-constrained embedded systems.

## 1.2 ROS 2 Architecture Overview

At its core, ROS 2 employs a distributed architecture, meaning that different parts of the robot software can run on separate processes, different computers, or even different robots, all communicating over a network. This distribution is managed by a **DDS (Data Distribution Service)** layer, which handles reliable and efficient data exchange.

**Key Architectural Concepts:**

*   **Nodes**: The fundamental building blocks of a ROS 2 system. Each node is an executable process that performs a specific task, such as reading sensor data, controlling a motor, or performing a complex computation. Nodes are designed to be single-purpose and reusable.
*   **Topics**: The primary mechanism for asynchronous, many-to-many communication in ROS 2. Nodes publish data (messages) to topics, and other nodes subscribe to those topics to receive the data. This publish/subscribe model allows for loose coupling between nodes, promoting modularity.
*   **Messages**: Data structures used for communication over topics. Messages are strictly typed and defined in `.msg` files, ensuring that all communicating nodes understand the format of the data being exchanged.
*   **Services**: Used for synchronous, request/response communication. When a node needs a specific task performed by another node and expects an immediate result, it can call a service. The service server processes the request and sends back a response. Services are defined in `.srv` files.
*   **Actions**: A more complex communication pattern built on topics and services, used for long-running, goal-oriented tasks. Actions allow a client to send a goal, receive continuous feedback on the progress, and ultimately get a result (or cancel the goal). Actions are defined in `.action` files.
*   **Parameters**: Configuration values that can be dynamically set and retrieved by nodes. Parameters allow for flexible configuration of robot behavior without recompiling code.
*   **ROS 2 Graph**: The collection of all active nodes and their connections (topics, services, actions) at runtime. Visualizing the ROS 2 graph is crucial for understanding the flow of data and control in a complex system.
*   **Packages**: The primary unit for organizing ROS 2 code. A package is a directory containing source files (C++, Python), message/service/action definitions, configuration files, and a `package.xml` manifest file that describes the package and its dependencies.

## 1.3 Setting up Your ROS 2 Environment

Before diving into programming, you'll need to set up your ROS 2 development environment. We'll focus on Ubuntu, which is the most common and well-supported platform for ROS 2.

**Prerequisites:**

*   **Ubuntu 22.04 (Jammy Jellyfish)** or **Ubuntu 20.04 (Focal Fossa)**: ROS 2 Jazzy Jalisco (the current LTS distribution) is recommended for Ubuntu 22.04.
*   **Internet Connection**: For downloading packages.

**Installation Steps (Ubuntu 22.04 - Jazzy Jalisco):**

1.  **Set up Locale**:
    Ensure your locale supports UTF-8.
    ```bash
    locale  # check for UTF-8
    sudo apt update && sudo apt install locales
    sudo locale-gen en_US en_US.UTF-8
    sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
    export LANG=en_US.UTF-8
    ```

2.  **Add ROS 2 Repository**:
    ```bash
    sudo apt install software-properties-common
    sudo add-apt-repository universe
    sudo apt update && sudo apt install curl -y
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
    ```

3.  **Install ROS 2 Packages**:
    Update your apt repository cache, then install the `ros-jazzy-desktop` package.
    ```bash
    sudo apt update
    sudo apt install ros-jazzy-desktop
    ```
    This command installs a complete ROS 2 environment with development tools, demos, and tutorials.

4.  **Environment Setup**:
    Source the ROS 2 setup script to make ROS 2 commands available in your current shell. Add it to your `.bashrc` for permanent access.
    ```bash
    source /opt/ros/jazzy/setup.bash
    echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
    ```
    To verify your installation, open a new terminal and run:
    ```bash
    ros2 --help
    ```
    If you see a list of ROS 2 commands, your installation is successful!

## 1.4 ROS 2 Basic Concepts in Depth

Let's delve deeper into the core communication mechanisms.

### 1.4.1 Nodes: The Executable Units

As mentioned, nodes are individual executable programs within a ROS 2 system. They are designed to be modular and can be written in various languages (Python, C++, etc.). A single ROS 2 package can contain multiple nodes.

**Example**: A robot might have a node for camera input, another for motion control, and a third for obstacle detection.

### 1.4.2 Topics: Asynchronous Data Streaming

Topics enable one-way, asynchronous communication. Data is continuously streamed from a "publisher" node to one or more "subscriber" nodes. This is ideal for sensor data (e.g., camera images, LiDAR scans), odometry, or joint states.

*   **Publisher**: A node that sends messages to a topic.
*   **Subscriber**: A node that receives messages from a topic.
*   **Message Type**: Defines the structure of data sent over a specific topic. ROS 2 provides many standard message types (e.g., `std_msgs/msg/String`, `sensor_msgs/msg/Image`). You can also define custom message types.

**Analogy**: Think of topics like a radio station. The broadcaster (publisher) sends out information, and anyone tuned to that frequency (subscribing node) receives it.

### 1.4.3 Services: Synchronous Request/Response

Services provide a synchronous, client-server communication model. A "client" node sends a request to a "server" node and waits for a response. This is suitable for tasks that require an immediate computation or action with a definite result, like "calculate inverse kinematics" or "move arm to position X."

*   **Service Server**: A node that offers a service and responds to requests.
*   **Service Client**: A node that sends a request to a service server and waits for a response.
*   **Service Type**: Defines the structure of the request and response messages. Custom service types can be defined.

**Analogy**: Services are like making a phone call to a specific person (server) to ask a question (request) and get an answer (response) directly from them.

### 1.4.4 Actions: Goal-Oriented Tasks with Feedback

Actions extend the service concept for tasks that take a long time to complete and require ongoing feedback. A "client" node sends a "goal" to an "action server," which then executes the task, periodically sending "feedback" to the client. Once the task is complete, the action server sends a "result." The client can also cancel a goal in progress.

*   **Action Server**: Executes a long-running goal and provides feedback and results.
*   **Action Client**: Sends goals, receives feedback, and awaits results from an action server.
*   **Action Type**: Defines the structure of the goal, result, and feedback messages.

**Analogy**: Actions are like ordering a pizza (goal). You get updates on its status (feedback: "dough stretched," "in oven," "on its way"), and finally, the pizza arrives (result). You can also call to cancel the order.

## 1.5 The ROS 2 Command-Line Interface (CLI)

ROS 2 provides a powerful set of command-line tools for interacting with your robot system at runtime. These tools are essential for debugging, inspection, and managing nodes.

*   **`ros2 run`**: Executes a ROS 2 node.
    ```bash
    ros2 run <package_name> <executable_name>
    ```
*   **`ros2 topic`**: Inspects and manipulates topics.
    *   `ros2 topic list`: Lists active topics.
    *   `ros2 topic echo <topic_name>`: Displays messages published on a topic.
    *   `ros2 topic pub <topic_name> <message_type> <message_data>`: Publishes data to a topic from the command line.
*   **`ros2 node`**: Manages nodes.
    *   `ros2 node list`: Lists active nodes.
    *   `ros2 node info <node_name>`: Displays information about a node (publishers, subscribers, services, actions, parameters).
*   **`ros2 service`**: Inspects and calls services.
    *   `ros2 service list`: Lists available services.
    *   `ros2 service call <service_name> <service_type> <request_data>`: Calls a service with a request.
*   **`ros2 param`**: Manages parameters.
    *   `ros2 param list`: Lists parameters.
    *   `ros2 param get <node_name> <param_name>`: Gets a parameter value.
    *   `ros2 param set <node_name> <param_name> <value>`: Sets a parameter value.
*   **`rviz2`**: A 3D visualization tool for ROS 2. It allows you to visualize sensor data, robot models, and the ROS 2 graph.
*   **`rqt`**: A GUI framework for ROS 2 with various plugins for introspection and debugging. `rqt_graph` is particularly useful for visualizing the ROS 2 computation graph.


## 1.6 Practical Examples

Let's dive into some practical Python code examples to solidify your understanding of ROS 2 fundamentals.

### 1.6.1 Example 1: Simple ROS 2 Publisher Node

This example demonstrates how to create a basic ROS 2 publisher that sends "Hello ROS 2" messages to a topic named `topic`.

```python
# simple_publisher.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS 2: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Explanation:**
1.  **`rclpy.init(args=args)`**: Initializes the ROS 2 Python client library.
2.  **`MinimalPublisher(Node)`**: Defines a class that inherits from `rclpy.node.Node`, making it a ROS 2 node.
3.  **`super().__init__('minimal_publisher')`**: Initializes the node with the name `minimal_publisher`.
4.  **`self.create_publisher(String, 'topic', 10)`**: Creates a publisher for messages of type `std_msgs.msg.String` on the `topic` topic with a queue size of 10.
5.  **`self.create_timer(timer_period, self.timer_callback)`**: Creates a timer that calls `timer_callback` every 0.5 seconds.
6.  **`self.publisher_.publish(msg)`**: Publishes the message to the topic.
7.  **`rclpy.spin(minimal_publisher)`**: Keeps the node alive and processes callbacks until `rclpy.shutdown()` is called.

**To Run:**
First, compile your ROS 2 workspace (if this is part of a package). Then, open a terminal and execute:
```bash
ros2 run <your_package_name> minimal_publisher
```

### 1.6.2 Example 2: Simple ROS 2 Subscriber Node

This example shows how to create a basic ROS 2 subscriber that receives and prints messages from the `topic` topic, which is published by the `minimal_publisher` node from the previous example.

```python
# simple_subscriber.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Explanation:**
1.  **`MinimalSubscriber(Node)`**: Defines a class for our subscriber node.
2.  **`self.create_subscription(String, 'topic', self.listener_callback, 10)`**: Creates a subscription to messages of type `std_msgs.msg.String` on the `topic` topic. When a message is received, `listener_callback` is invoked.
3.  **`listener_callback(self, msg)`**: This function is called every time a message is received. It logs the received data.

**To Run:**
First, ensure your `minimal_publisher` node is running. Then, in a separate terminal, execute:
```bash
ros2 run <your_package_name> minimal_subscriber
```

### 1.6.3 Example 3: Basic ROS 2 Service Client/Server

This example illustrates a simple service that adds two integers. We'll define a custom service type, a server node that provides the service, and a client node that calls it.

**Create Service Definition (`AddTwoInts.srv`):**
First, create a `srv` directory inside your ROS 2 package (e.g., `my_package/srv/`) and add the following file:

```
# AddTwoInts.srv
int64 a
int64 b
---
int64 sum
```

**Service Server Node (`add_two_ints_server.py`):**

```python
# add_two_ints_server.py
import rclpy
from rclpy.node import Node

from example_interfaces.srv import AddTwoInts # Replace with your package's srv if not using example_interfaces

class AddTwoIntsService(Node):

    def __init__(self):
        super().__init__('add_two_ints_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
        self.get_logger().info('Add Two Ints Service Ready.')

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request: a: %d b: %d' % (request.a, request.b))
        self.get_logger().info('Sending response: sum: %d' % response.sum)
        return response

def main(args=None):
    rclpy.init(args=args)
    add_two_ints_service = AddTwoIntsService()
    rclpy.spin(add_two_ints_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Service Client Node (`add_two_ints_client.py`):**

```python
# add_two_ints_client.py
import sys
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

from example_interfaces.srv import AddTwoInts # Replace with your package's srv if not using example_interfaces

class AddTwoIntsClient(Node):

    def __init__(self):
        super().__init__('add_two_ints_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)

    if len(sys.argv) != 3:
        print('Usage: ros2 run <your_package_name> add_two_ints_client <int_a> <int_b>')
        return

    add_two_ints_client = AddTwoIntsClient()
    response = add_two_ints_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    add_two_ints_client.get_logger().info(
        'Result of add_two_ints: for %d + %d = %d' %
        (int(sys.argv[1]), int(sys.argv[2]), response.sum))

    add_two_ints_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Explanation:**
1.  **Service Definition (`AddTwoInts.srv`)**: Defines the request (`a`, `b`) and response (`sum`) structure for our service.
2.  **Service Server**:
    *   **`self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)`**: Creates a service named `add_two_ints` of type `AddTwoInts`. When a request is received, `add_two_ints_callback` is executed.
    *   **`add_two_ints_callback(self, request, response)`**: This function receives the `request` and populates the `response` with the computed sum.
3.  **Service Client**:
    *   **`self.create_client(AddTwoInts, 'add_two_ints')`**: Creates a client to call the `add_two_ints` service.
    *   **`self.cli.wait_for_service(...)`**: The client waits until the service is available.
    *   **`self.cli.call_async(self.req)`**: Asynchronously calls the service with the request.
    *   **`rclpy.spin_until_future_complete(self, self.future)`**: Waits for the service call to complete and returns the result.

**To Run:**
1.  **Before running these, you'll need to create a ROS 2 package and place these files in the correct locations.**
    *   Create a package: `ros2 pkg create --build-type ament_python my_package`
    *   Place `AddTwoInts.srv` in `my_package/srv/`
    *   Place `add_two_ints_server.py` and `add_two_ints_client.py` in `my_package/my_package/`
    *   Update `setup.py` and `package.xml` in `my_package` to include the service and executables. Refer to ROS 2 documentation for details on custom messages/services.
2.  **Build your workspace**: `colcon build` (from your workspace root)
3.  **Source your workspace**: `source install/setup.bash` (from your workspace root)
4.  **Run the server**: In one terminal:
    ```bash
    ros2 run my_package add_two_ints_server
    ```
5.  **Run the client**: In another terminal:
    ```bash
    ros2 run my_package add_two_ints_client 5 3
    ```
    You should see the client print the sum (8) and the server log the request and response.

## 1.7 Exercises

These exercises will help you practice and deepen your understanding of ROS 2 fundamentals.

### Exercise 1.7.1: Echoing a Custom Message

**Goal**: Create a ROS 2 publisher and subscriber using a custom message type.

1.  **Define a Custom Message**: Create a file `MyCustomMessage.msg` in your package's `msg` directory:
    ```
    # MyCustomMessage.msg
    string header
    float64 timestamp
    string data
    ```
2.  **Publisher Node**: Create a publisher node that publishes `MyCustomMessage` messages to a topic `/my_custom_topic` every second.
3.  **Subscriber Node**: Create a subscriber node that subscribes to `/my_custom_topic` and prints the received message data.
4.  **Build and Run**: Compile your package and run both nodes simultaneously. Verify the subscriber prints the custom messages.

<details>
<summary>Solution 1.7.1</summary>

**`MyCustomMessage.msg`** (in `my_package/msg/`)
```
string header
float64 timestamp
string data
```

**`custom_publisher.py`** (in `my_package/my_package/`)
```python
import rclpy
from rclpy.node import Node
from my_package.msg import MyCustomMessage  # Import your custom message
import time

class CustomPublisher(Node):

    def __init__(self):
        super().__init__('custom_publisher')
        self.publisher_ = self.create_publisher(MyCustomMessage, 'my_custom_topic', 10)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = MyCustomMessage()
        msg.header = f"Message {self.i}"
        msg.timestamp = time.time()
        msg.data = f"This is custom data number {self.i}"
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.header}, {msg.data}'')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    custom_publisher = CustomPublisher()
    rclpy.spin(custom_publisher)
    custom_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**`custom_subscriber.py`** (in `my_package/my_package/`)
```python
import rclpy
from rclpy.node import Node
from my_package.msg import MyCustomMessage  # Import your custom message

class CustomSubscriber(Node):

    def __init__(self):
        super().__init__('custom_subscriber')
        self.subscription = self.create_subscription(
            MyCustomMessage,
            'my_custom_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "Header: {msg.header}, Data: {msg.data}'')

def main(args=None):
    rclpy.init(args=args)
    custom_subscriber = CustomSubscriber()
    rclpy.spin(custom_subscriber)
    custom_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**`setup.py`** (example modifications)
```python
# ... other imports
import os
from glob import glob

package_name = 'my_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'msg'), glob(os.path.join('msg', '*.msg'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='you@example.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'custom_publisher = my_package.custom_publisher:main',
            'custom_subscriber = my_package.custom_subscriber:main',
        ],
    },
)
```

**`package.xml`** (example modifications)
```xml
<!-- ... other tags -->
  <buildtool_depend>ament_cmake_python</buildtool_depend>
  <depend>rclpy</depend>
  <depend>std_msgs</depend>

  <member_of_group>rosidl_interface_packages</member_of_group>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```
</details>

### Exercise 1.7.2: Parameter Management

**Goal**: Create a ROS 2 node that uses a parameter and modify it at runtime.

1.  **Node with Parameter**: Create a node that declares an integer parameter, e.g., `update_interval`, with a default value. In its timer callback, print the current value of this parameter every second.
2.  **Runtime Modification**: While the node is running, use `ros2 param set` from the command line to change the `update_interval` to a new value. Observe if the node updates its behavior.

<details>
<summary>Solution 1.7.2</summary>

**`parameter_node.py`** (in `my_package/my_package/`)
```python
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

class ParameterNode(Node):

    def __init__(self):
        super().__init__('parameter_node')
        self.declare_parameter('update_interval', 1)  # Default to 1 second
        self.update_interval = self.get_parameter('update_interval').get_parameter_value().integer_value
        self.get_logger().info(f'Initial update_interval: {self.update_interval}'')

        self.timer = self.create_timer(self.update_interval, self.timer_callback)
        self.get_logger().info('ParameterNode Ready.')

    def timer_callback(self):
        new_interval = self.get_parameter('update_interval').get_parameter_value().integer_value
        if new_interval != self.update_interval:
            self.update_interval = new_interval
            self.get_logger().info(f'Update interval changed to: {self.update_interval}'')
            # Recreate timer with new interval (optional, but good practice for dynamic timers)
            self.timer.cancel()
            self.timer = self.create_timer(self.update_interval, self.timer_callback)

        self.get_logger().info(f'Working with interval: {self.update_interval}'')

def main(args=None):
    rclpy.init(args=args)
    parameter_node = ParameterNode()
    rclpy.spin(parameter_node)
    parameter_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**`setup.py`** (add to `entry_points`)
```python
# ...
    entry_points={
        'console_scripts': [
            'custom_publisher = my_package.custom_publisher:main',
            'custom_subscriber = my_package.custom_subscriber:main',
            'parameter_node = my_package.parameter_node:main',
        ],
    },
# ...
```

**`package.xml`** (no changes usually required for basic parameters)

**To Run:**
1.  Build and source your workspace.
2.  Run the node:
    ```bash
    ros2 run my_package parameter_node
    ```
3.  In another terminal, check its parameters:
    ```bash
    ros2 param list /parameter_node
    ```
4.  Change the parameter:
    ```bash
    ros2 param set /parameter_node update_interval 5
    ```
    Observe the logs from `parameter_node` to see the change.
</details>

### Exercise 1.7.3: Understanding ROS 2 Graph

**Goal**: Visualize the ROS 2 computation graph and identify nodes and topics.

1.  **Run Nodes**: Start your `simple_publisher.py` and `simple_subscriber.py` nodes (from examples or Exercise 1.7.1 solution).
2.  **Visualize Graph**: Open `rqt_graph`.
    ```bash
    rqt_graph
    ```
3.  **Analyze**: Identify the publisher and subscriber nodes, and the topic connecting them. Experiment by stopping one node and observing the graph change.

<details>
<summary>Solution 1.7.3</summary>

This exercise primarily involves using the `rqt_graph` tool. There's no specific code to write here, but the outcome should be a visual understanding of the ROS 2 graph.

**Expected Observations:**
*   You will see two nodes: `/minimal_publisher` and `/minimal_subscriber`.
*   A topic `/topic` will connect them, flowing from the publisher to the subscriber.
*   If you stop `/minimal_publisher`, `/topic` will still exist but without an active publisher. If you stop `/minimal_subscriber`, it will disappear from the graph.
</details>

### Exercise 1.7.4: Publishing Data from the Command Line

**Goal**: Use the `ros2 topic pub` command to send a message to a running subscriber.

1.  **Start Subscriber**: Run your `simple_subscriber.py` node (from example 1.6.2 or Exercise 1.7.1 solution).
2.  **Publish from CLI**: In a separate terminal, publish a string message to the `/topic` topic.
    ```bash
    ros2 topic pub /topic std_msgs/msg/String 'data: "Hello from CLI!"'
    ```
3.  **Verify**: Observe the subscriber's output. It should print "I heard: Hello from CLI!".

<details>
<summary>Solution 1.7.4</summary>

This exercise focuses on direct CLI interaction.

**Steps to follow:**
1.  Open terminal 1, build and source your workspace, then run:
    ```bash
    ros2 run my_package simple_subscriber
    ```
2.  Open terminal 2, build and source your workspace, then run:
    ```bash
    ros2 topic pub /topic std_msgs/msg/String 'data: "Hello from CLI!"'
    ```

**Expected Output in Terminal 1 (subscriber):**
```
[INFO] [minimal_subscriber]: I heard: "Hello from CLI!"
```
</details>

### Exercise 1.7.5: Simple ROS 2 Action

**Goal**: Understand the basics of ROS 2 Actions by implementing a simple action server and client.

1.  **Define an Action**: Create a file `Fibonacci.action` in your package's `action` directory:
    ```
    # Fibonacci.action
    int32 order
    ---
    int32[] sequence
    ---
    int32[] partial_sequence
    ```
2.  **Action Server Node**: Implement an action server that computes the Fibonacci sequence up to a given `order` (goal). It should publish `partial_sequence` as feedback and the final `sequence` as the result.
3.  **Action Client Node**: Implement an action client that sends an `order` goal to the Fibonacci action server and prints the feedback and final result.
4.  **Build and Run**: Compile your package, then run the action server. In a separate terminal, run the action client.

<details>
<summary>Solution 1.7.5</summary>

**`Fibonacci.action`** (in `my_package/action/`)
```
int32 order
---
int32[] sequence
---
int32[] partial_sequence
```

**`fibonacci_action_server.py`** (in `my_package/my_package/`)
```python
import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from example_interfaces.action import Fibonacci # Replace with your package's action if not using example_interfaces

class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        sequence = [0, 1]
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            sequence.append(sequence[i] + sequence[i-1])
            feedback_msg.partial_sequence = sequence
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback: {feedback_msg.partial_sequence}'')
            time.sleep(1) # Simulate long-running task

        goal_handle.succeeded()

        result = Fibonacci.Result()
        result.sequence = sequence
        self.get_logger().info(f'Result: {result.sequence}'')
        return result

def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(fibonacci_action_server)

if __name__ == '__main__':
    main()
```

**`fibonacci_action_client.py`** (in `my_package/my_package/`)
```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from example_interfaces.action import Fibonacci # Replace with your package's action if not using example_interfaces

class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}'')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback.partial_sequence}'')

def main(args=None):
    rclpy.init(args=args)

    action_client = FibonacciActionClient()
    action_client.send_goal(10) # Request Fibonacci sequence up to order 10

    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
```

**`setup.py`** (example modifications)
```python
# ...
import os
from glob import glob

package_name = 'my_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'msg'), glob(os.path.join('msg', '*.msg'))),
        (os.path.join('share', package_name, 'srv'), glob(os.path.join('srv', '*.srv'))),
        (os.path.join('share', package_name, 'action'), glob(os.path.join('action', '*.action'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='you@example.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'custom_publisher = my_package.custom_publisher:main',
            'custom_subscriber = my_package.custom_subscriber:main',
            'parameter_node = my_package.parameter_node:main',
            'add_two_ints_server = my_package.add_two_ints_server:main',
            'add_two_ints_client = my_package.add_two_ints_client:main',
            'fibonacci_action_server = my_package.fibonacci_action_server:main',
            'fibonacci_action_client = my_package.fibonacci_action_client:main',
        ],
    },
)
```

**`package.xml`** (example modifications)
```xml
<!-- ... other tags -->
  <buildtool_depend>ament_cmake_python</buildtool_depend>
  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>example_interfaces</depend> <!-- For AddTwoInts.srv and Fibonacci.action -->

  <member_of_group>rosidl_interface_packages</member_of_group>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

**To Run:**
1.  **Before running, update your `setup.py` and `package.xml`** to correctly define the `action` directory and executables. Refer to ROS 2 documentation for details.
2.  Build your workspace: `colcon build`
3.  Source your workspace: `source install/setup.bash`
4.  Run the server: `ros2 run my_package fibonacci_action_server`
5.  Run the client: `ros2 run my_package fibonacci_action_client`
    You will observe feedback messages from the client and server as the sequence is computed, followed by the final result.
</details>

## 1.8 RAG and Urdu Integration

To enhance the learning experience, this chapter includes markers for RAG (Retrieval-Augmented Generation) chatbot integration and Urdu translations for key terms. These features aim to provide interactive assistance and language accessibility.

### 1.8.1 RAG Chatbot Integration Points

Throughout the chapter, you will find `<!-- RAG_INTEGRATION_POINT: <query_suggestion> -->` markers. These indicate areas where a RAG chatbot can provide additional context, answer questions, or offer further explanations based on the surrounding content. For example, a query suggestion might be "What are ROS 2 nodes?" or "Explain the difference between topics and services."

*   **ROS 2 Nodes**: `<!-- RAG_INTEGRATION_POINT: What is a ROS 2 node? -->`
*   **Topics**: `<!-- RAG_INTEGRATION_POINT: How do ROS 2 topics work? -->`
*   **Messages**: `<!-- RAG_INTEGRATION_POINT: Explain ROS 2 message types -->`
*   **Services**: `<!-- RAG_INTEGRATION_POINT: When to use ROS 2 services? -->`
*   **Actions**: `<!-- RAG_INTEGRATION_POINT: Describe ROS 2 actions with an example -->`
*   **Parameters**: `<!-- RAG_INTEGRATION_POINT: How to manage ROS 2 parameters? -->`
*   **ROS 2 Graph**: `<!-- RAG_INTEGRATION_POINT: Visualize the ROS 2 computation graph -->`
*   **Packages**: `<!-- RAG_INTEGRATION_POINT: What is a ROS 2 package? -->`
*   **DDS**: `<!-- RAG_INTEGRATION_POINT: Explain Data Distribution Service (DDS) in ROS 2 -->`
*   **`ros2 run`**: `<!-- RAG_INTEGRATION_POINT: How to run a ROS 2 node using ros2 run? -->`
*   **`ros2 topic`**: `<!-- RAG_INTEGRATION_POINT: Basic ros2 topic commands -->`
*   **`ros2 service`**: `<!-- RAG_INTEGRATION_POINT: Basic ros2 service commands -->`
*   **`ros2 param`**: `<!-- RAG_INTEGRATION_POINT: Basic ros2 param commands -->`
*   **`rviz2`**: `<!-- RAG_INTEGRATION_POINT: Introduction to RViz2 for ROS 2 visualization -->`
*   **`rqt`**: `<!-- RAG_INTEGRATION_POINT: How to use rqt for ROS 2 introspection? -->`

### 1.8.2 Urdu Translation Tags

Key technical terms are marked with `urdu_tag` elements to facilitate on-demand Urdu translations. These tags allow learners to instantly view the Urdu equivalent and a brief explanation, promoting inclusivity and understanding for Urdu-speaking audiences. The translations are sourced from a centralized `translation_tags.json` file.

Here are some examples of terms with `urdu_tag`:

*   **ROS 2 Fundamentals**: <urdu_tag term="ROS 2 Fundamentals" />
*   **Nodes**: <urdu_tag term="Nodes" />
*   **Topics**: <urdu_tag term="Topics" />
*   **Messages**: <urdu_tag term="Messages" />
*   **Services**: <urdu_tag term="Services" />
*   **Actions**: <urdu_tag term="Actions" />
*   **Parameters**: <urdu_tag term="Parameters" />
*   **Packages**: <urdu_tag term="Packages" />
*   **DDS**: <urdu_tag term="DDS" />
*   **Publisher**: <urdu_tag term="Publisher" />
*   **Subscriber**: <urdu_tag term="Subscriber" />
*   **Service Server**: <urdu_tag term="Service Server" />
*   **Service Client**: <urdu_tag term="Service Client" />
*   **Action Server**: <urdu_tag term="Action Server" />
*   **Action Client**: <urdu_tag term="Action Client" />
*   **ROS 2 Graph**: <urdu_tag term="ROS 2 Graph" />

These integration points and tags are designed to make the learning experience more interactive and accessible. As you progress through the chapter, you can leverage these features to deepen your understanding and explore concepts in more detail.
