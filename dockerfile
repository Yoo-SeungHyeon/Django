FROM python

#RUN pip install --upagrade pip

RUN pip install django

WORKDIR /usr/src/app

COPY . .

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]