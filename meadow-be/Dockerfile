FROM m.daocloud.io/docker.io/library/python:3.9.21

WORKDIR /sheep-app

COPY . .
EXPOSE 5000
RUN pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
CMD ["python","app.py"]

