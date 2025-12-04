# Research Findings: ROS 2 Textbook Module 1

## ROS 2 Distribution Selection

**Decision**: Jazzy Jalisco

**Rationale**: Jazzy Jalisco is a Long Term Support (LTS) distribution supported until May 2029. This provides a stable and consistent platform for a textbook, ensuring examples and tutorials remain functional and relevant for an extended period, reducing the need for frequent updates due to breaking changes. While Humble Hawksbill is also an LTS, Jazzy offers longer support, which is beneficial for educational materials.

**Alternatives Considered**: Humble Hawksbill (shorter support duration, but also an LTS).

## AI Agent Libraries for ROS 2 Integration

**Decision**: A combination of general-purpose and specialized Python libraries.

**Rationale**: Integrating AI agents with ROS 2 involves diverse functionalities like simulation, perception, planning, control, and machine learning. A flexible approach using a combination of libraries will provide comprehensive coverage for Chapter 4.

**Key Library Categories and Examples**:
- **Simulation**: PyBullet
- **Reinforcement Learning**: Stable Baselines, RLlib
- **ROS-enabled AI/RL**: `ros2learn`
- **Perception**: `pclpy`, OpenCV
- **Motion Planning**: `sparse-rrt`, OMPL
- **Kinematics/Control**: `Pybotics`, `Kinpy`

**Alternatives Considered**: Relying on a single, monolithic AI framework, which would limit flexibility and breadth of topics.

## ROS 2 Testing Frameworks

**Decision**: `pytest` for unit testing and `launch_testing` for integration testing, with consideration for `ros2-easy-test` for simplified assertions.

**Rationale**: This combination provides a robust and comprehensive testing strategy. `pytest` is a powerful and widely adopted Python framework for unit tests, ensuring individual components work correctly. `launch_testing` is the official ROS 2 framework for integration tests, essential for verifying interactions between multiple nodes and entire systems. `ros2-easy-test` offers a more user-friendly approach for expressive assertions in integration scenarios.

**Alternatives Considered**: Solely relying on `unittest` (less feature-rich than `pytest`) or only using `launch_testing` (might be overkill for simple unit tests).
