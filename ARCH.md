<<<<<<< HEAD
# course_management
=======
=======
>>>>>>> 8428495 (cse-mgt-v1)
# Course Management Application using Django

## 1. Project Overview
The Course Management System is designed to digitize the basic academic record management workflow of an educational institution.

<br>The system provides a centralized platform where students can register, select courses, access their demographic information, and view academic results. Authorized institutional staff can manage student records, maintain course information, and record student scores.

<br>The application uses Django's Model-View-Template (MVT) architecture and a relational database to maintain data consistency and enforce relationships between students, courses, enrollments, and results.

### Primary users
<br>Students: Register accounts, select courses, access personal records, and view results.
<br>Administrative staff: Manage students, courses, enrollments, and academic records.
<br>System administrators: Configure users, permissions, application settings, and system operations.

## 2. Objectives
<br>The primary objectives are to:
<br>Provide a structured student registration workflow.
<br>Maintain accurate student demographic records.
<br>Maintain a centralized catalogue of institutional courses.
<br>Associate students with their selected courses.
<br>Record and retrieve academic scores by course.


## 3. Architechtural Diagram

flowchart TB
    subgraph Presentation["Presentation Layer"]
        Browser["Web Browser"]
        Templates["Django Templates"]
        Bootstrap["HTML / CSS / Bootstrap"]
    end

    subgraph Application["Application Layer - Django"]
        URLs["URL Routing"]
        Views["Views / Controllers"]
        Forms["Forms and Validation"]
        Auth["Authentication and Permissions"]
        Models["Django Models / ORM"]
        Admin["Django Admin"]
    end

    subgraph Data["Data Layer"]
        DB[("Relational Database")]
    end

    Browser --> Templates
    Templates --> Bootstrap
    Browser --> URLs
    URLs --> Views
    Views --> Forms
    Views --> Auth
    Views --> Models
    Admin --> Models
    Models --> DB
    DB --> Models
    Models --> Views
    Views --> Templates

### Database Architecture
The database uses a relational model with foreign keys and uniqueness constraints.

#### Entity relationship diagram

erDiagram
    USER ||--o| STUDENT : owns
    STUDENT ||--o{ ENROLLMENT : registers
    COURSE ||--o{ ENROLLMENT : contains
    ENROLLMENT ||--o| RESULT : receives

    USER {
        bigint id PK
        string username UK
        string password
        string email
        string first_name
        string last_name
        boolean is_active
        boolean is_staff
    }

    STUDENT {
        bigint id PK
        bigint user_id FK
        string student_number UK
        date date_of_birth
        string phone
        text address
        datetime created_at
    }

    COURSE {
        bigint id PK
        string code UK
        string title
        text description
        int credits
        boolean is_active
    }

    ENROLLMENT {
        bigint id PK
        bigint student_id FK
        bigint course_id FK
        datetime enrolled_at
    }

    RESULT {
        bigint id PK
        bigint enrollment_id FK
        decimal score
        datetime updated_at
    }


### Project Structure

course_management/
├── manage.py
├── requirements.txt
├── README.md
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── records/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   └── templates/
│       └── records/
│           ├── base.html
│           ├── register.html
│           ├── login.html
│           ├── dashboard.html
│           ├── students.html
│           ├── courses.html
│           ├── results.html
│           └── record_result.html
└── db.sqlite3





<<<<<<< HEAD
>>>>>>> 512550e (cse-mgt-v1)
=======
>>>>>>> 8428495 (cse-mgt-v1)
