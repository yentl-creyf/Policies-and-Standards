FROM python:3.11-slim AS base

# set the working directory
WORKDIR /project

# copy the scripts to the folder
COPY ./main.py .

# production image
FROM base AS production
# Creates a non-root user with an explicit UID and adds permission to access the /project folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /project
USER appuser

CMD ["python", "main.py"]