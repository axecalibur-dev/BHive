# Mutual Fund Brokerage using Rapid API

## Project Prerequisites

- **Internet Connection**: Required for downloading dependencies and pulling Docker images.
- **Python Installed**: Ensure Python 3.8 or above is installed on your local machine.
- **Docker**: Make sure Docker is installed and running in the background.

---

## How to Set Up

1. **Clone the Repository**
   - Clone the repository from GitHub:
     ```bash
     git clone <repository_url>
     cd <repository_name>
     ```

2. **Set Up Environment Variables**
   - Move the `.env` file to the project root directory. This ensures all required environment variables are passed to the project.

3. **Ensure Docker is Running**
   - Keep Docker open and running in the background.

4. **Create and Activate Virtual Environment**
   - Navigate to the project root and create a virtual environment:
     ```bash
     python3 -m venv myenv
     ```
   - Activate the virtual environment:
     ```bash
     source myenv/bin/activate
     ```

5. **Start the Project**
   - Navigate to project root and run the startup script to initialize the project:
     ```bash
     sh start_project.sh
     ```
   - This script will:
     - Install all necessary dependencies listed in `requirements.txt` locally.
     - Build Docker containers using `docker-compose`.
     - Install dependencies inside Docker via the `Dockerfile`.
     - Start the application using Uvicorn on port `8000` and inject environment variables from `.env`.

---

## Performing Database Migrations

1. **Prepare a Concurrent Terminal**
   - Open a new terminal window and create a separate virtual environment:
     ```bash
     python3 -m venv myenv
     source myenv/bin/activate
     ```
   - This is required since the first terminal is displaying project logs.

2. **Run the Migration Script**
   - Navigate to the project root and execute the migration script:
     ```bash
     sh migrate.sh
     ```
   - The migration script will use Alembic to apply any pending database migrations. Migration files are located at:
     ```
     root > alembic > versions
     ```

---

## Testing the APIs

- Use the provided **Postman Collection** to test the APIs. The collection includes all necessary endpoints and example requests for the application.
