# Quickstart Guide: Robotic Nervous System (ROS 2) Textbook Module 1

This guide provides a quick overview to get you started with Module 1 of 'The Robotic Nervous System (ROS 2) for Physical AI' textbook. It covers essential setup steps and how to interact with the textbook's interactive features.

## 1. Setting up Your Development Environment

To make the most of this textbook, you'll need a ROS 2 development environment. We primarily target **Ubuntu 22.04 LTS (Jammy Jellyfish)** with **ROS 2 Jazzy Jalisco**.

### Recommended Setup Steps:

1.  **Install Ubuntu 22.04 LTS**: If you don't already have it, install Ubuntu 22.04 LTS on a virtual machine (e.g., VirtualBox, VMware) or as a dual-boot alongside your existing operating system.
2.  **Install ROS 2 Jazzy Jalisco**: Follow the official ROS 2 documentation for installing Jazzy Jalisco on Ubuntu. Ensure you choose the "Desktop" installation for full features.
    ```bash
    # Example (refer to official docs for precise commands):
    sudo apt update && sudo apt install locales
    sudo locale-gen en_US en_US.UTF-8
    sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
    export LANG=en_US.UTF-8

    sudo apt install software-properties-common
    sudo add-apt-repository universe

    sudo apt update && sudo apt install curl -y
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

    sudo apt update
    sudo apt install ros-jazzy-desktop
    # Source the setup script
    source /opt/ros/jazzy/setup.bash
    ```
3.  **Install Python 3 and Pip**: Ensure you have Python 3.8+ and pip installed.
    ```bash
    sudo apt install python3 python3-pip
    ```
4.  **Create a ROS 2 Workspace**: A workspace is where you'll store your ROS 2 packages.
    ```bash
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws
    colcon build
    source install/setup.bash
    ```

## 2. Navigating the Textbook Content

The textbook content is organized into modules and chapters. Each chapter is presented in markdown files (`.md`) and includes:

-   **Theory**: Explanations of concepts.
-   **Diagrams**: Visual aids.
-   **Code Examples**: Python code snippets.
-   **Hands-on Exercises**: Practical tasks.
-   **Personalization Sections**: Prompts to apply concepts to your projects.

### Running Code Examples

Code examples are provided as standalone Python files (e.g., `code_examples/chapter1/publisher_node.py`).

1.  **Navigate to your workspace**: `cd ~/ros2_ws`
2.  **Source ROS 2 setup**: `source /opt/ros/jazzy/setup.bash` (if not already sourced)
3.  **Run the example**: `python3 path/to/code_examples/chapter1/publisher_node.py`

Some examples might require launching ROS 2 nodes in separate terminals using `ros2 run` or `ros2 launch`. Instructions will be provided within the chapter content.

## 3. Interacting with the RAG Chatbot

Throughout the textbook, you will find `<!-- RAG_INTEGRATION_POINT: [topic] -->` markers. These indicate sections where you can engage with the RAG chatbot for deeper understanding, definitions, or Q&A.

### How to Use:

-   **Highlight text**: In an interactive reading environment, highlighting a section near a RAG marker will send the `context_snippet` to the chatbot.
-   **Ask questions**: You can directly ask the chatbot questions related to the current topic.

The chatbot will provide a response and link back to relevant sections of the textbook for verification.

## 4. Urdu Translations

Key technical terms are accompanied by inline Urdu translation tags, e.g., `[Term in English]<urdu_tag>اردو ترجمہ</urdu_tag>`. This feature aims to enhance accessibility for Urdu-speaking learners.

