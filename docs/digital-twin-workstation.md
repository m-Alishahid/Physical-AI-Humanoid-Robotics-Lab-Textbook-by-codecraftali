---
title: "Setup Guide: Digital Twin Workstation"
sidebar_position: 1
---

# Digital Twin Workstation Setup

This guide will provide detailed, step-by-step instructions for setting up a powerful local workstation for digital twin simulation, including NVIDIA driver installation, Docker, and ROS 2 setup.

A robust local workstation is the cornerstone of modern robotics development, especially when dealing with GPU-intensive tasks like photorealistic simulation, synthetic data generation, and training AI models. This guide provides a complete walkthrough for setting up an Ubuntu-based machine to run NVIDIA Isaac Sim and the ROS 2 ecosystem.

## 1. System Requirements

High-fidelity simulation is computationally expensive. While it's possible to run simpler simulations on lower-end hardware, the following specifications are recommended for a smooth experience with the tools used in this course.

*   **Operating System:** Ubuntu 22.04 LTS
*   **CPU:** 6-core Intel or AMD processor (or better)
*   **RAM:** 32 GB DDR4 (or more)
*   **GPU:** **NVIDIA RTX Series GPU is mandatory.**
    *   **Minimum:** NVIDIA RTX 2070 (8 GB VRAM)
    *   **Recommended:** NVIDIA RTX 3070 / 4070 (or better) with at least 12 GB VRAM.
*   **Storage:** 512 GB NVMe SSD (or larger) for fast loading times.

> **Warning:** An NVIDIA GPU with RTX capabilities is not optional. The simulation tools we will use, like NVIDIA Isaac Sim, rely on real-time ray tracing, which is only available on these cards.

## 2. Initial System Setup

Start with a fresh installation of **Ubuntu 22.04 LTS**.

Once installed, open a terminal (`Ctrl+Alt+T`) and perform a full system update and upgrade. This ensures all your base packages are up-to-date.

```bash
sudo apt update
sudo apt-get upgrade -y
```

Next, install some essential command-line tools.

```bash
sudo apt install -y git curl wget vim build-essential
```

## 3. NVIDIA Driver Installation

This is the most critical step. A correct NVIDIA driver installation is required for the system to recognize and utilize the GPU.

1.  **Check for Recommended Drivers:**
    Ubuntu has a utility to detect your hardware and suggest the appropriate proprietary drivers.

    ```bash
    ubuntu-drivers devices
    ```

    This will output a list of devices and drivers. Look for the entry corresponding to your NVIDIA GPU. It will likely have a `driver : nvidia-driver-XXX - distro non-free (recommended)` line.

2.  **Install the Recommended Driver:**
    You can either install the specific version number or use the `autoinstall` command, which is generally the safest option.

    ```bash
    sudo ubuntu-drivers autoinstall
    ```

3.  **Reboot Your System:**
    A reboot is required to load the new kernel modules for the driver.

    ```bash
    sudo reboot
    ```

4.  **Verify the Installation:**
    After rebooting, open a terminal and run the NVIDIA System Management Interface (`nvidia-smi`).

    ```bash
    nvidia-smi
    ```

    If the installation was successful, you will see a table detailing your GPU name, driver version, and CUDA version. If this command fails, the driver was not installed correctly, and you must debug the issue before proceeding.

## 4. Docker Engine Installation

We will use Docker to run our simulation environment in a clean, containerized way. This avoids cluttering our host system with dependencies.

1.  **Uninstall Old Versions:**
    ```bash
    for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
    ```

2.  **Set up Docker's `apt` Repository:**
    ```bash
    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    ```

3.  **Install Docker Packages:**
    ```bash
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

4.  **Manage Docker as a Non-Root User:**
    To avoid typing `sudo` for every Docker command, add your user to the `docker` group.

    ```bash
    sudo groupadd docker
    sudo usermod -aG docker $USER
    ```
    You will need to **log out and log back in** for this group membership to take effect.

5.  **Verify Docker Installation:**
    After logging back in, open a terminal and run:
    ```bash
    docker run hello-world
    ```
    This should download and run a small test image, confirming that Docker is working correctly.

## 5. NVIDIA Container Toolkit Installation

By default, Docker containers cannot access the host's GPU. The NVIDIA Container Toolkit bridges this gap.

1.  **Set up the Repository:**
    ```bash
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    ```

2.  **Install the Toolkit:**
    ```bash
    sudo apt-get update
    sudo apt-get install -y nvidia-container-toolkit
    ```

3.  **Configure Docker:**
    Restart the Docker daemon to apply the changes.
    ```bash
    sudo systemctl restart docker
    ```

4.  **Verify GPU Access in Docker:**
    Run a container and execute `nvidia-smi` from within it.
    ```bash
    docker run --rm --gpus all nvidia/cuda:12.1.1-base-ubuntu22.04 nvidia-smi
    ```
    This command should output the same `nvidia-smi` table you saw earlier, but this time it's being generated from inside a Docker container. This confirms that your containers can now leverage the power of your NVIDIA GPU.

## 6. ROS 2 Humble Hawksbill Installation

Finally, we install ROS 2, the backbone of our robotics software.

1.  **Set Locale and Add ROS 2 Repository:**
    Follow the official ROS 2 Humble installation instructions.
    ```bash
    sudo apt install software-properties-common
    sudo add-apt-repository universe
    sudo apt update && sudo apt install curl -y
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
    ```

2.  **Install ROS 2 Packages:**
    We will install the `ros-humble-desktop` package, which includes ROS, RViz, demos, and tutorials.
    ```bash
    sudo apt update
    sudo apt install -y ros-humble-desktop
    ```

3.  **Source the Setup File:**
    Add the ROS 2 setup script to your shell's startup file to make ROS 2 commands available in every new terminal.
    ```bash
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
    source ~/.bashrc
    ```

4.  **Verify ROS 2 Installation:**
    Run a simple talker-listener example in two separate terminals.
    *   **Terminal 1:** `ros2 run demo_nodes_cpp talker`
    *   **Terminal 2:** `ros2 run demo_nodes_py listener`

    If you see the talker publishing messages and the listener receiving them, your ROS 2 installation is complete.

Your Digital Twin Workstation is now fully configured and ready for the advanced robotics work in the upcoming modules.