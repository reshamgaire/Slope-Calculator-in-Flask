# Slope Calculator

This is a web application that calculates the slope of a straight line given two points (in 2D or 3D) and the slope of a curve at a given point using its equation. It provides mathematical results and visual plots for 2D calculations.

## Features

This application provides two main functionalities:

### 1. Slope of a Line

*   **2D Points:** Given two points (x₁, y₁) and (x₂, y₂), the calculator will determine:
    *   The slope of the line.
    *   The angle the line makes with the positive x-axis (in degrees).
    *   The equation of the line.
    *   A visual plot of the line and the two points.
*   **3D Points:** Given two points (x₁, y₁, z₁) and (x₂, y₂, z₂), the calculator will determine the slope of the line with respect to the x-axis, y-axis, and z-axis. This is derived from the direction cosines of the line.

### 2. Slope of a Curve at a Point

*   Given the equation of a curve (e.g., `y = x^2 - 3x + 2`) and a point (either an x-coordinate or a full (x, y) coordinate pair that lies on the curve):
    *   The calculator will determine the slope of the tangent line to the curve at that specific point using differentiation.
    *   A visual plot of the curve, the specified point, and the tangent line at that point.
    *   If only the x-coordinate is provided, the application will calculate the corresponding y-coordinate on the curve.

## Technologies Used

*   **Flask:** A micro web framework for Python used to build the web application.
*   **SymPy:** A Python library for symbolic mathematics, used for parsing equations and performing differentiation.
*   **Matplotlib:** A plotting library for Python, used to generate graphs of lines and curves.
*   **NumPy:** A library for numerical operations in Python, used in conjunction with Matplotlib for generating plot data.
*   **HTML/CSS/JavaScript:** For the front-end structure, styling, and basic interactivity.

## Setup and Run

To run this application locally, follow these steps:

1.  **Prerequisites:**
    *   Ensure you have Python 3.x installed on your system.
    *   Ensure you have pip (Python package installer) installed.

2.  **Clone the Repository (if applicable):**
    ```bash
    git clone https://github.com/reshamgaire/Slope-Calculator-in-Flask.git
    cd Slope-Calculator-in-Flask
    ```
    *(If you've downloaded the files directly, navigate to the project directory.)*

3.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

4.  **Install Dependencies:**
    Navigate to the project's root directory (where `requirements.txt` is located) and run:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Application:**
    ```bash
    python app.py
    ```
    The application will typically be available at `http://127.0.0.1:5000/` in your web browser.

## File Structure

```
.
├── app.py              # Main Flask application file, contains routing and logic.
├── utils.py            # Utility functions, primarily for parsing mathematical input.
├── requirements.txt    # Lists the Python dependencies for the project.
├── static/             # Contains static assets like CSS and images.
│   ├── style.css       # Stylesheet for the application.
│   └── slope-calculator.ico # Favicon for the application.
├── templates/          # HTML templates for rendering web pages.
│   ├── index.html      # Main page template with input forms and general info.
│   └── slopans.html    # Template for displaying calculation results and graphs.
```

## How to Use

1.  Navigate to the homepage of the application.
2.  You will see options to calculate the slope either by "Two points (straight line)" or by "Equation of curve".
3.  **For a straight line (Two Points):**
    *   Click the "Two points (straight line)" button if it's not already selected.
    *   Enter the coordinates of the first point in the format `x1,y1` (for 2D) or `x1,y1,z1` (for 3D).
    *   Enter the coordinates of the second point in the same format.
    *   Click "SUBMIT". The results (slope, angle, equation, and graph for 2D) will be displayed.
4.  **For a curve (Equation of Curve):**
    *   Click the "Equation of curve" button.
    *   Enter the equation of the curve (e.g., `y = x^2`, `y = sin(x)`). Ensure `y` is on one side.
    *   Enter the point at which you want to find the slope. You can either provide:
        *   Just the x-coordinate (e.g., `2`). The application will calculate the y-coordinate.
        *   Both x and y coordinates (e.g., `2,4`).
    *   Click "SUBMIT". The slope at that point and a graph of the curve with the tangent line will be displayed.
