FROM m.daocloud.io/docker.io/library/python:3.9.21

WORKDIR /meadow-app

COPY . .
EXPOSE 5000
RUN apt-get update && apt-get install -y default-mysql-client >/dev/null 2>&1
RUN pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
CMD ["python","app.py"]

