# HRMS Lite - Human Resource Management System

A comprehensive web-based HRMS Lite application built with React frontend and Django backend, designed for managing employee records and tracking daily attendance.

## 🚀 Features

### Employee Management
- ✅ Add new employees with unique Employee ID, name, email, and department
- ✅ View all employees with search and filter capabilities
- ✅ Edit employee information
- ✅ Delete employees
- ✅ Input validation and duplicate prevention

### Attendance Management
- ✅ Mark daily attendance (Present/Absent) for employees
- ✅ View attendance records with filtering by employee, date range, and status
- ✅ Edit attendance records
- ✅ Delete attendance records
- ✅ Prevent future date attendance marking

### Dashboard & Analytics
- ✅ Real-time dashboard with key statistics
- ✅ Today's attendance summary
- ✅ Department-wise employee distribution
- ✅ Recent attendance records
- ✅ Quick action buttons

### Professional UI/UX
- ✅ Clean, modern, and responsive design
- ✅ Professional color scheme and typography
- ✅ Loading states and empty state handling
- ✅ Toast notifications for user feedback
- ✅ Form validation with error messages
- ✅ Mobile-friendly responsive layout

## 🛠 Tech Stack

### Frontend
- **React 18** - Modern JavaScript library for building user interfaces
- **React Router DOM** - Client-side routing
- **Axios** - HTTP client for API requests
- **CSS3** - Custom styling with modern CSS features

### Backend
- **Django 4.2** - High-level Python web framework
- **Django REST Framework** - Powerful toolkit for building Web APIs
- **PostgreSQL** - Robust, production-ready relational database
- **psycopg2** - PostgreSQL adapter for Python
- **Django CORS Headers** - Cross-Origin Resource Sharing support

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- **Python 3.8+** - [Download Python](https://python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **npm** or **yarn** - Package manager (comes with Node.js)
- **PostgreSQL 12+** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git** - Version control system

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hrms-lite
```

### 2. PostgreSQL Database Setup

First, set up the PostgreSQL database:

```bash
# Install PostgreSQL (if not already installed)
# On macOS with Homebrew:
brew install postgresql
brew services start postgresql

# On Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# On Windows: Download from https://www.postgresql.org/download/windows/

# Create database and user (choose one of the following methods):

# Method 1: Using the setup script (if postgres user has no password)
sudo -u postgres psql -f backend/setup_postgresql.sql

# Method 2: If postgres user has a password, use this instead:
psql -U postgres -f backend/setup_postgresql.sql

# Method 3: Manual setup (recommended if above methods don't work)
# First, connect to PostgreSQL as superuser:
sudo -u postgres psql
# OR if that doesn't work, try:
psql -U postgres

# Then run these commands in the PostgreSQL prompt:
CREATE DATABASE hrms_lite_db;
CREATE USER hrms_user WITH PASSWORD 'hrms_password';
GRANT ALL PRIVILEGES ON DATABASE hrms_lite_db TO hrms_user;
\c hrms_lite_db;
GRANT ALL ON SCHEMA public TO hrms_user;
\q

# Method 4: Using createdb and createuser commands (alternative)
sudo -u postgres createdb hrms_lite_db
sudo -u postgres createuser --interactive hrms_user
# When prompted, make hrms_user a superuser or grant necessary permissions
```

### 3. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies (including PostgreSQL adapter)
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Start Django development server
python manage.py runserver
```

The Django backend will be available at `http://localhost:8000`

### 3. Frontend Setup (React)

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start React development server
npm start
```

The React frontend will be available at `http://localhost:3000`

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/ (if superuser created)

## 🔧 Development Setup

### Using the Convenience Script

For easier development, you can use the package.json scripts:

```bash
# Install all dependencies (backend + frontend)
npm run setup

# Run both backend and frontend concurrently
npm run dev
```

### Manual Setup

If you prefer to run services manually:

**Terminal 1 (Backend):**
```bash
cd backend
python manage.py runserver
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```

## 📁 Project Structure

```
hrms-lite/
├── backend/                    # Django backend
│   ├── hrms_project/          # Django project settings
│   │   ├── settings.py        # Configuration
│   │   ├── urls.py           # URL routing
│   │   └── wsgi.py           # WSGI configuration
│   ├── hrms_app/             # Main Django app
│   │   ├── models.py         # Database models
│   │   ├── serializers.py    # API serializers
│   │   ├── views.py          # API views
│   │   ├── urls.py           # App URL routing
│   │   ├── admin.py          # Admin configuration
│   │   └── tests.py          # Unit tests
│   ├── manage.py             # Django management script
│   └── requirements.txt      # Python dependencies
├── frontend/                  # React frontend
│   ├── public/               # Static files
│   ├── src/                  # Source code
│   │   ├── components/       # React components
│   │   │   ├── Dashboard.js
│   │   │   ├── EmployeeList.js
│   │   │   ├── EmployeeForm.js
│   │   │   ├── AttendanceList.js
│   │   │   ├── AttendanceForm.js
│   │   │   ├── Navbar.js
│   │   │   └── Toast.js
│   │   ├── context/          # React context
│   │   │   └── ToastContext.js
│   │   ├── services/         # API services
│   │   │   └── api.js
│   │   ├── App.js            # Main App component
│   │   ├── App.css           # Global styles
│   │   └── index.js          # Entry point
│   ├── package.json          # Node.js dependencies
│   └── package-lock.json     # Dependency lock file
├── package.json              # Root package.json for scripts
└── README.md                 # This file
```

## 🔌 API Endpoints

### Employee Endpoints
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create new employee
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/` - Update employee
- `DELETE /api/employees/{id}/` - Delete employee
- `GET /api/employees/simple/` - Get simple employee list for dropdowns

### Attendance Endpoints
- `GET /api/attendance/` - List attendance records
- `POST /api/attendance/` - Create attendance record
- `GET /api/attendance/{id}/` - Get attendance details
- `PUT /api/attendance/{id}/` - Update attendance record
- `DELETE /api/attendance/{id}/` - Delete attendance record

### Dashboard Endpoints
- `GET /api/dashboard/` - Get dashboard summary

### Query Parameters

**Employee List:**
- `search` - Search by name, ID, or email
- `department` - Filter by department

**Attendance List:**
- `employee` - Filter by employee ID
- `status` - Filter by status (Present/Absent)
- `date_from` - Filter from date (YYYY-MM-DD)
- `date_to` - Filter to date (YYYY-MM-DD)

## 🧪 Testing

### Backend Tests

```bash
cd backend
python manage.py test
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🚀 Production Deployment

### Quick Production Setup

For a production-ready PostgreSQL setup, use the automated setup script:

```bash
cd backend
python setup_production.py
```

This script will:
- Create a production `.env` file with secure settings
- Generate a secure Django secret key
- Configure PostgreSQL database connection
- Test database connectivity
- Run migrations
- Collect static files
- Create a superuser account
- Run security checks

### Manual Production Setup

#### 1. Environment Configuration

Create a production environment file:

```bash
cd backend
cp .env.example .env
```

Edit `.env` with your production values:
- Set `DEBUG=False`
- Configure `DATABASE_*` settings for PostgreSQL
- Set a secure `SECRET_KEY`
- Configure `ALLOWED_HOSTS` with your domain
- Set up SSL/HTTPS settings
- Configure email settings for error notifications

#### 2. PostgreSQL Production Setup

For detailed PostgreSQL production configuration, see [PRODUCTION_SETUP.md](PRODUCTION_SETUP.md) which includes:
- Production PostgreSQL installation and configuration
- Security settings and SSL configuration
- Performance optimization
- Backup strategies
- Monitoring and logging setup
- Nginx reverse proxy configuration
- SSL certificate setup

#### 3. Backend (Django)

```bash
cd backend

# Install production dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Run security checks
python manage.py check --deploy

# Use Gunicorn for production
pip install gunicorn
gunicorn --config gunicorn.conf.py hrms_project.wsgi:application
```

#### 4. Frontend (React)

```bash
cd frontend

# Build for production
npm run build

# Serve with a web server (Nginx recommended)
```

### Production Files

- **PRODUCTION_SETUP.md** - Comprehensive production deployment guide
- **backend/setup_production.py** - Automated production setup script
- **backend/.env.example** - Environment configuration template
- **backend/.env.development** - Development environment defaults
- **backend/setup_postgresql.sql** - PostgreSQL database setup script

### Environment-Based Configuration

The application now supports environment-based configuration:
- **Development**: Uses SQLite by default, relaxed security settings
- **Production**: Uses PostgreSQL, enhanced security, caching, logging

Switch between environments by configuring the `.env` file or using environment variables.

## 🔒 Security Considerations

- Input validation on both frontend and backend
- CSRF protection enabled
- SQL injection prevention through Django ORM
- XSS protection through proper data sanitization
- CORS configuration for cross-origin requests

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use:**
   - Backend: Change port in `python manage.py runserver 8001`
   - Frontend: Set `PORT=3001` environment variable

2. **Database errors:**
   - Run migrations: `python manage.py migrate`
   - Reset database: Delete `db.sqlite3` and run migrations again

3. **CORS errors:**
   - Ensure `django-cors-headers` is installed and configured
   - Check `CORS_ALLOWED_ORIGINS` in settings.py

4. **Module not found errors:**
   - Backend: Ensure virtual environment is activated and dependencies installed
   - Frontend: Run `npm install` to install dependencies

5. **PostgreSQL connection errors:**
   - Ensure PostgreSQL service is running: `brew services start postgresql` (macOS) or `sudo systemctl start postgresql` (Linux)
   - Check if database exists: `psql -U postgres -l`
   - Verify user permissions: `psql -U postgres -c "\du"`
   - If you get "password authentication failed", try resetting postgres password:
     ```bash
     sudo -u postgres psql
     ALTER USER postgres PASSWORD 'newpassword';
     ```

6. **PostgreSQL setup password issues:**
   - If `sudo -u postgres psql` asks for password, try these alternatives:
     - Use `psql -U postgres` and enter the postgres user password
     - Reset postgres password: `sudo passwd postgres`
     - Use peer authentication: edit `/etc/postgresql/*/main/pg_hba.conf` and change `md5` to `peer` for local connections
     - Restart PostgreSQL after config changes: `sudo systemctl restart postgresql`

7. **Alternative: Use SQLite for development:**
   - If PostgreSQL setup is problematic, copy `settings_sqlite.py` to `settings.py`:
     ```bash
     cp backend/hrms_project/settings_sqlite.py backend/hrms_project/settings.py
     ```
   - Then run migrations normally: `python manage.py migrate`

## 📝 Assumptions and Limitations

### Assumptions
- Single admin user (no authentication system implemented)
- PostgreSQL database for robust data storage and scalability
- Employees have unique email addresses and employee IDs
- Attendance can only be marked for current or past dates

### Limitations
- No user authentication/authorization system
- No role-based access control
- No advanced reporting features
- No bulk operations for attendance
- No employee photo upload
- No leave management system
- No payroll integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Support

For support or questions, please create an issue in the repository or contact the development team.

---

**Built with ❤️ using React and Django**
