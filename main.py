import pandas as pd
from network_nodes import Host, Link, Router, Server
# Create network nodes
host1 = Host(
    id=1,
    ip_address="192.168.1.10",
    name="web-client",
    os="Windows 10",
    installed_application="Web-app",
    start_time=0,
    packets_source="random",
    num_packets=0,
    packets_off_time=0
)

router1 = Router(
    id=1,
    ip_address="192.168.1.1",
    name="MainRouter",
    queue=[],
    aqm_algoritm="RED",
    queue_size=1000
)

server1 = Server(
    id=1,
    name="Web-Server",
    ip_address="192.168.2.10",
    supported_service="HTTP",
    os="Ubuntu Server"
)



class Network_Simulation:
    def __init__(self, id, sim_time, nodes,links):
        self.id = id
        self.sim_time = sim_time
        self.nodes = nodes  # List of network nodes (e.g., hosts, routers, servers)
        self.packets = []  # List to store packets in the simulation
        self.links =links # List to store links between nodes
        def get_simulation_packets(self):
            for node in self.nodes:
                if node.node_type == "Host":
                    packets = node.generate_packets(self.sim_time)
                    self.packets.extend(packets)
            
            return self.packets
        
        def run_simulation(self):
            for node in self.nodes:
                if node.node_type == "Host":
                    node.start_packet_generation(self.sim_time)


if __name__=="__main__":
    pakets_stream=pd.read_csv("dataset.csv")
    print(pakets_stream.head())