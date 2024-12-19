# Configuration
database_inf = {
    "username": "", # Default "root"
    "password": "", 
    "host": "", # Default "localhost"
    "port": 0, # Default 3306
    "database": "todo_api"
}


# True = will recreate tables every launch (good for testing)
# False = disable this function
refresh_tables_on_startup = True


# JWT key, you can insert yours below
jwt_secret_key = "RVCgIRbz7A8"


database_url = f"mysql+pymysql://{database_inf['username']}:{database_inf['password']}@{database_inf['host']}/{database_inf['database']}"


description_for_api = """
# Task Management API

This API is designed to manage tasks, allowing users to perform CRUD operations on tasks. 

## Features:
- **Authentication**: Secure access using token-based authentication.
- **Account System**: Users can register and have their own tasks.
- **Task Operations**:
  - Create new tasks.
  - Edit tasks by ID.
  - Delete tasks by ID.
  - View tasks assigned to a specific user.
- **User-Specific Data**: Each account has its own tasks, ensuring data separation.
- **Structured Responses**: Consistent JSON responses for easy integration.

Endpoints are intuitive and focus on managing task data such as `title`, `description`, and `status`. Ideal for building task management systems or integrating task tracking into existing platforms.
"""