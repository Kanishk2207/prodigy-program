# Activity Scheduling API

This project provides a FastAPI-based application for managing daily activity schedules. The application is containerized using Docker and uses SQLite3 as the database. The project is designed to automatically migrate database tables on startup and serves APIs for querying and managing activities.

Please Note that the structure of the project is POC level. If given more time and efforts, it can be more robust

## Features

- **Activity Management**: Define and manage activities with their categories, frequencies, and durations.
- **Daily Scheduling**: Assign activities to specific days.
- **Automatic Database Migration**: The application automatically creates necessary tables on startup.
- **Containerized Deployment**: Simplified setup and deployment using Docker.
- **RESTful APIs**: Exposes endpoints for retrieving and managing schedules.

## Prerequisites

- Docker installed on your system.
- Python 3 installed in the container.

## Project Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Kanishk2207/prodigy-program.git
   cd prodigy-program
   ```

2. Place the required CSV files in the `resources` directory if not present:
   - `weekly_plan.csv`
   - `daily_schedule.csv`

3. Update the `.env` file with the filenames if not there:
   ```env
   DB_URL=sqlite+aiosqlite:///./database/database
   MIGRATION_SCRIPT_PATH=/app/database/migration/migration.sql
   WEEKLY_PLAN_CSV_FILE_NAME=weekly_plan.csv
   DAILY_SCHEDULE_CSV_FILE_NAME=daily_schedule.csv
   DEFAULT_RESOURCE_PATH=resources
   ```

4. Build the Docker container:
   ```bash
   ./entrypoint.sh build Dockerfile
   ```
   
5. Start the Docker container:
   ```bash
   ./entrypoint.sh start
   ```

6. Access the container and start the application:
   ```bash
   python3 main.py
   ```

7. The application will be hosted at `http://localhost:9002`.

## Database Schema

The following tables are automatically created:

### `activities`
| Column   | Type   | Description            |
|----------|--------|------------------------|
| `id`     | TEXT  | Primary Key (UUID)     |
| `category` | TEXT  | Activity Category     |
| `activity` | TEXT  | Activity Name         |
| `frequency` | TEXT | Frequency of Activity |
| `time` | TEXT | Duration of Activity |

### `schedule`
| Column   | Type   | Description        |
|----------|--------|--------------------|
| `id`    | TEXT | ID of schedule |
| `day`    | INTEGER | Day of the schedule |
| `activity_id` | TEXT | Foreign Key (UUID) from `activities` |
| `completed` | INTEGER | Mark if activity is completed |

## API Endpoints

### 1. `GET /schedule/all?day=Intiger`
Retrieve all activities for the day.
Eg: day = 15, day=16
- **Response:**
  ```json
  [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "category": "Athleticism",
      "activity": "Advanced Mobility exercises",
      "frequency": "Maximize",
      "time": "Max."
    },
    ...
  ]
  ```



### 2. `POST /schedule/complete`
Mark an activity completed
- **Request body:** 
```json
   {
    "schedule_id": "71b41fd8-7186-4f15-b838-ba65bfcffca0"(enter schedule it from get request)
}
```
- **Response:**
  ```json
    "data": {
        "message": "Activity already completed"
    }

  ```

## Notes

- Ensure that the `resources` directory contains the required CSV files before starting the application.
- The database tables are automatically migrated when the app starts.
- Default hosting port: `9002`.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

