# Django URL Shortener

A robust web application built with Python and the Django framework that allows users to shorten long URLs, manage their links, and track click analytics.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure registration, login, and logout system.
- **Shortening Algorithm**: Implements a unique **Base62 encoding** algorithm ($0-9, a-z, A-Z$) to convert database IDs into short, unique URL keys.
- **Redirection**: Seamlessly redirects short URLs to original long URLs.

### URL Management & Analytics
- **Personal Dashboard**: Users can view a list of all their created short links.
- **CRUD Operations**: Options to edit destination URLs or delete existing short links.
- **Usage Statistics**: Real-time tracking of click counts for every link.
- **Information Display**: Shows creation dates and click counts for better link management.

### User Interface
- Clean, intuitive, and responsive design built with Django templates.

---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/url-shortener.git](https://github.com/yourusername/url-shortener.git)
cd url-shortener

### 2. Set up the Environment
Make sure you have Python installed. It is recommended to use a virtual environment.
```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate

# Install Django
pip install django

### 3. Initialize the Database
Run migrations to create the necessary tables for users and short URLs.
```bash
python manage.py makemigrations
python manage.py migrate

### 4. Run the Application
```bash
python manage.py runserver

## Visit http://127.0.0.1:8000/ in your browser.

#### Project Structure
core/: Project configuration, settings, and root URL routing.

shortener/: The main application logic containing:

models.py: Database schema for URLs, users, and analytics.

views.py: Logic for shortening, redirecting, and URL management.

utils.py: The Base62 encoding utility function.

templates/: HTML views for the Dashboard, Login, and Registration pages.

#### 🧠 Technical Details: Base62 Logic
The application converts the unique primary key (ID) of each database record into a Base62 string. This ensures that every short link is unique and the length remains as short as possible without the need for random string collision checks.

Conversion Examples:

ID 125 → c3

ID 10000 → 2Bi

This method allows for billions of unique URLs using only 6 or 7 characters.


***

### 🚀 Ready to upload?
Now that your README is perfect, you can push your code to GitHub. If you haven't initialized your repository yet, run these commands in your project folder:



1. `git init`
2. `git add .`
3. `git commit -m "Initial commit: Full URL Shortener functionality"`
4. `git branch -M main`
5. `git remote add origin https://github.com/yourusername/your-repo-name.git`
6. `git push -u origin main`

**Would you like me to double-check any of your Python files (like `models.py` or `views.py`) one last time to make sure they match the README perfectly?**