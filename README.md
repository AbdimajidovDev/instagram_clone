# # 📸 Instagram Clone API

A full-featured Instagram-like REST API built with Django and Django REST Framework. This project allows users to register, upload posts with images, like and comment on posts, follow other users, and manage their profiles.

---

## 🚀 Features

- 🔐 User registration, login, logout
- 👤 User profiles with avatar and bio
- 📷 Create, retrieve, update and delete image posts
- ❤️ Like/unlike posts
- 💬 Comment on posts
- 👥 Follow/unfollow other users
- 🧵 Post feed with pagination
- 🖼 Media uploads
- 🔒 JWT-based authentication
- 🔁 Shared utility module (for reusable logic)

---

## 🛠 Tech Stack

- **Python 3.11+**
- **Django 4+**
- **Django REST Framework**
- **Pillow** for image handling
- **SQLite3** (for development)
- **JWT (Simple JWT)** for authentication
---

## 📂 Project Structure

instagram_clone/
- ├── users/ # Registration, login, profiles, following
- ├── post/ # Post CRUD, likes, comments
- ├── shared/ # Common utils and base models
- ├── media/ # Uploaded images
- ├── templates/ # HTML templates (optional for email/reset)
- ├── instagram_clone/ # Main project settings
- ├── requirements.txt
- └── manage.py

---
```bash

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/AbdimajidovDev/instagram_clone.git
cd instagram_clone

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Run the development server
python manage.py runserver

```
---
## 🔐 Authentication
This project uses JWT (JSON Web Tokens) for secure API authentication.

Add the token to your headers when making authenticated requests:
```angular2html
Authorization: Bearer <your_access_token>
```
---
## 🧑🏻‍💻 Author
👤 Name: To‘lqinbek Abdimajidov

📧 Email: tulqinjonabdimajidovhp@gmail.com

🌐 GitHub: AbdimajidovDev