---
title: "Chapter 4: URDF for Robot Modeling"
sidebar_position: 4
---

# Chapter 4: URDF for Robot Modeling

So far, we have understood the methods of communication between ROS 2 nodes. But a robot is not just a collection of software nodes; it has a physical structure. To represent this physical structure in the ROS 2 ecosystem, we use the **Unified Robot Description Format (URDF)**.

This chapter will teach you how to create a 3D model of your robot using URDF, which can then be used for simulation, visualization, and control.

## What is URDF?

URDF is an XML-based file format used to describe the kinematic and dynamic properties of a robot. It includes:
*   All the rigid parts of the robot, called **links**.
*   The **joints** that connect these links.
*   The visual aspects of the links (how they look).
*   The collision properties of the links (for impacts in simulation).
*   The physical properties of the links, such as mass and inertia.

Once you have created a URDF for your robot, ROS 2 tools like RViz2 can visualize it in 3D, simulators like Gazebo can simulate it, and nodes like `robot_state_publisher` can broadcast its structure as a transform tree (`/tf`).

## Core Components of URDF

A URDF file is always enclosed within a `<robot>` tag. Its main components are `<link>` and `<joint>`.

### `<link>`

A link represents a rigid body part of the robot. Each link must have a unique name. A link can have three main sub-tags: `<visual>`, `<collision>`, and `<inertial>`.

```xml
<link name="base_link">
  <visual>
    <geometry>
      <box size="0.6 0.4 0.2" />
    </geometry>
    <origin xyz="0 0 0.1" rpy="0 0 0" />
    <material name="grey">
      <color rgba="0.5 0.5 0.5 1.0" />
    </material>
  </visual>
  
  <collision>
    <geometry>
      <box size="0.6 0.4 0.2" />
    </geometry>
    <origin xyz="0 0 0.1" rpy="0 0 0" />
  </collision>
  
  <inertial>
    <mass value="5.0" />
    <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1" />
    <origin xyz="0 0 0.1" rpy="0 0 0" />
  </inertial>
</link>
```

*   **`<visual>`**: Describes how the link will look in tools like RViz.
    *   `<geometry>`: The shape of the link. This can be a `<box>`, `<cylinder>`, `<sphere>`, or a `<mesh filename="..."/>` for an external 3D model.
    *   `<origin>`: The offset and orientation of the visual geometry with respect to the link's origin frame.
    *   `<material>`: The color or texture of the link.
*   **`<collision>`**: Defines the link's collision geometry for physics simulation. Often, the collision geometry is simpler than the visual geometry to improve performance.
*   **`<inertial>`**: Defines the dynamic properties of the link.
    *   `<mass>`: The mass of the link (in kilograms).
    *   `<inertia>`: The 3x3 inertia matrix, which describes the link's resistance to rotation.

### `<joint>`

A joint connects two links and defines the relative motion between them.

```xml
<joint name="base_to_arm_joint" type="revolute">
  <parent link="base_link" />
  <child link="arm_link_1" />
  <origin xyz="0.25 0 0.2" rpy="0 0 0" />
  <axis xyz="0 0 1" />
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0" />
</joint>
```

*   **`name` and `type`**: Each joint has a unique name and a type. The main joint types are:
    *   `revolute`: Rotates around an axis (e.g., an elbow joint). It has limits.
    *   `continuous`: Rotates continuously around an axis (e.g., a wheel). It has no limits.
    *   `prismatic`: Slides along an axis (e.g., a piston). It has limits.
    *   `fixed`: Rigidly connects two links. There is no motion.
    *   `floating`: Allows 6-DoF motion between two links.
    *   `planar`: Allows motion on a plane.
*   **`<parent>` and `<child>`**: Specifies which two links the joint connects, forming a kinematic tree.
*   **`<origin>`**: The transform from the parent link's origin to the joint's origin.
*   **`<axis>`**: The axis of motion for the joint (for rotation or translation).
*   **`<limit>`**: For `revolute` and `prismatic` joints, defines the range of motion (`lower`, `upper`), maximum effort, and maximum velocity.

## Xacro: Better URDFs with Macros

As a robot becomes more complex, the URDF file can become very long and repetitive. To solve this problem, we use **Xacro (XML Macros)**. Xacro allows you to create modular and more readable URDF files by using constants, mathematical expressions, and macros.

A Xacro file is converted into a standard `.urdf` file using the `xacro` command.

### Key Features of Xacro

1.  **Properties (Constants):**
    ```xml
    <xacro:property name="wheel_radius" value="0.1" />
    <xacro:property name="wheel_mass" value="0.5" />
    
    <mass value="${wheel_mass}" />
    <cylinder radius="${wheel_radius}" length="0.05" />
    ```
    This makes it easy to define values in one place and use them throughout the file.

2.  **Mathematical Expressions:**
    ```xml
    <xacro:property name="base_height" value="0.2" />
    <xacro:property name="wheel_radius" value="0.1" />
    
    <origin xyz="0 0 ${base_height / 2 + wheel_radius}" />
    ```

3.  **Macros:**
    Macros let you create reusable blocks of code. This is the most powerful feature for complex robots.

    ```xml
    <xacro:macro name="default_inertial" params="mass">
      <inertial>
        <mass value="${mass}" />
        <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01" />
      </inertial>
    </xacro:macro>
    
    <!-- Calling the macro -->
    <xacro:default_inertial mass="2.0" />
    ```

## Practical Example: A Simple 2-DOF Robot Arm

Let's create a `.urdf.xacro` file for a simple 2-DOF (Degrees of Freedom) robot arm.

Create the file `robotics_lab_pkg/urdf/simple_arm.urdf.xacro`:

```xml
<?xml version="1.0"?>
<robot name="simple_arm" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Constants -->
  <xacro:property name="PI" value="3.1415926535897931"/>
  <xacro:property name="base_link_mass" value="2.0" />
  <xacro:property name="link_1_mass" value="1.0" />
  <xacro:property name="link_2_mass" value="0.5" />

  <!-- Inertial Macro -->
  <xacro:macro name="default_inertial" params="mass">
    <inertial>
      <mass value="${mass}" />
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01" />
    </inertial>
  </xacro:macro>

  <!-- ******************* LINKS ******************* -->

  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry><cylinder length="0.05" radius="0.1"/></geometry>
      <material name="grey"><color rgba="0.5 0.5 0.5 1"/></material>
    </visual>
    <collision><geometry><cylinder length="0.05" radius="0.1"/></geometry></collision>
    <xacro:default_inertial mass="${base_link_mass}" />
  </link>

  <!-- Link 1 -->
  <link name="link_1">
    <visual>
      <geometry><box size="0.5 0.05 0.05"/></geometry>
      <origin xyz="0.25 0 0" rpy="0 0 0"/>
      <material name="blue"><color rgba="0 0 1 1"/></material>
    </visual>
    <collision><geometry><box size="0.5 0.05 0.05"/></geometry><origin xyz="0.25 0 0" rpy="0 0 0"/></collision>
    <xacro:default_inertial mass="${link_1_mass}" />
  </link>

  <!-- Link 2 -->
  <link name="link_2">
    <visual>
      <geometry><box size="0.4 0.05 0.05"/></geometry>
      <origin xyz="0.2 0 0" rpy="0 0 0"/>
      <material name="green"><color rgba="0 1 0 1"/></material>
    </visual>
    <collision><geometry><box size="0.4 0.05 0.05"/></geometry><origin xyz="0.2 0 0" rpy="0 0 0"/></collision>
    <xacro:default_inertial mass="${link_2_mass}" />
  </link>

  <!-- ******************* JOINTS ******************* -->

  <!-- Base to Link 1 Joint -->
  <joint name="joint_1" type="revolute">
    <parent link="base_link"/>
    <child link="link_1"/>
    <origin xyz="0 0 0.025" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-${PI/2}" upper="${PI/2}" effort="100" velocity="1.0"/>
  </joint>

  <!-- Link 1 to Link 2 Joint -->
  <joint name="joint_2" type="revolute">
    <parent link="link_1"/>
    <child link="link_2"/>
    <origin xyz="0.5 0 0" rpy="0 ${PI/2} 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-${PI/2}" upper="${PI/2}" effort="100" velocity="1.0"/>
  </joint>

</robot>
```

## Visualizing the Robot Model

Now that we have the URDF file, we can view it in RViz2. For this, we need three nodes:

1.  **`robot_state_publisher`**: This node reads the URDF file and, based on the robot's joint states (from the `/joint_states` topic), publishes the transforms (`/tf`) between the links.
2.  **`joint_state_publisher_gui`**: This provides a GUI tool that allows us to manually control the joint angles. It publishes joint values on the `/joint_states` topic.
3.  **`rviz2`**: The visualization tool.

To launch all of these together, we will create a launch file. This is the topic of the next chapter, but here is a preview:

`robotics_lab_pkg/launch/display_arm.launch.py`
```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_path = get_package_share_directory('robotics_lab_pkg')
    urdf_file_path = os.path.join(pkg_path, 'urdf', 'simple_arm.urdf.xacro')
    
    # Process the xacro file to generate URDF
    robot_description_raw = xacro.process_file(urdf_file_path).toxml()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_raw}]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', os.path.join(pkg_path, 'rviz', 'urdf_config.rviz')]
        )
    ])
```

By running this launch file (and after installing the necessary packages), you will see a 3D model in RViz. You can move the arm by moving the sliders in the `joint_state_publisher_gui`.

In this chapter, you learned how to represent a robot's physical structure in code using URDF and Xacro. This is a very important step, as this robot model is now ready for simulation, motion planning, and control. In the next chapter, we will learn about launch files in detail so that we can easily manage such complex, multi-node applications.