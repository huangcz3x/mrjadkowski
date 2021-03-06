# SMARS-mini-XL
### A small wheeled or tracked robot running on Circuit Python

![Stemma QT board carrier face](https://user-images.githubusercontent.com/81754963/115438428-62a7b580-a1db-11eb-8941-654ec8801648.jpg)

#### I noticed that there has been a bump in traffic the last few days. I would love to have some collaborators on this project. I'm brand new to programming, brand new to CAD, brand new to GitHub, and brand new to 3D printing. About the only exiting skill I bring to this is soldering. Post an issue if you have a suggestion for a change, revise the 3D model, fork the code and improve it if you want, go crazy! I honestly have no idea what I'm doing and I know it can all be done better.

This repository has the 3D models, wiring details, and code for the SMARS mini XL. Currently the code is designed for Circuit Python 6.2.0 running on an Adafruit Feather RP2040. It uses a VL53L0X time-of-flight sensor and an APDS-9960 proximity/gesture/color/light sensor connected with i2c, an DRV8833 h-bridge motor driver, a small lipo, and a SPST switch. The code currently includes basic light seeking behavior while driving forward, obstacle detection and avoidance, and stuck detection that triggers an "unstuck" maneuver.

This project started as a remix of the "SMARS mini" design by [Kevin McAleer](https://www.youtube.com/user/kevinmcaleer28). I don't think it shares a single part with that design anymore, but it was an excellent starting point and gave the project an aesthetic theme that has certainly carried on. Thanks Kevin!

.STL and .STEP files are available in the CAD files folder (probably the most current) and at: https://www.thingiverse.com/thing:4810626

Current hardware BOM (this is the list of parts you need to buy and links to buy them): https://docs.google.com/spreadsheets/d/167UUY43PvzWUNg7vgtmYUr31faELwSrEWL3U5X_r1nM/edit?usp=sharing

The Media folder has a bunch of pictures and videos of various versions of the robot, including pictures of the wiring to see how things are routed.

Current code is running on the 2.x.x hardware setup. For the QT Py version, see the 1.1.0 release

See the Fritzing diagram for wiring.

See the code for the current required libraries; at the moment it requires:

  - adafruit_bus_device
  - adafruit_vl53l0x
  - adafruit_neopixel
  - adafruit_motor
  - adafruit_debouncer
  - adafruit_apds9960

The following parameters can be changed in the setup section of the code to alter the behavior:

  - start_turn_distance: the distance from an obstacle that the robot will stop and begin to pivot right
  - turn_time: the amount of time the robot will pivot to the right once started
  - stop_turn_distance: the distance from an obstacle that the robot will stop pivoting and start driving forward again, assuming turn_time has elapsed
  - abort_turn_time: if the robot has not reached stop_turn_distance in this amount of time while pivoting, it will attempt an unstuck maneuver
  - stuck_variance: if the robot moves less than this distance in 1 second, a stuck_counter event is recorded.

The NeoPixel on the RP2040 is used to show different states. The color codes are:
  - Green: driving forward
  - Red: obstacle detected and turning
  - Blue: stuck event detected, performing unstuck maneuver
  - Bright white: three consecutive unstuck maneuvers have failed

### Upcoming planned releases:
  - 3.0.0: Addition of solar charging, light-seeking behavior, and sleep logic to the 2.0.0 driving behavior. The end goal is to allow the robot to run perpetually, always trying to keep the battery charged as much as possible.
