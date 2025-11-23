FROM python:3

WORKDIR /work

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# `mandoc` needed for `aws help`
# `less` needed for `aws ec2 describe-instances ..`
RUN apt update && apt install less mandoc tmux tree cowsay yamllint -y

CMD ["tail", "-f", "/dev/null"]