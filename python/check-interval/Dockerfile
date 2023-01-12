FROM python:3.7

ADD  check-interval.py   .
ADD  requirements.txt  .
ADD config.yaml    .

WORKDIR  .

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

CMD ["python3", "check-interval.py"]