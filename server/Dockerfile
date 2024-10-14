# Use a base image
FROM python:3.12.0-slim-bookworm

# Set environment variables
ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1
ENV APP=/app

# Change the working directory to /app
WORKDIR $APP

# Install the requirements
COPY requirements.txt $APP
RUN pip3 install -r requirements.txt

# Copy the rest of the application files to /app
COPY . $APP

# Expose the application port
EXPOSE 8000

# Ensure entrypoint.sh is executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint and default command
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
