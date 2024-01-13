# PyDE

# A Python Development Environment

PyDE is a web-based integrated development environment (IDE) tailored for Python programmers. It provides a comprehensive platform for writing, editing, and executing Python code entirely within a web browser. The aim is to offer a seamless coding experience with essential features like code editing, file management, syntax highlighting, and real-time code execution in an isolated environment for each user.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Setting Up .env](#setting-up-env)
- [Usage](#usage)
- [Screenshots](#screenshots)

## Features

- Real-time code execution in an isolated environment
- Access to a shell container.
- Code editing.
- File management
- Hinting and auto-completion.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login
- python-dotenv
- Other dependencies (check `requirements.txt`)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/aqib-abdullahi.PyDE.git
   
2. Navigate to the project directory:

   ```bash
   cd PyDE
   
3. Create a virtual environment 
   ```
   python3 -m venv venv
   source venv/bin/activate
   
4. Install the required packages
   ```
   pip install -r requirements.txt
   
5. Setting up .env
   
   - Create a .env file in the project root 
   - Add your sensitive configuration data to the '.env' file.
   - The configuration data should be inbetween the quotation marks.
   ```
    MYSQL DB CONFIGURATION
    DB_HOST=""
    DB_PORT=""
    DB_USER=""
    DB_NAME=""
    DB_PASS=""

    CONTAINER CONFIGURATION
    IP_ADDRESS=""
    CONTAINER_ID=""
    CONTAINER_PORT="2375"

    MONGODB CONFIGURATION
    MONGODB_HOST=""
    MONGODB_PORT=""
    MONGODB_NAME=""
    DOCUMENT NAME IN DB SHOULD BE "FILES"