# 💰 Personal Expense Tracker

A desktop application to track daily expenses with filtering capabilities, built with Python, Tkinter, and SQLite.

## ✨ Features

- ➕ **Add expenses**: Track amount, category, date, and description
- ✏️ **Edit entries**: Modify existing expenses
- ❌ **Delete records**: Remove unwanted entries
- 🔍 **Advanced filtering**:
  - By category (Food, Transport, Bills, etc.)
  - By date range
- 📊 **Data persistence**: SQLite database saves all entries
- 🖥️ **User-friendly interface**: Clean Tkinter GUI

## 🛠️ Technologies Used

- Python 3.8+
- Tkinter (GUI framework)
- SQLite3 (lightweight database)
- ttkbootstrap (optional for modern UI themes)

## 🚀 Installation & Usage

### Basic Installation
```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
python expense_tracker.py
*Note: Requires Python 3.6+ with Tkinter (usually included in standard Python installation)*

🏗️ Development Setup
bash
# Optional: Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install optional dependencies
pip install ttkbootstrap
📦 Creating an Executable
To distribute to non-technical users:

Install PyInstaller:

bash
pip install pyinstal
Build executable:

bash
pyinstaller --onefile --windowed --icon=app.ico expense_tracker.py
Find the executable in dist/ folder

🤝 Contributing
We welcome contributions! Please:

Fork the repository

Create a feature branch (git checkout -b feature/your-feature)

Commit your changes (git commit -m 'Add some feature')

Push to the branch (git push origin feature/your-feature)

Open a Pull Request

📜 License
MIT License - See LICENSE file for details.

Copyright (c) 2025 Nexha