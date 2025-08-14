# AI CSV Dashboard Troubleshooting Guide

This guide will help you troubleshoot common issues with the AI CSV Dashboard application.

## 1. Backend Connection Issues

### Symptom: "Could not connect to the backend" error

**Possible causes and solutions:**

1. **Backend is not running**
   - Make sure both terminal windows (backend and frontend) are open
   - Check if the backend window shows any error messages
   - Restart the application using `start_windows.bat`

2. **Port 8000 is already in use**
   - Close other applications that might be using port 8000
   - Or modify the port number in `start_windows.bat` to use a different port (e.g., 8080)

3. **Environment variables not set correctly**
   - Check if your `.env` file contains `GOOGLE_API_KEY`
   - Make sure the API key is valid and has access to the Gemini model

## 2. Internal Server Errors (500 errors)

### Symptom: "500 Server Error: Internal Server Error" 

**Possible causes and solutions:**

1. **API Key issues**
   - Verify your Google API key is correct and has access to the Gemini model
   - Check if you've reached your API usage limits or quotas

2. **Missing packages**
   - Run `pip install -r requirements.txt` to ensure all dependencies are installed

3. **Invalid model name**
   - Check your `.env` file to make sure `GEMINI_MODEL` is set to a valid model name
   - Current valid values: "gemini-2.0-flash", "gemini-pro", etc.

4. **Data too complex or large**
   - Try with a smaller or simpler CSV file
   - Ask more specific questions about the data

## 3. CSV Parsing Issues

### Symptom: Error messages about CSV parsing

**Possible causes and solutions:**

1. **Invalid CSV format**
   - Make sure your CSV file is properly formatted
   - Check for special characters, incorrect delimiters, or encoding issues
   - Try opening and re-saving your CSV file in Excel or another spreadsheet application

2. **Empty file**
   - Ensure your CSV file actually contains data
   - Check that the CSV has headers and at least some rows of data

## 4. Getting Better Answers

If you're not getting the analysis you expect:

1. **Be specific in your questions**
   - Instead of "analyze this data," try "What's the average salary by department?"

2. **Check your data quality**
   - Make sure column names are descriptive
   - Ensure data types are appropriate (numbers for numerical data, etc.)

3. **Start simple**
   - Begin with basic questions before asking complex ones
   - Try questions like "Show me a summary of this data" first

## 5. Running the Application Properly

1. **Always use the start script**
   - Run `start_windows.bat` to properly launch both backend and frontend
   - Keep both terminal windows open

2. **Wait for complete initialization**
   - The script waits 6 seconds, but some systems might need more time
   - Check that the backend window shows "[Startup] Environment loaded" message

3. **Correct access URL**
   - Access the application at http://localhost:8501 in your browser

## Contact Support

If you continue experiencing issues:

1. Check the terminal output for detailed error messages
2. Make sure you have the latest version of the application
3. Contact support with:
   - Screenshots of the error
   - The CSV file you're trying to analyze (if possible)
   - The question you asked
   - Any error messages from the terminal windows
