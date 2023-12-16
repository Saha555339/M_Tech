# M_Tech
Test task for M_Tech.

1. Соберите Docker-образ:

   ```bash
   docker build -t my_streamlit_app .
2. Запустите контейнер:

   ```bash
   docker run --name my_app_v1 -p 8501:8501 my_streamlit_app

*. Чтобы остановить приложение, выполните:

   ```bash
   docker stop my_app_v1
