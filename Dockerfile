FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV EVENTS_DB=/data/hamcal.db
EXPOSE 5001
# Copy the script into the container (if not already copied by your build steps)
COPY start.sh /app/start.sh

# Make the script executable
RUN chmod +x /app/start.sh

# Run the script when the container starts
CMD ["/app/start.sh"]