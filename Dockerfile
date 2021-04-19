FROM --platform=linux/amd64 python:3.6.6

WORKDIR /app

COPY req.txt .

RUN pip install --disable-pip-version-check -r req.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]