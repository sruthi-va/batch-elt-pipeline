FROM apache/spark:4.0.0-python3

USER root

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/artifacts /app/data /app/output \
    && chown -R spark:spark /app

USER spark

CMD ["/opt/spark/bin/spark-submit", "validation/validate_transformation.py"]