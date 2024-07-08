FROM python:3.9-slim-buster

WORKDIR /

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080

# Define environment variables
ENV FLASK_ENV=production
ENV FLASK_APP=server.py
ENV DATABASE_URL=https://speety-2175-default-rtdb.firebaseio.com
ENV WALKABILITY_API_KEY=5e775c237088586a07f1a8ba73969b1a
ENV PRICE_TREND_GPT_API_KEY=sk-proj-oOIKmJQ5tAJTL0baRdvyT3BlbkFJkLCVSancI3TNukiWlvKy
ENV SCAIL_CONTACT_BOT_API_KEY=sk-proj-DBaaojqg622ljaXkaxorT3BlbkFJIYLDWazWAYlQr6C1DA6g
ENV PRICE_TREND_GPT_MODEL=ft:gpt-3.5-turbo-0125:personal::9hKhCk83
ENV SCAIL_CONTACT_BOT_MODEL=ft:gpt-3.5-turbo-0125:personal::9hVRYHlV

CMD python3 server.py