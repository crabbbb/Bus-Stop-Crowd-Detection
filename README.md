# Bus Stop Crowd Detection System

The **Bus Stop Crowd Detection System** is designed to provide real-time information on bus schedules, crowd sizes, and bus capacity. This system uses advanced AI models like YOLOv8 for object detection and offers features like bus schedule management, wait time estimation, and real-time crowd monitoring to enhance decision-making and reduce uncertainty for bus passengers.

## Features

- Real-time crowd detection and queue estimation
- Bus schedule and route management
- Capacity monitoring for efficient bus utilization
- Dynamic and interactive user interface
- Integrated with MongoDB for scalable data management

## Prerequisites

Before installing and running the project, ensure you have the following installed:

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- MongoDB 

## Installation

Follow these steps to set up the project:

### Backend (Django)

1. **Clone the repository**:
    ```bash
    git clone https://github.com/crabbbb/Bus-Stop-Crowd-Detection.git
    ```

2. **Set up a virtual environment**:
    ```bash
    python -m venv myenv # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    cd /path/to/project/file/
    pip install -r requirements.txt
    ```

4. **Configure environment variables**:
    - Create a `.env` file put under Bus-Stop-Crowd-Detection/src/backend/config
    - Add the following variables:
        ```env
        <!-- env file template -->
        <!-- for MongoDB -->
        DB_USER=
        DB_PASSWORD=
        <!-- for train model use -->
        ROBOTFLOW_DATASET_APIKEY=
        GITHUB_ACCESS_TOKEN=
        ```

5. **Run migrations**:
    ```bash
    cd src/backend
    python manage.py migrate
    ```

6. **Start the server**:
    ```bash
    python manage.py runserver
    ```

### Frontend (React.js)

1. **Navigate to the frontend directory**:
    ```bash
    cd src/frontend
    ```

2. **Install dependencies**:
    ```bash
    npm install
    ```

3. **Start the development server**:
    ```bash
    npm start
    ```

### Database Setup (MongoDB)

- MongoDB Atlas:
    - Create a cluster in MongoDB Atlas.
    - Add your IP to the IP whitelist.
    - Add your username and password to `.env` file

### Running the System

1. Start the backend server as described in the Backend section.
2. Start the frontend server as described in the Frontend section.
3. Access the application in your browser at `http://localhost:3000`.

# Future improvement
- WebSocket
    - Resource 1 : [Real-Time Progress Bar using Django Channels, React, and WebSockets](https://medium.com/@martindegesus1/real-time-progress-bar-using-django-channels-react-and-websockets-7845342418d6)
        - [GitHub Repo](https://github.com/martindegesus/django-channels-progress-bar/tree/main/progressbar/progressbar)
    - Resource 2 : [Stackoverflow - Websockets, React + Django](https://stackoverflow.com/questions/71506466/websockets-react-django)
        - [GitHub Repo](https://github.com/pplonski/simple-tasks/blob/master/backend/server/server/settings.py)
    - Work with [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/)
    - Tools : [WebSocket King](https://websocketking.com/) 

---

This project was developed as part of a Final Year Project to enhance public transportation systems using real-time AI-powered crowd detection.

