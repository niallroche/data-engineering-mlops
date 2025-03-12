FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY api/ api/
COPY model/ model/
COPY static/ static/

# Expose the port and run the Flask app
EXPOSE 5000
CMD ["python", "api/app.py"]