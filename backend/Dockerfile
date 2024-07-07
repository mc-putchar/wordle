FROM python:3-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["fastapi", "run", "wordle.py", "--port", "8080"]
