import grpc
import iot_service_pb2
import iot_service_pb2_grpc
import threading

def test_request(thread_id):
    channel = grpc.insecure_channel('grpc_server:50051')
    stub = iot_service_pb2_grpc.IoTServiceStub(channel)

    request = iot_service_pb2.ConnectionRequest(
        user_id=f"1234_{thread_id}",
        trigger_id="5678",
        connection_id="91011",
        connection_url="broker.emqx.io",
        port=1883,
        qos=2,
        keep_alive=30,
        subscribe_topic="paho/test/topic",
    )

    response = stub.StartConnection(request)
    print(f"Thread {thread_id}: Response = {response.status}")

# Run multiple concurrent requests
threads = []
for i in range(5):  # Adjust for more load
    t = threading.Thread(target=test_request, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
