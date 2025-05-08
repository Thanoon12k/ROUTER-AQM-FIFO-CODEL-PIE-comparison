import simpy
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np

class HostType(Enum):
    FTP = "FTP"
    WEB = "WEB"
    VIDEO = "VIDEO"

@dataclass
class Packet:
    id: int
    source: HostType
    size: int
    creation_time: float
    arrival_time: Optional[float] = None
    departure_time: Optional[float] = None
    
    @property
    def delay(self) -> float:
        if self.arrival_time is None or self.departure_time is None:
            return 0.0
        return self.departure_time - self.arrival_time

class Host:
    def __init__(self, env: simpy.Environment, host_type: HostType, 
                 packet_size_range: tuple, router: 'Router'):
        self.env = env
        self.host_type = host_type
        self.packet_size_range = packet_size_range
        self.router = router
        self.packets_sent = 0
        self.packets_received = 0
        self.total_delay = 0.0
        
    def generate_packet(self) -> Packet:
        size = random.randint(*self.packet_size_range)
        packet = Packet(
            id=self.packets_sent,
            source=self.host_type,
            size=size,
            creation_time=self.env.now
        )
        self.packets_sent += 1
        return packet
    
    def send_packet(self):
        while self.packets_sent < 100:  # Generate exactly 100 packets
            packet = self.generate_packet()
            yield self.env.timeout(random.expovariate(1.0))  # Exponential inter-arrival time
            self.router.receive_packet(packet)
            
    def receive_ack(self, packet: Packet):
        self.packets_received += 1
        self.total_delay += packet.delay

class Router:
    def __init__(self, env: simpy.Environment, queue_size: int, 
                 aqm_type: str, servers: List['Server']):
        self.env = env
        self.queue_size = queue_size
        self.aqm_type = aqm_type
        self.servers = servers
        self.queue = []
        self.packets_dropped = 0
        self.packets_processed = 0
        self.total_queue_delay = 0.0
        
        # CODEL specific parameters
        self.target_delay = 0.005  # 5ms target delay
        self.interval = 0.1  # 100ms interval
        self.last_drop_time = 0.0
        self.min_delay = float('inf')
        
    def receive_packet(self, packet: Packet):
        packet.arrival_time = self.env.now
        
        if self.aqm_type == "FIFO":
            if len(self.queue) >= self.queue_size:
                self.packets_dropped += 1
                return
            self.queue.append(packet)
            self.env.process(self.process_packet(packet))
            
        elif self.aqm_type == "CODEL":
            current_delay = self.env.now - packet.arrival_time
            self.min_delay = min(self.min_delay, current_delay)
            
            if self.env.now - self.last_drop_time >= self.interval:
                if self.min_delay > self.target_delay:
                    self.packets_dropped += 1
                    self.last_drop_time = self.env.now
                    self.min_delay = float('inf')
                    return
                self.last_drop_time = self.env.now
                self.min_delay = float('inf')
            
            if len(self.queue) >= self.queue_size:
                self.packets_dropped += 1
                return
                
            self.queue.append(packet)
            self.env.process(self.process_packet(packet))
    
    def process_packet(self, packet: Packet):
        # Simulate processing delay
        yield self.env.timeout(packet.size / 1000)  # Assuming 1Mbps link speed
        
        # Remove from queue
        self.queue.remove(packet)
        self.packets_processed += 1
        
        # Calculate queue delay
        queue_delay = self.env.now - packet.arrival_time
        self.total_queue_delay += queue_delay
        
        # Forward to appropriate server
        server = self.servers[packet.source.value % len(self.servers)]
        server.receive_packet(packet)

class Server:
    def __init__(self, env: simpy.Environment, hosts: List[Host]):
        self.env = env
        self.hosts = hosts
        self.packets_processed = 0
        
    def receive_packet(self, packet: Packet):
        # Simulate processing delay
        yield self.env.timeout(packet.size / 2000)  # Assuming 2Mbps processing speed
        
        packet.departure_time = self.env.now
        self.packets_processed += 1
        
        # Send acknowledgment back to the host
        host = self.hosts[packet.source.value % len(self.hosts)]
        host.receive_ack(packet) 