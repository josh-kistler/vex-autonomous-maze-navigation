# VEX Autonomous Maze Navigation

An autonomous maze-navigation robot built with **VEX EXP** and programmed in **Python**.

The robot was designed to navigate an unknown maze without relying on a predetermined sequence of turns. The final system used reactive wall following, proximity sensing, obstacle avoidance, and collision-recovery behavior to balance traversal speed with reliability.

Developed as a **three-person robotics team project**.

## Performance

In the final maze competition, the robot:

- Completed an unknown maze in **1 minute 1 second**
- Recorded **4 wall collisions**
- Received a final scored time of **1 minute 5 seconds**
- Finished **2nd overall**

The competition added a one-second penalty for every collision, so the control system was tuned to balance speed against navigation accuracy.

## System Overview

The final robot used a compact four-wheel VEX EXP chassis equipped with:

- Four drive motors
- Side-mounted distance sensor
- Front optical proximity sensor
- Mechanical bumper sensor
- Inertial sensing
- VEX EXP Brain

The chassis was intentionally kept narrow to reduce the likelihood of wall collisions while retaining enough structural stability for reliable sensor measurements.

## Navigation Strategy

An earlier version of the project explored a more complex navigation strategy involving:

- Detecting open paths
- Tracking previously visited directions
- Maintaining an estimate of the robot's position
- Searching for the maze's exit light

Testing showed that this approach depended too heavily on consistently accurate sensor measurements.

The final design therefore shifted to a more robust **reactive wall-following algorithm**.

Rather than constructing a map, the robot continuously responded to its immediate surroundings.

## Wall Following

The robot maintains a target distance from a selected maze wall using the side-mounted distance sensor.

The controller calculates an error between the measured wall distance and the desired offset and adjusts the relative drive-motor velocities to steer the robot:

```text
Distance Sensor
      ↓
Measured Wall Distance
      ↓
Target Distance Comparison
      ↓
Steering Correction
      ↓
Left / Right Motor Velocities
```

If the robot moves too far from the wall, the drivetrain arcs toward it.

If it moves too close, the drivetrain steers away.

Separate control routines support both **left-wall** and **right-wall** following so the sensor configuration can be adapted to the maze layout.

## Obstacle Avoidance

A front-mounted optical sensor continuously checks for obstacles in the robot's path.

When an obstacle is detected, the program determines whether the robot should continue following an available opening or execute a turn to avoid the wall.

Turn behavior uses motor control and inertial measurements to help reorient the robot before navigation resumes.

## Collision Recovery

The bumper sensor acts as a final failsafe when proximity sensing does not prevent a collision.

When triggered, the robot reverses and adjusts its position before returning to the normal maze-solving loop.

This created multiple layers of collision handling:

1. Distance-based wall correction
2. Optical obstacle detection
3. Bumper-based physical collision recovery

## Control Loop

The autonomous navigation system repeatedly:

1. Reads the distance, optical, bumper, and inertial sensors.
2. Checks for a physical collision.
3. Executes recovery behavior if necessary.
4. Checks for an obstacle ahead.
5. Determines whether a turn is necessary.
6. Adjusts motor velocities to maintain the desired wall distance.
7. Repeats until the maze is completed.

## Tuning

A significant part of development involved experimentally tuning values controlling:

- Base driving speed
- Target distance from the wall
- Steering correction strength
- Corner-detection threshold
- Turn speed
- Turn duration
- Close-wall correction

Repeated physical testing was necessary because aggressive settings improved traversal speed but could reduce sensor reliability and increase collisions.

## Technologies

- Python
- VEX EXP
- VEXcode
- Autonomous robotics
- Reactive control
- Distance sensing
- Optical sensing
- Inertial sensing
- Obstacle avoidance
- Sensor-based navigation

## Project Structure

```text
vex-autonomous-maze-navigation/
├── README.md
├── src/
│   └── maze_navigation.py
├── vexcode/
│   └── maze_navigation.exppython
└── docs/
    └── images/
```

The `.exppython` project contains the original VEXcode project configuration, while the Python source is provided separately for easier inspection on GitHub.

## Key Takeaway

This project demonstrated that the most sophisticated navigation strategy is not necessarily the most effective one on real hardware.

A simpler reactive controller, combined with careful mechanical design, sensor placement, fallback behaviors, and iterative tuning, produced a faster and more reliable system than the team's initial map-based approach.
