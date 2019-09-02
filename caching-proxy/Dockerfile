FROM python:3.7-slim

WORKDIR /app
COPY . .
RUN pip install flask requests redis

EXPOSE 5006
CMD ["python", "proxy.py"]
