FROM mongo
RUN apt update -y
RUN apt install nano curl python3 python3-pip -y
RUN python3 -m pip install pymongo
RUN curl https://raw.githubusercontent.com/JosebaSaenz/mongodb/main/main.py > /home/main.py
