# 📌 ToDo API  

## 📖 Description  
ToDo API is a RESTful API for personal task management. It includes an authentication system, session management, and user accounts. The project is built using **FastAPI** and aims to provide a simple yet powerful tool for managing tasks.  

The code is modular, clean, and well-structured, making it easy to understand and maintain.  

---

## 🔧 Features  
- Authentication and session management.  
- User accounts with personal tasks.  
- Task operations:
  - Create tasks.  
  - Edit tasks.  
  - Delete tasks.  
  - View tasks.  

---

## 🛠 Technologies  
- **Language**: Python 3.13.1  
- **Framework**: FastAPI  
- **Database**: MySQL  
- **ORM**: SQLAlchemy + PyMySQL as driver  
- **Authentication**: AuthX  

---

## 👀 Screenshots
<details>
  <summary>Open</summary>
  
  - ### Overview:
  
  ![Screenshot](https://github.com/PixisProd/todo-api/blob/main/screenshots/ToDo_api_overview.png?raw=true)
  
  - ### Request documentation example:

  ![Screenshot](https://github.com/PixisProd/todo-api/blob/main/screenshots/GET_method_example.png?raw=true)
  
</details>
  
---

# ⚙ How to setup and run

## 📦 Preparation:
1. **First, select the location where you want to install the project:**
```bash
cd <your-repository-folder>
```
2. **Next, clone the repository:**
```bash
git clone https://github.com/PixisProd/todo-api.git
```
3. **Install poetry:**
```bash
pip install poetry
```
4. **Next you need to install the dependencies:**
```bash
poetry install
```
5. **Download and install mysql**:  
- Visit the [official MySQL download page](https://dev.mysql.com/downloads/).
- Ensure MySQL is running and note the credentials for your database setup.

---

## 🚀 Launch:
1. Open the `config.py` file and update the `database_inf` with your MySQL connection credentials.  
*I also clarified which elements can have default values ​​and the default values ​​themselves*
2. **Open the project folder:**  
```bash
cd <repository-folder>
```
3. **Activate the poetry virtual environment:**
```bash
poetry shell
```
4. **Run the project and start testing:**
```bash
python main.py
```

---

# 🌠 Conclusion:
Thank you for your attention. If you like the structure and implementation of the project, feel free to give it a star.

_✨ Crafted to build knowledge._
