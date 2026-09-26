# TrackShield – AI-Powered Railway Safety Monitoring Framework

## 📌 Project Overview

**TrackShield** is an AI-powered railway safety monitoring system designed to detect foreign objects and potential obstacles on railway tracks.

The system uses **YOLO and OpenCV** for object detection and **Django** for web application development. When a potential risk is detected, the system can generate alerts for the responsible users, helping improve railway track safety and monitoring.

## 🎯 Objectives

- Detect objects and obstacles on railway tracks.
- Identify potential safety risks using AI-based object detection.
- Provide alerts when a dangerous object is detected.
- Maintain information about trains, loco pilots, and cameras.
- Provide a web-based platform for monitoring and management.
- Maintain detection and alert history.

## 🛠️ Technologies Used

- **Python**
- **Django**
- **YOLO**
- **OpenCV**
- **MySQL**
- **HTML**
- **CSS**
- **JavaScript**
- **Bootstrap**

## ✨ Key Features

### Admin Module

- Admin Login
- Manage Trains
- Manage Loco Pilots
- Manage Cameras
- Add Awareness Notifications
- View Detection/Alert History
- Manage Complaints and Replies

### Loco Pilot Module

- Loco Pilot Login
- View Live Alerts
- View Camera Feed
- View Safety Awareness Information
- Submit Complaints
- Receive Replies
- Chatbot Assistance

### AI Detection

The system uses **YOLO-based object detection** with **OpenCV** to identify possible obstacles such as:

- Humans
- Animals
- Vehicles
- Foreign objects
- Debris

Detected objects can be evaluated according to their potential risk level and used to generate safety alerts.

## 🔄 How the System Works

```text
Camera / Video Feed
        ↓
     OpenCV
        ↓
   YOLO Detection
        ↓
Object / Obstacle Detection
        ↓
    Risk Assessment
        ↓
    Safety Alert
        ↓
Loco Pilot / Admin
```

## 📂 Main Modules

### Admin

- Login
- Train Management
- Loco Pilot Management
- Camera Management
- Awareness Management
- Alert History
- Complaint Management

### Loco Pilot

- Login
- Live Alerts
- Camera Feed
- Awareness
- Complaints
- Chatbot Assistance

## 🗄️ Database

The project uses **MySQL** for storing application data.

Some of the major data entities include:

- Train
- Loco Pilot
- Camera
- Complaint
- Awareness Notification
- Camera Alert

## 📸 Screenshots

### 🔐 Login Page

[![Login Page](Screenshot%202026-03-24%20203845.png)](Screenshot%202026-03-24%20203845.png)

### 📊 Admin Dashboard

[![Admin Dashboard](Screenshot%202026-03-24%20204257.png)](Screenshot%202026-03-24%20204257.png)

### 🚂 Loco Pilot Dashboard

[![Loco Pilot Dashboard](Screenshot%202026-03-24%20204727.png)](Screenshot%202026-03-24%20204727.png)

### 📹 Camera Feed

[![Camera Feed](Screenshot%202026-03-24%20205110.png)](Screenshot%202026-03-24%20205110.png)

### 🤖 Object Detection

[![Object Detection](Screenshot%202026-03-25%20120945.png)](Screenshot%202026-03-25%20120945.png)

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Athisaya99/TrackShield.git
```

### 2. Open the project folder

```bash
cd TrackShield
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install required packages

```bash
pip install -r requirements.txt
```

If a `requirements.txt` file is not available yet, create one after installing the required Python packages.

### 6. Configure MySQL

Create the required MySQL database and update the Django database configuration with your MySQL username, password, and database name.

### 7. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Start the Django server

```bash
python manage.py runserver
```

Open the application in your browser using the local Django server address.

## 🚀 Future Enhancements

- Real-time railway track monitoring using multiple cameras.
- Improved object detection accuracy.
- Integration with railway control-room systems.
- Mobile notifications for emergency alerts.
- Improved risk prediction using additional AI models.
- Cloud-based monitoring and data storage.

## 👩‍💻 Developer

**Athisaya K S**

MCA Graduate | Aspiring Python Full Stack Developer

### Project

**TrackShield – AI-Powered Railway Safety Monitoring Framework**

Technologies: **Python | Django | YOLO | OpenCV | MySQL**
