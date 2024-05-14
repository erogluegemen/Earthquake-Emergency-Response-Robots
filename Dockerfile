FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /emergency_robot_project

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    portaudio19-dev \
    libgl1-mesa-glx 

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./emergency_robot_project .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]