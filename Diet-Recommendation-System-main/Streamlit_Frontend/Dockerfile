FROM python:3.10.8

RUN mkdir -p /app/frontend
WORKDIR /app/frontend

# Ensure the auth directory exists and is writable
RUN mkdir -p /app/frontend/auth && \
    chmod 777 /app/frontend/auth

COPY Streamlit_Frontend/ .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["Hello.py"]