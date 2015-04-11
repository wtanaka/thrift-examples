all:
	for i in *.thrift; do thrift -r --gen js --gen py $$i; done

clean:
	rm -rf gen-py *~

server:
	env PYTHONPATH=.:gen-py python server.py

client:
	env PYTHONPATH=.:gen-py python client.py
