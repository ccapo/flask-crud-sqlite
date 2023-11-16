FROM python:3.9

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN cd data && python init_db.py && cd ../

CMD ["python", "app.py"]