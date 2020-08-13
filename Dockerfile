FROM python:3.7

RUN pip install fastapi uvicorn pymongo uuid passlib pydantic[email] python-multipart

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--reload"]
