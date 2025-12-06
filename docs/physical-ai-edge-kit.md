---
title: "Setup Guide: Physical AI Edge Kit"
sidebar_position: 2
---

# Physical AI Edge Kit Setup

This guide will detail the process of flashing and configuring the edge computing device (e.g., NVIDIA Jetson) that will serve as the brain for our physical robot.

While the Digital Twin Workstation is for simulation, the Physical AI Edge Kit is the "brain" that will be deployed on the actual humanoid robot. This is typically a power-efficient, single-board computer with a powerful GPU, such as an **NVIDIA Jetson AGX Orin** or **Jetson Orin Nano**.

This guide provides a general workflow for setting up such a device.

## 1. Hardware Requirements

*   **Edge Device:** NVIDIA Jetson Orin Developer Kit (AGX or Nano).
*   **Power Supply:** The official power supply for your Jetson model.
*   **Storage:** A high-speed microSD card (256GB or larger, U3/A2 rated) or an NVMe SSD for the best performance.
*   **Host PC:** A computer running Ubuntu (20.04 or 22.04) to flash the device.
*   **Cables:** USB-C cable for flashing and recovery mode.

## 2. Flashing with NVIDIA SDK Manager

The most reliable way to set up a Jetson device is by using the NVIDIA SDK Manager on a host PC.

1.  **Download SDK Manager:**
    On your **host PC**, go to the NVIDIA SDK Manager website and download the `.deb` package for your host's Ubuntu version.

2.  **Install SDK Manager:**
    Open a terminal on your host PC and install the downloaded package.
    ```bash
    sudo apt install ./sdkmanager_[version]-[build].deb
    ```

3.  **Run SDK Manager:**
    Launch the SDK Manager from your application menu or via the terminal:
    ```bash
    sdkmanager
    ```

4.  **Login and Select Hardware:**
    *   Log in with your NVIDIA Developer account.
    *   In **Step 01 (Hardware Configuration)**, the SDK Manager should automatically detect your Jetson device if it's connected and in recovery mode. If not, you can manually select your target hardware (e.g., Jetson AGX Orin Devkit).

5.  **Put Jetson in Recovery Mode:**
    *   Ensure the Jetson is powered off.
    *   Connect the host PC to the Jetson's USB-C flashing port.
    *   Press and hold the "Force Recovery" button.
    *   While holding the button, press and release the "Power" button.
    *   You can release the "Force Recovery" button after a few seconds.
    *   On your host PC, run `lsusb`. You should see a device with an ID like `0955:7023 NVIDIA Corp.`.

6.  **Select Software and Flash:**
    *   In **Step 02 (Target Operating System)**, select the latest **JetPack** version. JetPack includes the Linux for Tegra (L4T) OS, CUDA, cuDNN, TensorRT, and other essential libraries.
    *   Choose your desired storage target (microSD or NVMe).
    *   Proceed to **Step 03** and accept the license agreements.
    *   The SDK Manager will download the necessary files and then flash them to the Jetson device. This process can take a significant amount of time.

## 3. Initial Device Configuration

After flashing is complete, the Jetson will reboot. Connect a monitor, keyboard, and mouse to complete the standard Ubuntu OEM configuration, where you will set your username, password, timezone, etc.

## 4. Post-Installation Setup

Once you have a desktop environment on the Jetson, open a terminal and perform the same essential setup as on the workstation:

*   **Install ROS 2 Humble:** The process is identical to the workstation setup. The Jetson's L4T OS is based on Ubuntu, so the standard ROS 2 installation instructions will work.
*   **Install Essential Tools:** `sudo apt install git curl vim build-essential`.
*   **Configure Networking:** Ensure the Jetson is connected to the same network as your workstation for seamless ROS 2 communication.

Your Physical AI Edge Kit is now ready to run the control software for your robot and communicate with your digital twin environment.