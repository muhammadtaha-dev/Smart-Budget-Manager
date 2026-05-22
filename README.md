# Smart Budget Manager 💰

A monthly expense tracking system with Flask backend and responsive UI.

## Features
- ✅ Save user profile (name, age, monthly budget)
- ✅ Add/delete expenses with category, item, amount
- ✅ Real-time dashboard with progress bar
- ✅ Budget health status (Under control / Near limit / Exceeded)
- ✅ Responsive design for mobile, tablet, desktop
- ✅ Data persistence with JSON file storage

## Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Icons**: Lucide Icons

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository
2. Install dependencies: `pip install flask flask-cors`
3. Run the backend: `python app.py`
4. Open `index.html` with Live Server

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/profile | Save user profile |
| GET | /api/profile | Get user profile |
| POST | /api/expenses | Add expense |
| GET | /api/expenses | Get all expenses |
| DELETE | /api/expenses/{index} | Delete expense |
| DELETE | /api/expenses/clear | Clear all expenses |

## License
MIT
