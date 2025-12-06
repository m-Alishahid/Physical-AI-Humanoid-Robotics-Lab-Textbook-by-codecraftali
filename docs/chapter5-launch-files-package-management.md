---
title: "Chapter 5: Launch Files and Package Management"
sidebar_position: 5
---

# Chapter 5: Launch Files and Package Management

Until now, we have been starting our nodes manually using the `ros2 run` command in separate terminals. This is fine for a simple system, but a real-world robot can have dozens of nodes, each with its own parameters, remappings, and configurations. Managing all of this manually is impossible.

The solution to this problem is the **ROS 2 Launch System**. This chapter will teach you how to use Python-based launch files to start, configure, and manage complex robotic applications with a single command. We will also look at the `colcon` build system and best practices for package management.

## The ROS 2 Launch System: The Power of Python

In ROS 1, launch files were XML-based, which was declarative but lacked programmatic logic. ROS 2 changes this paradigm. In ROS 2, launch files are **Python scripts**. This means you can use the full power of Python to launch your application:

*   **Variables, Loops, and Conditionals:** Launch nodes dynamically for different scenarios.
*   **Functions and Classes:** Organize and reuse your launch logic.
*   **File I/O and Environment Variables:** Load parameters from external configuration files or change behavior based on the system environment.
*   **Arguments:** Customize the behavior of the launch file from the command line.

### Anatomy of a Basic Launch File

A ROS 2 launch file is a Python script that defines a function called `generate_launch_description()`. This function returns a `LaunchDescription` object, which contains a list of all the "actions" that the launch system needs to execute.

Let's create a launch file for our publisher and subscriber nodes from Chapter 2.

Create the file `robotics_lab_pkg/launch/pub_sub_demo.launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Create a LaunchDescription object.
    ld = LaunchDescription()

    # 2. Define the publisher node.
    publisher_node = Node(
        package='robotics_lab_pkg',
        executable='simple_publisher_node_py', # Your Python or C++ executable name
        name='my_publisher' # Optional: Override the node name
    )

    # 3. Define the subscriber node.
    subscriber_node = Node(
        package='robotics_lab_pkg',
        executable='simple_subscriber_node_py',
        name='my_subscriber'
    )

    # 4. Add the nodes to the LaunchDescription.
    ld.add_action(publisher_node)
    ld.add_action(subscriber_node)

    # 5. Return the LaunchDescription.
    return ld
```

**Code Breakdown:**
1.  `LaunchDescription`: This is the container for all launch actions.
2.  `Node`: This is the most common action. It is equivalent to starting a ROS 2 node. We specify the `package` and `executable`.
3.  `ld.add_action()`: We add our created node actions to the launch description.

To run this launch file, source your workspace and use the `ros2 launch` command:

```bash
ros2 launch robotics_lab_pkg pub_sub_demo.launch.py
```

This command will start both the publisher and subscriber nodes simultaneously!

### Parameters and Remappings

The real power of launch files lies in configuring nodes.

Let's launch our parameter-enabled publisher (from Chapter 3) and set its frequency.

```python
# advanced_launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robotics_lab_pkg',
            executable='simple_publisher_with_params',
            name='param_publisher',
            # Set parameters
            parameters=[
                {'publish_frequency': 5.0}
            ],
            # Remap topics
            remappings=[
                ('/chatter', '/my_custom_chatter_topic')
            ]
        ),
        Node(
            package='robotics_lab_pkg',
            executable='simple_subscriber_node_py',
            name='param_subscriber',
            remappings=[
                ('/chatter', '/my_custom_chatter_topic')
            ]
        )
    ])
```

Here, we have used two more arguments inside the `Node` action:
*   `parameters`: A list of dictionaries where we set the parameter name and its value. Now our publisher will publish at 5 Hz.
*   `remappings`: A list of tuples that changes the names of topics, services, or actions. Here, we have remapped the default `/chatter` topic to `/my_custom_chatter_topic`. Remapping is necessary in both nodes for them to communicate.

### URDF and Launch Files

In the previous chapter, we saw a launch file for launching `robot_state_publisher`. That is an excellent example of how launch files can process external files (like URDF/Xacro) and pass their content as a parameter.

```python
# From Chapter 4
import xacro
# ...
robot_description_raw = xacro.process_file(urdf_file_path).toxml()

robot_state_publisher_node = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[{'robot_description': robot_description_raw}]
)
```
Here, the Python `xacro` library processes the Xacro file and converts it into a string, which is then passed to the `robot_description` parameter of the `robot_state_publisher` node.

## Package Management and `colcon`

An important part of building a robust robotics system is organizing the code well. In ROS 2, code is organized into **packages**.

### Best Practices for Package Creation

1.  **One Package, One Purpose:** Each package should have a specific purpose. For example, `my_robot_description` (for URDFs), `my_robot_bringup` (for launch files), `my_robot_navigation` (for navigation-related nodes). This keeps the code modular and reusable.
2.  **Declare Dependencies Correctly:** In your `package.xml`, declare all necessary dependencies with `build_depend`, `exec_depend`, and `test_depend` tags. This allows other developers to build your package easily.
3.  **Standard Directories:** Use standard directory names inside your package:
    *   `launch/`: For launch files.
    *   `urdf/` or `description/`: For URDF/Xacro files.
    *   `config/`: For parameter YAML files.
    *   `rviz/`: For RViz configuration files.

### `colcon`: The ROS 2 Build System

`colcon` (collective construction) is the official build tool for ROS 2. It finds the packages in your workspace, checks their dependencies, and builds them in the correct order.

**Some Essential `colcon` Commands:**

*   `colcon build`: Builds the entire workspace.
*   `colcon build --packages-select <pkg_name>`: Builds only a specific package and its dependencies. This is very useful during development.
*   `colcon build --symlink-install`: For Python nodes, this symlinks the source files to the `install` directory instead of copying them. This means you can modify your Python code and you won't need to run `colcon build` again (unless you add new files or entry points).
*   `colcon test`: Runs the automated tests defined in your packages.

At the end of Module 1, you have now covered all the foundational concepts of ROS 2. You can use nodes, topics, services, actions, parameters, URDF models, and launch files to create a complete robotic application.

In the upcoming modules, we will use these same concepts to work on advanced topics like Digital Twins, NVIDIA Isaac Sim, and AI-based control.