# Symmetry: Particle Physics Database

## Description
Symmetry is a Django-based web application that serves as a database for particle physics. It allows users to view and manage information about elementary particles, their properties, and interactions.

## Features
- Database of elementary particles with detailed properties
- Admin interface for managing particle data
- RESTful API for accessing particle information
- User-friendly web interface for browsing particles

## Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)
- PostgreSQL

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/symmetry.git
   cd symmetry
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   - Create a database named `symmetry_db`
   - Update the database configuration in `symmetry/settings.py` if necessary

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Load initial particle data:
   ```bash
   python manage.py import_particles
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

## Usage

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Access the application:
   - Web Interface: http://127.0.0.1:8000/particles/
   - Admin Interface: http://127.0.0.1:8000/admin/

## Contributing
Contributions to Symmetry are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Particle data sourced from [insert source here]
- Built with Django and PostgreSQL