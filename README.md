# LinkedIn Analytics Dashboard

## Overview
This project is an executive-grade LinkedIn Analytics Dashboard built with Python and Plotly Dash. It visualizes LinkedIn engagement data (impressions, followers, demographics, etc.) from Excel exports, providing insights into content performance and audience statistics.

## Project Structure
- `dashboard.py`: The main application entry point.
- `assets/`: Contains static assets like CSS files (`custom.css`).
- `data/` (Assumed): Place your LinkedIn Excel export files here (e.g., `Content_...xlsx`).
- `.gitignore`: Specifies intentionally untracked files to ignore.

## Prerequisites
- **Python 3.x**: Ensure Python is installed on your system.
- **Virtual Environment** (Recommended): It's best practice to run this project in a virtual environment.

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment**:
    - Windows:
        ```powershell
        .venv\Scripts\activate
        ```
    - macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies**:
    *(Note: If a `requirements.txt` exists, run `pip install -r requirements.txt`. Otherwise, install the necessary packages manually as shown below.)*
    ```bash
    pip install dash pandas plotly openpyxl
    ```

## Usage

1.  **Prepare Data**: Ensure your LinkedIn data Excel files (e.g., `Content_...xlsx`) are in the project directory.

2.  **Run the Dashboard**:
    ```bash
    python dashboard.py
    ```

3.  **Access the Dashboard**:
    Open your web browser and go to `http://127.0.0.1:8050/`.

## License
[Add License Information Here]
