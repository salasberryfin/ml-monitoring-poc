FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/.
COPY ./app /app/.

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
