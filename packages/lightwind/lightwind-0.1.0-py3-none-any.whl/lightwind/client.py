import json

import grpc

from lightwind import inference_pb2
from lightwind.inference_pb2_grpc import PrivateTransferProtocolStub


class LightWindClient:
    CMD = "inference"

    def __init__(self, url: str):
        self.url = url

    def create(self, payload) -> str:
        channel = grpc.insecure_channel(self.url)
        stub = PrivateTransferProtocolStub(channel)
        request_payload = bytes(
            json.dumps({"query": json.dumps(payload, ensure_ascii=False)}, ensure_ascii=False), "utf-8"
        )
        response = stub.invoke(inference_pb2.Inbound(cmd=self.CMD, payload=request_payload))
        response_payload = response.payload.decode("utf-8")
        return response_payload
