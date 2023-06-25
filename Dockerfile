FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY script.py .

ENV GITHUB_TOKEN='<GITHUB API TOKEN>'
ENV GITHUB_USERNAME='<github repo username>'
ENV GITHUB_REPO='<github repo name>'


ENV SENDER_EMAIL='<provide sender gmail adress>'
ENV RECEIVER_EMAIL='<receiver gmail address>'
ENV SMTP_SERVER="smtp.gmail.com" <replace gmail server here>
ENV SMTP_PORT=587 <Replace gmail port>
ENV SMTP_USERNAME='<provide gmail sender address >'
ENV SMTP_PASSWORD='<generated app gmail api token>'

CMD ["python", "script.py"]
