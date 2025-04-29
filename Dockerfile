FROM public.ecr.aws/sam/build-python3.12:1.125.0-20240926224229

WORKDIR /src

COPY . /src

ENV PYTHONPATH="/src"

RUN pip install --no-cache-dir -r prod-requirements.txt

EXPOSE 8000


CMD ["/bin/sh", "-c", "python src/create_db.py && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]