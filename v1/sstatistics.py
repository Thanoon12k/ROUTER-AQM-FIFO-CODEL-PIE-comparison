from classes import *
class NetworkStatistics:
    def __init__(self):
        self.node_statistics = {}  # Stores statistics per node

    def collect_node_data(self, node):
        stats = {
            "Node ID": node.node_id,
            "IP Address": node.ip_address,
            "MAC Address": node.mac_address,
            "Location": node.location,
            "Status": node.status,
            "Manufacturer": node.manufacturer,
            "Model": node.model,
            "Firmware Version": node.firmware_version,
            "Uptime": node.uptime,
            "Power Usage": node.power_usage,
            "Max Bandwidth": node.max_bandwidth,
            "Security Level": node.security_level,
            "Packet Log Count": len(node.packet_log)
        }

        if isinstance(node, Host):
            stats.update({
                "Hostname": node.hostname,
                "OS": node.os,
                "CPU Usage": node.cpu_usage,
                "Memory Capacity": node.memory_capacity
            })
        
        if isinstance(node, Router):
            stats.update({
                "Routing Table": node.routing_table,
                "Interfaces": node.interfaces,
                "Firewall Rules": node.firewall_rules,
                "AQM QoS Protocol": node.aqm_qos_protocol,
                "Packet Forwarding Protocol": node.packet_forwarding_protocol,
                "Queue Type": node.queue_type,
                "Buffer Size": node.buffer_size
            })

        if isinstance(node, Switch):
            stats.update({
                "Switch Ports": node.switch_ports,
                "VLAN Config": node.vlan_config,
                "MAC Table": node.mac_table,
                "STP Enabled": node.stp_enabled
            })
        
        if isinstance(node, Hub):
            stats.update({
                "Connected Devices": node.connected_devices,
                "Data Rate": node.data_rate,
                "Collision Rate": node.collision_rate,
                "Transmission Medium": node.transmission_medium
            })

        if isinstance(node, Server):
            stats.update({
                "Server Type": node.server_type,
                "Storage Capacity": node.storage_capacity,
                "CPU Utilization": node.cpu_utilization,
                "Active Sessions": node.active_sessions,
                "Database Engine": node.database_engine,
                "Virtualized": node.virtualized
            })

        self.node_statistics[node.node_id] = stats

    def display_statistics(self):
        for node_id, stats in self.node_statistics.items():
            print(f"\nStatistics for Node {node_id}:")
            for key, value in stats.items():
                print(f"{key}: {value}")
