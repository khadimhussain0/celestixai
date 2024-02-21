FROM python:3.12.2-bookworm

# Install supervisord
RUN apt-get update && \
    apt-get install -y supervisor && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir -p /var/log/supervisor /var/log/celestixai

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN pip install "fastapi[all]"
RUN pip install pydantic==1.10.13


COPY . .

COPY celestixai.conf /etc/supervisor/conf.d/celestixai.conf


EXPOSE 8000

# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
