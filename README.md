# Earthquake Emergency Response Robots

## Introduction
Welcome to the Earthquake Emergency Response Robots project! This project aims to create, develop, and implement systems specifically designed to handle post-earthquake situations using adaptable robots equipped with sensors and communication capabilities.

## Project Overview
The Earthquake Emergency Response Robots project is a capstone project undertaken by a team of 8 individuals. The main focus of this project is to build adaptable robots capable of post-earthquake response tasks. These robots are equipped with various sensors and communication capabilities to aid in their operations.

## Features
- **Route Optimization**: Utilizes the A* algorithm to optimize routes for efficient navigation in post-earthquake scenarios.
- **Voice Detection**: Enables the robot to recognize voice commands for enhanced interaction and control.
- **Object Detection**: Utilizes YOLO (You Only Look Once) for real-time object detection, allowing the robot to identify and respond to objects in its environment.
- **Building Damage Classification**: Utilizes Convolutional Neural Networks (CNN) to classify building damage, providing valuable information for rescue operations.

## Hardware Components
- Raspberry Pi 5 (8GB) as the core controller.
- Camera for capturing visual data.
- Microphone for voice detection.
- PIR Sensor for detecting motion.
- Neo-6m GPS Module for location tracking.
- 2 DC Motors for movement.
- L298N Voltage Regulator for power management.
- 4 Batteries for powering the system.

## Tech Stacks
- **Python**: The primary programming language used for development.
- **Django**: Used for building the web application framework.
- **Apache Server**: Hosting the web application.
- **PostgreSQL**: Relational database for storing structured data.
- **MongoDB**: NoSQL database for storing unstructured data.
- **Apache Airflow**: Used for orchestrating workflows and scheduling tasks.
- **Docker**: Used for containerization to ensure consistent deployment across different environments.

## Getting Started
1. Clone the repository from [GitHub](https://github.com/erogluegemen/Earthquake-Emergency-Response-Robots).
2. Install the necessary dependencies listed in the `requirements.txt` file.
3. Set up the hardware components as described in the documentation.
4. Configure the settings according to your environment (e.g., database configurations, API keys).
5. Run the Django server using the `python manage.py runserver` command.
6. Access the web application from your browser at `http://localhost:8000`.

## Contributing
We welcome contributions from the community. If you're interested in contributing to the Earthquake Emergency Response Robots project, please follow these guidelines:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and ensure the code passes all tests.
- Submit a pull request detailing your changes.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contact
For any inquiries or feedback, please contact the project team at: <br>
[@Egemen Eroglu](https://github.com/erogluegemen) <br>
[@Ece Akdeniz](https://github.com/ece-akdeniz) 
