# 🎉 EventManager

A full-stack event management web application built using Django’s MVT pattern. This platform enables users to discover, RSVP to, and manage events seamlessly. With clearly defined roles — **Admin**, **Organizer**, and **User** — each user experiences a tailored interface and functionality.

🔗 **Live Site:** [EventManager](https://event-manager-ie3m.onrender.com/)

---

## ✨ Features

- 🔐 **User Authentication** using JWT with login, registration & email verification
- 📅 **RSVP to Events** – view event details and confirm attendance
- 🔎 **Search & Filter** – by event name, category, or date
- 🧑‍⚖️ **Role-Based Access Control**
  - **Admin** – full access to manage users, events, roles, groups, and permissions
  - **Organizer** – manage tasks assigned by admin such as events and categories
  - **User** – RSVP to events and manage personal profile
- 📊 **Dashboards** for each role
  - Admin dashboard
  - Organizer panel
  - User profile & event history

---

## 🧰 Tech Stack

| Frontend                     | Backend              | Authentication          | Deployment                   |
| ---------------------------- | -------------------- | ----------------------- | ---------------------------- |
| HTML, Tailwind CSS, Flowbite | Python, Django (MVT) | JWT, Email Verification | [Render](https://render.com) |

---

## 🚀 Installation & Setup (Local)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/rjmahfuztech/event-management.git
cd event-management
```

### 2️⃣ Create Virtual Environment & Activate

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Configuration

Create a .env file in the root directory and add your environment variables:

```bash
SECRET_KEY=your django project secret key

# for email configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=your email host password
```

### 5️⃣ Apply Migrations & Create Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6️⃣ Run the Development Server

```bash
python manage.py runserver
```

## 📄 License

This project is licensed under the MIT License.

## 🙋‍♂️ Author

**Mahfuz Islam**

For any questions or issues, feel free to contact me at rjmahfuz.islam@gmail.com or visit:

🌐 [Portfolio Website](https://mahfuzislam.vercel.app)  
🔗 [LinkedIn](https://linkedin.com/in/mahfuz-islam)  
🐙 [GitHub](https://github.com/rjmahfuztech)
