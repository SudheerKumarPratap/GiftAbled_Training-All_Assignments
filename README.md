
# Expenses Tracker System in FastAPI

A lightweight, robust web application designed to monitor and manage daily expenses efficiently. This project combines a **FastAPI backend REST API** with a clean frontend interface.

## 🚀 Features
* **Full CRUD Functionality:** Seamlessly Create, Read (get details), Update, and Delete expense entries.
* **Category Filtering:** Easily filter and view expense items by specific categories.
* **Expense Analytics:** Automatically calculates and displays the total amount spent across various categories.

## 📁 File Structure Overview
The application consists of the following core components:
* `main.py` - Core FastAPI backend application containing the REST endpoints and business logic.
* `index.html` - The user interface structure for interacting with the tracker.
* `styles.css` - Visual layout and styling of the user interface.
* `app.js` - Client-side script handling asynchronous API requests (`fetch`) to communicate with the backend.

## 🛠️ Prerequisites
Make sure Python has been installed on your local computer.

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd Expenses_Tracker
   ```

2. **Install dependencies:**
   *(Ensure you create a requirements.txt file or run directly if using default packages)*
   ```bash
   pip install fastapi uvicorn
   ```

3. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Launch the Application:**
   * Once the server is running locally at `http://127.0.0.1:8000`, simply open your `index.html` file in your preferred web browser (like Google Chrome) to begin tracking your expenses.

## 🔌 API Documentation
When running locally, you can view the fully interactive API documentation provided natively by FastAPI:
* Interactive Swagger Docs: `http://127.0.0`
* Alternative Redoc: `http://127.0.0`

