




# Chapter 1: Introduction to ROS 2

This chapter introduces the fundamental concepts of the Robot Operating System 2 (ROS 2), its architecture, and why it has become the standard for modern robotics development.

## 1.1 What is ROS 2?

The **Robot Operating System 2 (ROS 2)** is not an actual operating system but a **middleware framework** that provides tools, libraries, and conventions for building complex robotic systems. It's the successor to ROS 1, designed to address its limitations while maintaining its core philosophy.

### Key Characteristics:
- **Open-source** robotics middleware
- **Language-agnostic** (primarily Python and C++)
- **Distributed** system architecture
- **Real-time** capable
- **Cross-platform** (Linux, Windows, macOS)
- **Commercial-friendly** licensing (Apache 2.0)

## 1.2 Why ROS 2? Evolution from ROS 1

### ROS 1 Limitations:
- Single robot, single master architecture
- Lack of real-time capabilities
- Security vulnerabilities
- No support for Windows or real-time operating systems
- Difficult to deploy in production

### ROS 2 Improvements:
- **Decentralized architecture** using Data Distribution Service (DDS)
- **Real-time support** for deterministic systems
- **Enhanced security** with authentication and encryption
- **Multi-robot support** out of the box
- **Production-ready** for commercial applications
- **Better quality of service (QoS)** policies

## 1.3 ROS 2 Architecture Overview

### Core Components:

```mermaid
graph TD
    A[ROS 2 Node] --> B[Topic Publisher]
    A --> C[Topic Subscriber]
    A --> D[Service Server]
    A --> E[Action Server]
    B --> F[DDS Middleware]
    C --> F
    D --> F
    E --> F
    F --> G[Network Transport]
1.3.1 DDS (Data Distribution Service)
ROS 2 uses DDS as its middleware layer, providing:

Decentralized discovery (no central master)

Multiple QoS policies for different communication needs

Type-safe data exchange

Platform independence

python
# Example: ROS 2 Quality of Service (QoS) Profiles
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

# Best effort communication (default)
qos_best_effort = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.BEST_EFFORT
)

# Reliable communication (for critical data)
qos_reliable = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL
)
1.3.2 Node Architecture
Nodes: Independent processes performing specific computations

Executors: Manage node execution and callbacks

Context: ROS 2 runtime environment

1.4 ROS 2 Distributions
ROS 2 follows Ubuntu-style distribution naming and release cycles:

Distribution	Release Date	EOL Date	Recommended For
Iron Irwini	May 2023	Nov 2024	Latest features
Humble Hawksbill	May 2022	May 2027	Recommended for this course
Galactic Geochelone	May 2021	Dec 2022	Legacy projects
Foxy Fitzroy	Jun 2020	Jun 2023	Legacy projects
For this textbook, we'll use ROS 2 Humble Hawksbill as it's the current Long-Term Support (LTS) release.

1.5 Core Concepts
1.5.1 Topics
Asynchronous communication channels

Publishers send messages, subscribers receive them

Used for continuous data streams (e.g., sensor data)

1.5.2 Services
Synchronous request-response pattern

Client sends request, server processes and returns response

Used for one-time operations (e.g., turning on a camera)

1.5.3 Actions
Asynchronous long-running operations

Client sends goal, server provides feedback and result

Used for complex tasks (e.g., navigating to a point)

1.5.4 Parameters
Dynamic configuration variables

Can be modified at runtime

Used for system tuning and configuration

1.6 Installation and Setup
Ubuntu 22.04 Installation:
bash
# 1. Set locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# 2. Add ROS 2 repository
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# 3. Add to sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 4. Install ROS 2 Humble
sudo apt update
sudo apt install ros-humble-desktop

# 5. Set up environment
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

# 6. Install colcon build tool
sudo apt install python3-colcon-common-extensions

# 7. Verify installation
ros2 --version
Verification Test:
bash
# Run a simple talker-listener demo
ros2 run demo_nodes_cpp talker &
ros2 run demo_nodes_cpp listener &

# Check active nodes
ros2 node list

# Check active topics
ros2 topic list
1.7 ROS 2 Workspace Structure
A typical ROS 2 workspace follows this structure:

text
workspace/
├── src/                    # Source packages
│   ├── package1/
│   │   ├── CMakeLists.txt
│   │   ├── package.xml
│   │   └── ...
│   └── package2/
│       ├── setup.py
│       ├── package.xml
│       └── ...
├── build/                  # Build files
├── install/                # Installed packages
└── log/                    # Build logs
Creating a Workspace:
bash
# Create workspace directory
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Clone example packages
git clone https://github.com/ros2/examples src/examples -b humble

# Build workspace
colcon build

# Source the workspace
source install/setup.bash
1.8 Basic ROS 2 Commands
Command	Description	Example
ros2 node list	List all running nodes	ros2 node list
ros2 topic list	List all active topics	ros2 topic list -t
ros2 topic echo	Display messages on a topic	ros2 topic echo /chatter
ros2 service list	List all available services	ros2 service list -t
ros2 param list	List all parameters	ros2 param list
ros2 bag record	Record topic data	ros2 bag record -a
ros2 run	Run a package executable	ros2 run demo_nodes_cpp talker
ros2 launch	Launch multiple nodes	ros2 launch package launch_file.launch.py
1.9 ROS 2 vs. Other Robotics Frameworks
Feature	ROS 2	ROS 1	YARP	MOOS
Real-time Support	✅ Excellent	❌ Poor	⚠️ Limited	⚠️ Limited
Multi-robot	✅ Native	❌ Difficult	✅ Good	✅ Good
Security	✅ Built-in	❌ None	⚠️ Basic	⚠️ Basic
Commercial Use	✅ Apache 2.0	❌ Mixed	✅ MIT	✅ MIT
Community	✅ Large	✅ Large	⚠️ Moderate	⚠️ Moderate
Learning Curve	⚠️ Steep	⚠️ Steep	✅ Moderate	✅ Moderate
1.10 Practical Example: Your First ROS 2 Node
Let's create a simple Python node that publishes messages:

python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        
    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS 2: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    simple_publisher = SimplePublisher()
    
    try:
        rclpy.spin(simple_publisher)
    except KeyboardInterrupt:
        pass
    
    simple_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
Running the Node:
bash
# Make the file executable
chmod +x simple_publisher.py

# Run the node
python3 simple_publisher.py

# In another terminal, listen to messages
ros2 topic echo /chatter
1.11 Common ROS 2 Tools
1.11.1 rqt - ROS 2 GUI Tool
bash
# Install rqt
sudo apt install ros-humble-rqt*

# Launch rqt
rqt
1.11.2 RViz2 - 3D Visualization
bash
# Install RViz2
sudo apt install ros-humble-rviz2

# Launch RViz2
rviz2
1.11.3 ros2doctor - System Check
bash
# Check system health
ros2 doctor

# Check specific component
ros2 doctor --report
1.12 Best Practices for ROS 2 Development
1.12.1 Node Design Principles
Single Responsibility: Each node should do one thing well

Loose Coupling: Minimize dependencies between nodes

Configuration: Use parameters for tunable values

Logging: Use appropriate log levels (DEBUG, INFO, WARN, ERROR)

Error Handling: Implement proper exception handling

1.12.2 Performance Tips
Use appropriate QoS policies

Minimize data copying

Profile with ros2 topic hz and ros2 topic bw

Consider using intra-process communication for closely coupled nodes

1.12.3 Security Practices
Enable authentication for production systems

Use namespaces for multi-robot systems

Implement access control lists (ACLs)

Regularly update ROS 2 packages

1.13 Summary
In this chapter, we've covered:

The fundamental concepts and architecture of ROS 2

How ROS 2 improves upon ROS 1

Installation and setup procedures

Basic commands and tools

Creating your first ROS 2 node

Best practices for ROS 2 development

ROS 2 represents a significant evolution in robotics middleware, providing the foundation for modern, scalable, and production-ready robotic systems.

1.14 Exercises
Exercise 1: Installation Verification
Install ROS 2 Humble on your system

Run the talker-listener demo

Use ros2 doctor to verify your installation

Exercise 2: First Node
Create a Python node that subscribes to the /chatter topic

Modify the node to count messages received

Add a parameter to control the logging frequency

Exercise 3: System Exploration
Launch multiple demo nodes

Use rqt_graph to visualize the node connections

Record a bag file and play it back

Exercise 4: Troubleshooting
Intentionally create a node with incorrect QoS settings

Observe the communication failures

Fix the QoS configuration

1.15 Next Steps
In the next chapter, we'll dive deeper into ROS 2 Nodes and Topics, exploring:

Creating custom message types

Advanced publisher/subscriber patterns

Understanding DDS quality of service

Multi-node communication patterns

Key Takeaways:

ROS 2 is a middleware framework, not an operating system

DDS provides decentralized, real-time capable communication

Humble Hawksbill is the current LTS release recommended for learning

Proper workspace structure is essential for project organization

Understanding basic commands is crucial for debugging and development

Resources for Further Learning:

ROS 2 Documentation

ROS 2 Tutorials

ROS 2 Design Articles