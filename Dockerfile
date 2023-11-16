FROM renz7/vallex-dep

WORKDIR /vallex

COPY . /vallex/

RUN pip install -r requirements.txt --ignore-installed -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT [ "sh", "entrypoint.sh" ]