FROM python:3-bullseye

RUN apt update && apt install unzip
WORKDIR /www
COPY . .

RUN pip install --upgrade pip wheel setuptools && pip install --no-cache-dir --upgrade -r requirements.txt
RUN reflex init
RUN reflex export --frontend-only --no-zip
EXPOSE 3000
# Always apply migrations before starting the backend.
CMD [ -d alembic ] && reflex db migrate; reflex run --env prod
