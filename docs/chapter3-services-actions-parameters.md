---
title: "Chapter 3: Services, Actions, and Parameters"
---

# Chapter 3: Services, Actions, and Parameters

In the previous chapter, we mastered ROS 2's most common communication pattern, the publish/subscribe model, using Topics. This is excellent for continuous data streams, such as sensor readings. However, in robotics, we often need other types of interactions:

1.  **Request/Response:** Asking one node to perform a task and waiting for it to complete (e.g., "Capture an image and send it to me").
2.  **Long-Running Tasks:** Asking a node to start a long task, tracking its progress, and being able to cancel it mid-execution (e.g., "Navigate to coordinates X, Y").
3.  **External Configuration:** Modifying a node's behavior without recompiling code (e.g., setting a robot's wheel diameter).

This chapter covers three key ROS 2 concepts that fulfill these needs: **Services**, **Actions**, and **Parameters**.

## 1. Services: Synchronous Request/Response

A **Service** is a strict request/response communication pattern, similar to a Remote Procedure Call (RPC). A **client** node sends a request and blocks (waits) until the **server** node processes the request and sends back a response.

**When to use Services:**
*   For tasks that complete quickly.
*   When you need confirmation that an action has been completed.
*   Examples: Resetting odometry, changing a specific camera setting, or clearing the map in a navigation system.

### Defining a Custom Service

Like Topics, Services also use data types, which are defined in `.srv` files. A `.srv` file has two parts, separated by `---`: the request and the response.

Let's define a service in our `robotics_lab_pkg` package that adds two integers.

1.  **Create the directory:**
    ```bash
    cd ~/ros2_ws/src/robotics_lab_pkg
    mkdir srv
    ```

2.  **Create the `.srv` file:**
    Create a file named `srv/AddTwoInts.srv` and add the following content:
    ```
    int64 a
    int64 b
    ---
    int64 sum
    ```

3.  **Update `CMakeLists.txt` and `package.xml`:**
    To inform ROS 2 about this new service definition, you must modify the build files.

    **In `package.xml`:**
    ```xml
    <build_depend>rosidl_default_generators</build_depend>
    <exec_depend>rosidl_default_runtime</exec_depend>
    <member_of_group>rosidl_interface_packages</member_of_group>
    ```

    **In `CMakeLists.txt`:**
    ```cmake
    find_package(rosidl_default_generators REQUIRED)

    rosidl_generate_interfaces(${PROJECT_NAME}
      "srv/AddTwoInts.srv"
    )
    ```

Now, when you run `colcon build`, ROS 2 will generate the necessary Python and C++ code for this `.srv` file.

### Service Server (Provider)

The server is the node that provides the service. It waits for requests, processes them, and sends a response.

#### Python Service Server

Create the file `robotics_lab_pkg/py_nodes/add_two_ints_server.py`:

```python
# add_two_ints_server.py
import rclpy
from rclpy.node import Node
from robotics_lab_pkg.srv import AddTwoInts

class AddTwoIntsServer(Node):
    def __init__(self):
        super().__init__('add_two_ints_server_node')
        # 1. Create a service
        self.srv = self.create_service(
            AddTwoInts, 
            'add_two_ints', 
            self.add_two_ints_callback)
        self.get_logger().info('Add Two Ints Service is ready.')

    def add_two_ints_callback(self, request, response):
        # 2. Process the request
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}. Sending back sum={response.sum}')
        
        # 3. Return the response
        return response

def main(args=None):
    rclpy.init(args=args)
    server_node = AddTwoIntsServer()
    rclpy.spin(server_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Code Breakdown:**
1.  `self.create_service()`: Creates a service. We pass the service type (`AddTwoInts`), the service name (`add_two_ints`), and a callback function.
2.  `add_two_ints_callback`: This function is called for every request. It has two arguments: `request` (the data from the client) and `response` (which we need to fill).
3.  `return response`: Returning the response object from the callback causes `rclpy` to send it back to the client.

### Service Client (Caller)

The client is the node that calls the service.

#### Python Service Client

Create the file `robotics_lab_pkg/py_nodes/add_two_ints_client.py`:

```python
# add_two_ints_client.py
import sys
import rclpy
from rclpy.node import Node
from robotics_lab_pkg.srv import AddTwoInts

class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client_node')
        # 1. Create a client
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        
        # 2. Wait for the service to be available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        
        # 3. Create a request object
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        # 4. Call the service asynchronously
        self.future = self.client.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        # 5. Get the result
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    client_node = AddTwoIntsClient()
    
    if len(sys.argv) != 3:
        client_node.get_logger().info('Usage: ros2 run robotics_lab_pkg add_two_ints_client <int> <int>')
        return

    a = int(sys.argv[1])
    b = int(sys.argv[2])
    
    client_node.get_logger().info(f'Requesting sum of {a} and {b}')
    response = client_node.send_request(a, b)
    
    if response:
        client_node.get_logger().info(f'Result of add_two_ints: {response.sum}')
    else:
        client_node.get_logger().error('Service call failed')

    client_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Code Breakdown:**
1.  `self.create_client()`: Creates a client interface for the service.
2.  `self.client.wait_for_service()`: This is a crucial step. The client should wait for the server to come online.
3.  `AddTwoInts.Request()`: Creates a request object from the service type.
4.  `self.client.call_async()`: Calls the service asynchronously. It returns a "future" object, which is a placeholder for the response.
5.  `rclpy.spin_until_future_complete()`: Blocks the program here until the future (the response) is completed.

*(The C++ implementation for services is very similar, using `create_service`, `create_client`, and `async_send_request`.)*

## 2. Actions: Asynchronous, Goal-Oriented Tasks

When a task is long-running, using a service is not ideal because the client will be blocked. Furthermore, we might need to track the task's progress or cancel it. **Actions** are designed for all these scenarios.

An Action has three parts:
1.  **Goal:** The client tells the server what to do (e.g., "Navigate to position X,Y").
2.  **Feedback:** The server sends periodic updates to the client during execution (e.g., "I am 5 meters away from the goal").
3.  **Result:** When the task is complete, the server sends a final result (e.g., "Reached the goal").

### Defining a Custom Action

Actions are defined in `.action` files. They have three sections, separated by `---`: Goal, Result, and Feedback.

Let's create a `Fibonacci.action`.

1.  **Create the directory:** `mkdir -p ~/ros2_ws/src/robotics_lab_pkg/action`
2.  **Create the `.action` file:** `action/Fibonacci.action`
    ```
    # Goal
    int32 order
    ---
    # Result
    int32[] sequence
    ---
    # Feedback
    int32[] partial_sequence
    ```

After this, `CMakeLists.txt` and `package.xml` must be updated just like for services, but with the `.action` filename instead of `.srv`.

### Action Server

An action server handles goal requests.

#### Python Action Server

Create `robotics_lab_pkg/py_nodes/fibonacci_action_server.py`:

```python
# fibonacci_action_server.py
import time
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from robotics_lab_pkg.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)
        self.get_logger().info("Fibonacci Action Server is ready.")

    def goal_callback(self, goal_request):
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1])
            
            self.get_logger().info(f'Publishing feedback: {feedback_msg.partial_sequence}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result

def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionServer()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
```

**Code Breakdown:**
*   `ActionServer`: In its constructor, we define the action type, action name, and three callbacks.
*   `goal_callback`: To accept or reject a new goal.
*   `cancel_callback`: To accept or reject a cancellation request.
*   `execute_callback`: This `async` function executes the goal.
    *   `goal_handle.is_cancel_requested`: Checks if the client has requested to cancel the goal.
    *   `goal_handle.publish_feedback()`: Sends feedback to the client.
    *   `goal_handle.succeed()`: Sets the state to successful upon goal completion.
    *   `return Fibonacci.Result()`: Returns the final result.

### Action Client

The action client sends the goal and receives feedback/results.

#### Python Action Client

Create `robotics_lab_pkg/py_nodes/fibonacci_action_client.py`:

```python
# fibonacci_action_client.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from robotics_lab_pkg.action import Fibonacci

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback.partial_sequence}')

    def send_goal(self, order):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.get_logger().info('Sending goal request...')
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

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
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()
    
    if len(sys.argv) != 2:
        action_client.get_logger().info('Usage: ros2 run robotics_lab_pkg fibonacci_action_client <order>')
        return

    order = int(sys.argv[1])
    action_client.send_goal(order)

    rclpy.spin(action_client)

if __name__ == '__main__':
    main()