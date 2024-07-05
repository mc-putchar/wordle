FROM python:3-alpine

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080
CMD ["fastapi", "run", "wordle.py", "--port", "8080"]
