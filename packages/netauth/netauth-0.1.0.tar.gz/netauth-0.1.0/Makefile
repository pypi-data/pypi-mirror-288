%PHONY: generate clean

generate: protocol/netauth.proto protocol/v2/rpc.proto
	$(VENV)/bin/python3 -m grpc_tools.protoc -I ./protocol \
		--python_out=netauth/_pb --pyi_out=netauth/_pb --grpc_python_out=netauth/_pb \
		./protocol/netauth.proto ./protocol/v2/rpc.proto
	# correct imports
	sed -i netauth/_pb/v2/rpc_pb2.py -e 's/import netauth_pb2/from .. &/'
	sed -i netauth/_pb/v2/rpc_pb2_grpc.py -e 's/from v2/from ./'

%.proto:
	@echo "Missing protocol definitions. Are submodules checked out?"

clean:
	rm netauth/_pb/netauth_pb2*
	rm netauth/_pb/v2/rpc_pb2*
