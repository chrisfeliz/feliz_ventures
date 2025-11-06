# Feliz Ventures LLC Website

A FastAPI-based website for Feliz Ventures LLC, a real estate development company based in North Carolina.

## Features

- Modern, responsive design
- Navigation menu with mobile support
- Current projects showcase
- Multiple pages: About, Sell Your Land, Contact, Privacy Policy

## Installation

### Option 1: Using Dev Container (Recommended)

If you're using VS Code with the Remote - Containers extension:

1. Open the project in VS Code
2. When prompted, click "Reopen in Container" or use the command palette: `Dev Containers: Reopen in Container`
3. The container will automatically install dependencies and set up the environment
4. The application will be available at `http://localhost:8000`

### Option 2: Local Installation

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## Project Structure

```
developer_site/
├── .devcontainer/       # Dev container configuration
│   └── devcontainer.json
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── templates/          # HTML templates
│   ├── index.html
│   ├── about.html
│   ├── sell_land.html
│   ├── contact.html
│   └── privacy.html
└── static/              # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Routes

- `/` - Homepage
- `/about` - About Us page
- `/sell-your-land` - Sell Your Land page
- `/contact` - Contact Us page
- `/privacy-policy` - Privacy Policy page

