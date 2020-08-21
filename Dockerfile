ARG VERSION=latest
FROM python:$VERSION
RUN pip install pandas xlrd
WORKDIR /usr/src
RUN git clone https://github.com/eddiebarry/WHO-FAQ-Keyword-Engine.git
WORKDIR /usr/src/WHO-FAQ-Keyword-Engine