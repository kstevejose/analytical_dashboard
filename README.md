# LinkedIn Analytics Dashboard

## Overview
This project is an executive-grade LinkedIn Analytics Dashboard built with Python and Plotly Dash. It visualizes LinkedIn engagement data (impressions, followers, demographics, etc.) from Excel exports, providing insights into content performance and audience statistics.

## Project Structure
- `main.py`: The main program that executes and displays the dashboard.
- `assets/`: Contains static assets like CSS files (`custom.css`).
- `data/`: Place your LinkedIn Excel export files here (Example: `Content_...xlsx`).
- `.gitignore`: Specifies untracked files to ignore.

## Prerequisites
- **Python 3.x**: Ensure Python is installed on your system.
- **Virtual Environment** (Recommended): It's best practice to run this project in a virtual environment.

## Installation

1.  **Clone the repository** and navigate to the project directory.

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

## Usage

1.  **Prepare Data**: Ensure your LinkedIn data Excel files (For Example, `Content_...xlsx`) are in the project's `data` folder.

2.  **Run the Dashboard**:
    Open your jupyter notebook and select "Click All".

3.  **Access the Dashboard**:
    Open your web browser and go to `http://127.0.0.1:8050/`. 

    **Note**: If you have other programs running on the port, change your port number.


