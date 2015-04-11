all: gen-py

gen-py:
	for i in *.thrift; do thrift --gen py $$i; done

clean:
	rm -rf gen-py *~

server:
	env PYTHONPATH=.:gen-py python server.py
