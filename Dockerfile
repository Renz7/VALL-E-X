FROM renz7/vallex-dep

WORKDIR /vallex

COPY . /vallex/

RUN python3 prepare.py

ENTRYPOINT [ "sh", "entrypoint.sh" ]