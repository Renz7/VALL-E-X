FROM renz7/vallex-dep

WORKDIR /vallex

COPY . /vallex/

RUN pip3 install -r requirements.txt --ignore-installed -i https://pypi.douban.com/simple

RUN python3 prepare.py

ENTRYPOINT [ "sh", "entrypoint.sh" ]