FROM python:3.10

WORKDIR /app 

COPY . /app 

RUN pip install --no-cache-dir -r requirements.txt 

EXPOSE 8500 

ENV PORT = 8500 

CMD ["streamlit", "run", "--server.port", "8501", "app.py"] 