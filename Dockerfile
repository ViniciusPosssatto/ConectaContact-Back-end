FROM python:3.8.13-alpine

# Expose port 8080
EXPOSE 8080
ENV PORT 8080
ENV HOST 0.0.0.0

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python3", "app.py" ]
