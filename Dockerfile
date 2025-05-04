# Import Base Python Image
FROM python:3.12.2

# Define Working Directory
WORKDIR /app

# Copy from Source to Container 
COPY /tiffin /app

# Intall Required Dependencies
RUN pip install -r requirements.txt

# Collect Static Files
RUN python manage.py collectstatic --noinput

# Expose Ports
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tiffin.wsgi:application"]