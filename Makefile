all: python
	for i in *.thrift; do thrift -r --gen js --gen py $$i; done

python: gen-py/typecheck

gen-py/%: %.thrift
	thrift -r --gen py $^

clean:
	rm -rf gen-py *~

tcheck: gen-py/typecheck
	env PYTHONPATH=.:gen-py python tcheck.py

server:
	env PYTHONPATH=.:gen-py python server.py

client:
	env PYTHONPATH=.:gen-py python client.py

docker:
	cp typecheck.thrift tcheck.py thrift-0.9.2
	docker build -t wtanaka/thrift thrift-0.9.2
