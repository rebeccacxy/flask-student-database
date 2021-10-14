# Student Database App

This is a Flask web application that manages student entries in a SQL database.

Users can upload a CSV into the SQL database, make changes and download the updated database to a CSV.  

If no CSV file is uploaded, the default CSV files `student1.csv` and `mark1.csv` will be used as placeholders in the SQL database.

## Functionality
- Upload CSV file
- Add database entries
- Search for database entries
- Edit database entries
- Delete database entries
- Download updated database to CSV into `outputs/output.csv`

&nbsp;

## Getting Started

### Local development

Set up the database before running for the first time
```bash
python db_creator.py
```

Run the development build locally

```bash
python main.py
```

The website will launch at http://127.0.0.1:5001/. 