FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]

# docker build -t my_streamlit_app .
# docker run --name my_app_v1 -p 8501:8501 my_streamlit_app
# docker stop ma_app_v1