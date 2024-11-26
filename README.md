Sales Analysis Web Application
This is a web-based application built using Flask, SQLite, Pandas, Matplotlib, and Seaborn. The application allows users to submit sales data and view statistical analysis and visualizations based on the submitted data.

Features
Form Submission: Submit product sales data including product ID, name, category, sales amount, units sold, region, and customer age.
Statistics: View basic statistics like mean, median, standard deviation of sales, units sold, and customer age.
Chart Visualization: Display a histogram of sales data to visualize the distribution of sales amounts.
Prerequisites
Make sure you have the following installed:

Python 3.x (preferably 3.8 or above)
pip (Python package manager)
Installation
Follow these steps to set up and run the application locally:

1. Clone the repository
bash
Copy code
git clone <repository_url>
cd sales_analysis_app
2. Create a Virtual Environment (Optional but recommended)
Create a virtual environment to manage dependencies.

bash
Copy code
python -m venv venv
Activate the virtual environment:

Windows:
bash
Copy code
venv\Scripts\activate
macOS/Linux:
bash
Copy code
source venv/bin/activate
3. Install Dependencies
Install the required Python packages listed in requirements.txt.

bash
Copy code
pip install -r requirements.txt
If you don’t have a requirements.txt file, you can manually install the necessary libraries using:

bash
Copy code
pip install Flask pandas matplotlib seaborn sqlite3
4. Database Setup
The application will automatically create the SQLite database (sales.db) on the first run. You don’t need to manually create the database.

5. Run the Flask Application
Run the Flask development server:

bash
Copy code
python app.py
The application will be accessible at http://127.0.0.1:5000/ in your web browser.

Usage
Enter Data: On the home page, fill in the product information and sales data in the form and click Submit.
View Statistics: After submitting data, the statistics (mean, median, etc.) will be displayed.
View Chart: A chart visualizing the distribution of sales amounts will be displayed below the statistics.
Troubleshooting
404 for Static Files: If you see a 404 error for static files like scripts.js or style.css, ensure that these files are located in the static directory and Flask is correctly configured to serve them.
Chart Not Displaying: If the chart is not showing up, ensure that the /chart route is correctly generating the chart. Test the /chart endpoint directly by navigating to http://127.0.0.1:5000/chart.
Directory Structure
graphql
Copy code
sales_analysis_app/
├── app.py                  # Main application code (Flask)
├── templates/
│   └── index.html          # HTML template for the home page
├── static/
│   ├── style.css           # CSS for the front-end
│   └── scripts.js          # JavaScript for form submission and chart updates
└── data/
    └── sales.db            # SQLite database for storing sales data
