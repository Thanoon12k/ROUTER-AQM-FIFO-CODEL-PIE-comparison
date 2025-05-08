
class UniqueIDGenerator:
    _counter = 0  # Class variable to track ID count
    _packet_counter = 0  # Class variable to track packet ID count
    @classmethod
    def get_next_id(cls,is_packet=False):
        """ Generate a unique ID for nodes or packets """
        if is_packet:
            cls._packet_counter += 1
            return cls._packet_counter
        else:
            cls._counter += 1
            return cls._counter



class Packet:
    def __init__(self, packet_id, source_ip, destination_ip, payload, protocol, size, timestamp):
        self.packet_id = packet_id
        self.source_ip = source_ip
        self.node_type = "Packet"  # Type of node
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
        

class NetworkNode:
    def __init__(self, node_id, ip_address, mac_address, location, status, manufacturer, model, firmware_version, uptime, power_usage, max_bandwidth, security_level):
        self.node_id = node_id
        self.node_type = "NetworkNode"  # Type of node
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.location = location
        self.status = status
        self.manufacturer = manufacturer
        self.model = model
        self.firmware_version = firmware_version
        self.uptime = uptime
        self.power_usage = power_usage
        self.max_bandwidth = max_bandwidth
        self.security_level = security_level
        self.packet_log = []  # Stores handled packets
        self.icon = "🆔"  # Icon for the node
        
    def receive_packet(self, packet):
        self.packet_log.append(packet)
        return f"{self.ip_address} received packet from {packet.source_ip}"

    def display_info(self):
        return (f"Node ID: {self.node_id}, IP: {self.ip_address}, MAC: {self.mac_address}, Location: {self.location}, "
                f"Status: {self.status}, Manufacturer: {self.manufacturer}, Model: {self.model}, "
                f"Firmware Version: {self.firmware_version}, Uptime: {self.uptime}, Power Usage: {self.power_usage}W, "
                f"Max Bandwidth: {self.max_bandwidth} Mbps, Security Level: {self.security_level}")


class Router(NetworkNode):
    def __init__(self, node_id, ip_address, mac_address, location, status, manufacturer, model, firmware_version, uptime, power_usage, max_bandwidth, security_level,
                 routing_table, interfaces, firewall_rules, aqm_qos_protocol, packet_forwarding_protocol, queue_type, buffer_size):
        super().__init__(node_id, ip_address, mac_address, location, status, manufacturer, model, firmware_version, uptime, power_usage, max_bandwidth, security_level)
        self.routing_table = routing_table
        self.node_type = "Router"  # Type of node
        self.interfaces = interfaces
        self.firewall_rules = firewall_rules
        self.aqm_qos_protocol = aqm_qos_protocol
        self.packet_forwarding_protocol = packet_forwarding_protocol
        self.queue_type = queue_type
        self.buffer_size = buffer_size
        self.icon = "🔀"


    def forward_packet(self, packet):
        if packet.destination_ip in self.routing_table:
            return f"Router forwarding packet {packet.packet_id} via {self.packet_forwarding_protocol}"
        return f"Router dropped packet {packet.packet_id} (destination unknown)"

    def display_info(self):
        return super().display_info() + f", Routing Table: {self.routing_table}, Interfaces: {self.interfaces}, Firewall Rules: {self.firewall_rules}, AQM QoS Protocol: {self.aqm_qos_protocol}, Packet Forwarding Protocol: {self.packet_forwarding_protocol}, Queue Type: {self.queue_type}, Buffer Size: {self.buffer_size}"



class Host(NetworkNode):
    def __init__(self, node_id, ip_address, mac_address, location, status, manufacturer, model, firmware_version, uptime, power_usage, max_bandwidth, security_level, hostname, os, installed_software, cpu_usage, memory_capacity):
        super().__init__(node_id, ip_address, mac_address, location, status, manufacturer, model, firmware_version, uptime, power_usage, max_bandwidth, security_level)
        self.hostname = hostname
        self.node_type = "Host"  # Type of node
        self.os = os
        self.installed_software = installed_software
        self.cpu_usage = cpu_usage
        self.memory_capacity = memory_capacity
        self.icon = "💻" # Icon for the host

    def send_packet(self, packet):
        return f"Host {self.hostname} sent packet {packet.packet_id} to {packet.destination_ip}"

    def display_info(self):
        return super().display_info() + f", Hostname: {self.hostname}, OS: {self.os}, Installed Software: {self.installed_software}, CPU Usage: {self.cpu_usage}%, Memory: {self.memory_capacity} GB"


class Switch(NetworkNode):
    def __init__(self, node_id, ip_address, mac_address, location, status, manufacturer, model, firmware_version, uptime, power_usage, max_bandwidth, security_level, switch_ports, vlan_config, mac_table, stp_enabled):
        super().__init__(node_id, ip_address, mac_address, location, status, manufacturer, model, firmware_version, uptime, power_usage, max_bandwidth, security_level)
        self.switch_ports = switch_ports
        self.node_type = "Switch"  # Type of node
        self.vlan_config = vlan_config
        self.mac_table = mac_table
        self.stp_enabled = stp_enabled
        self.icon = "🔛"  # Icon for the switch

    def switch_packet(self, packet):
        if packet.destination_ip in self.mac_table.values():
            return f"Switch forwarding packet {packet.packet_id} via MAC table lookup."
        return f"Switch broadcasting packet {packet.packet_id}."

    def display_info(self):
        return super().display_info() + f", Ports: {self.switch_ports}, VLAN Config: {self.vlan_config}, MAC Table: {self.mac_table}, STP Enabled: {self.stp_enabled}"


class Hub(NetworkNode):
    def __init__(self, node_id, ip_address, mac_address, location, status, manufacturer, model, firmware_version, uptime, power_usage, max_bandwidth, security_level, connected_devices, data_rate, collision_rate, transmission_medium):
        super().__init__(node_id, ip_address, mac_address, location, status, manufacturer, model, firmware_version, uptime, power_usage, max_bandwidth, security_level)
        self.connected_devices = connected_devices
        self.data_rate = data_rate
        self.node_type = "Hub"  # Type of node
        self.collision_rate = collision_rate
        self.transmission_medium = transmission_medium
        self.icon = "🔼"  # Icon for the hub

    def broadcast_packet(self, packet):
        return f"Hub broadcasting packet {packet.packet_id} to all connected devices."

    def display_info(self):
        return super().display_info() + f", Connected Devices: {self.connected_devices}, Data Rate: {self.data_rate}, Collision Rate: {self.collision_rate}, Transmission Medium: {self.transmission_medium}"


class Server(NetworkNode):
    def __init__(self, node_id, ip_address, mac_address, location, status, manufacturer, model, firmware_version, uptime, power_usage, max_bandwidth, security_level, server_type, storage_capacity, cpu_utilization, active_sessions, database_engine, virtualized):
        super().__init__(node_id, ip_address, mac_address, location, status, manufacturer, model, firmware_version, uptime, power_usage, max_bandwidth, security_level)
        self.server_type = server_type
        self.node_type = "Server"  # Type of node
        self.storage_capacity = storage_capacity
        self.cpu_utilization = cpu_utilization
        self.active_sessions = active_sessions
        self.database_engine = database_engine
        self.virtualized = virtualized
        self.icon = "🌐"  # Icon for the server

    def process_packet(self, packet):
        return f"Server processing packet {packet.packet_id} using {self.database_engine}."

    def display_info(self):
        return super().display_info() + f", Server Type: {self.server_type}, Storage Capacity: {self.storage_capacity} GB, CPU Utilization: {self.cpu_utilization}%, Active Sessions: {self.active_sessions}, Database Engine: {self.database_engine}, Virtualized: {self.virtualized}"



