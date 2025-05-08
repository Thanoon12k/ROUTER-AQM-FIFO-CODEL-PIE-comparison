from gui import Office
import time

from v1.classes import *

# Create an Office Space
office = Office(500, 300)  # Width x Height in pixels

# Create Nodes
router = Router(UniqueIDGenerator.get_next_id(), "192.168.1.1", "00:11:22:33:44:55", "Center", "Active", "Cisco", "RV340", "v2.0", "24hr", 70, 10000, "High",
                routing_table={"192.168.1.2": "eth0", "192.168.1.3": "eth1"},
                interfaces=["eth0", "eth1"], firewall_rules=["Allow all"],
                aqm_qos_protocol="WFQ", packet_forwarding_protocol="OSPF", queue_type="FIFO", buffer_size=100)

host1 = Host(UniqueIDGenerator.get_next_id(), "192.168.1.2", "00:1A:2B:3C:4D:5E", "Desk 1", "Active", "Dell", "XPS", "v1.0", "12hr", 50, 1000, "Medium",
             hostname="PC-1", os="Windows", installed_software=["Chrome", "Zoom"], cpu_usage=30, memory_capacity=16)

host2 = Host(UniqueIDGenerator.get_next_id(), "192.168.1.3", "00:1A:2B:3C:4D:5F", "Desk 2", "Active", "HP", "EliteBook", "v1.0", "15hr", 45, 1000, "Medium",
             hostname="PC-2", os="Linux", installed_software=["Firefox", "VS Code"], cpu_usage=40, memory_capacity=32)

# Add Nodes to Office
office.add_node(router)
office.add_node(host1)
office.add_node(host2)

# Connect Hosts to Router
office.connect_nodes(host1, router)
office.connect_nodes(host2, router)

import time

def generate_packets(num_packets, total_time):
    """ Generate a list of packets with evenly spaced start times """
    packets = []
    time_intervals = []

    interval = total_time / num_packets  # Calculate time spacing between packets

    for i in range(num_packets):
        packet = Packet(
            UniqueIDGenerator.get_next_id(is_packet=True),  # Unique ID
            "192.168.1.2",  # Source IP
            "192.168.1.3",  # Destination IP
            f"Hello Packet {i+1}",  # Payload
            "TCP",  # Protocol
            512,  # Size in bytes
            time.time()  # Timestamp
        )
        packets.append(packet)
        time_intervals.append(i * interval)  # Spaced start times

    return packets, time_intervals

if __name__ == "__main__":
    packets, time_interval = generate_packets(num_packets=10, total_time=40)
    office.display_network_gui(packets, time_interval)
