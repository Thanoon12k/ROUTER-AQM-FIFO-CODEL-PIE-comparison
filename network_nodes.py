


import pandas as pd


class Packet:
    def __init__(self, packet_id, source_ip, destination_ip, payload, protocol, size, timestamp):
        self.packet_id = packet_id
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.payload = payload  # Data being transmitted
        self.protocol = protocol  # TCP, UDP, ICMP, etc.
        self.size = size  # Packet size in bytes
        self.timestamp = timestamp  # When the packet was generated
        self.hubcount = 0  # Number of hops the packet has made
        self.ttl= 64  # Time to live, decremented by each router
        self.icon= "💌"  # Icon for the packet

    def display_info(self):
        return (f"Packet ID: {self.packet_id}, Source: {self.source_ip}, Destination: {self.destination_ip}, "
                f"Protocol: {self.protocol}, Size: {self.size} bytes, Timestamp: {self.timestamp}")
        


class Router():
    def __init__(self,id,ip_address,name, queue, aqm_algoritm, queue_size):
        self.id= id
        self.ip_address = ip_address
        self.name = name
        self.queue = queue
        self.node_type = "Router"  # Type of node
        self.queue_size = queue_size
        self.aqm_algoritm = aqm_algoritm
        self.icon = "🔀"


    def forward_packet(self, packet):
        if packet.destination_ip in self.routing_table:
            return f"Router forwarding packet {packet.packet_id} "
        return f"Router dropped packet {packet.packet_id} (destination unknown)"

    def display_info(self):
        return super().display_info() + f", Routing Table: {self.routing_table}, Interfaces: {self.interfaces}, Firewall Rules: {self.firewall_rules}, AQM QoS Protocol: {self.aqm_algoritm}, Packet Forwarding Protocol: {self.packet_forwarding_protocol}, Queue Type: {self.queue_type}, Buffer Size: {self.buffer_size}"



class Host():
    def __init__(self,id,ip_address,name, os, installed_application,start_time,packets_source,num_packets,packets_off_time):
        self.id= id
        self.name = name
        self.ip_address = ip_address
        self.node_type = "Host"  # Type of node
        self.start_time = start_time  # Time when the host started
        self.packets_source = packets_source #file of csv file path with packets
        self.num_packets = num_packets
        self.packets_off_time = packets_off_time

        self.os = os
        self.installed_application = installed_application
        self.icon = "💻" # Icon for the host
    def get_node_packets(self):
        packets=pd.read_csv(self.packets_source)
        return []
        
    def send_packet(self, packet):
        return f"Host {self.hostname} sent packet {packet.packet_id} to {packet.destination_ip}"

    def display_info(self):
        return super().display_info() + f", Hostname: {self.hostname}, OS: {self.os}, Installed Software: {self.installed_application}, CPU Usage: {self.cpu_usage}%, Memory: {self.memory_capacity} GB"

class Server():
    def __init__(self, id,name,ip_address,supported_service ,os ):
        self.id= id
        self.name = name
        self.ip_address = ip_address
        self.supported_service = supported_service
        self.node_type = "Server"  # Type of node
        self.os = os
        
        self.icon = "🌐"  # Icon for the server

    def process_packet(self, packet):
        return f"Server processing packet {packet.packet_id} using {self.database_engine}."

    def display_info(self):
        return super().display_info() + f", Server Type: {self.supported_service}, Storage Capacity: {self.storage_capacity} GB, CPU Utilization: {self.cpu_utilization}%, Active Sessions: {self.active_sessions}, Database Engine: {self.database_engine}, Virtualized: {self.virtualized}"



class Link():
    def __init__(self, id, source_node, destination_node, bandwidth, latency):
        self.id = id
        self.source_node = source_node  # Source node (Host/Router/Server)
        self.destination_node = destination_node  # Destination node (Host/Router/Server)
        self.latency = latency  # Latency in ms
        self.bandwidth = bandwidth
        self.node_type = "Link"

        self.icon = "🔗"  # Icon for the link

    def display_info(self):
        return f"Link ID: {self.id}, Source: {self.source_node.name}, Destination: {self.destination_node.name}, Bandwidth: {self.bandwidth} Mbps, Latency: {self.latency} ms"