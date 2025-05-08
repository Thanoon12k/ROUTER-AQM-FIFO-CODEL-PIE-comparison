import random
import time
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
import matplotlib.pyplot as plt
import json
import numpy as np

class HostType(Enum):
    FTP = 0
    WEB = 1
    VIDEO = 2

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
    def __init__(self, host_type: HostType, packet_size_range: tuple):
        self.host_type = host_type
        self.packet_size_range = packet_size_range
        self.packets_sent = 0
        self.packets_received = 0
        self.total_delay = 0.0
        self.packets = []
        
    def generate_packet(self, current_time: float) -> Packet:
        size = random.randint(*self.packet_size_range)
        packet = Packet(
            id=self.packets_sent,
            source=self.host_type,
            size=size,
            creation_time=current_time
        )
        self.packets_sent += 1
        return packet

class Router:
    def __init__(self, queue_size: int, aqm_type: str):
        self.queue_size = queue_size
        self.aqm_type = aqm_type
        self.queue = []
        self.packets_dropped = 0
        self.packets_processed = 0
        self.total_queue_delay = 0.0
        
        # CODEL specific parameters
        self.target_delay = 0.005  # 5ms target delay
        self.interval = 0.1  # 100ms interval
        self.last_drop_time = 0.0
        self.min_delay = float('inf')
        
        # PIE specific parameters
        self.target_queue_delay = 0.02  # 20ms target queue delay
        self.alpha = 0.125  # Proportional gain
        self.beta = 1.25    # Integral gain
        self.drop_probability = 0.0
        self.accu_prob = 0.0
        self.last_update_time = 0.0
        self.update_interval = 0.01  # 10ms update interval
        
    def receive_packet(self, packet: Packet, current_time: float) -> bool:
        packet.arrival_time = current_time
        
        if self.aqm_type == "FIFO":
            if len(self.queue) >= self.queue_size:
                self.packets_dropped += 1
                return False
            self.queue.append(packet)
            return True
            
        elif self.aqm_type == "CODEL":
            current_delay = current_time - packet.arrival_time
            self.min_delay = min(self.min_delay, current_delay)
            
            if current_time - self.last_drop_time >= self.interval:
                if self.min_delay > self.target_delay:
                    self.packets_dropped += 1
                    self.last_drop_time = current_time
                    self.min_delay = float('inf')
                    return False
                self.last_drop_time = current_time
                self.min_delay = float('inf')
            
            if len(self.queue) >= self.queue_size:
                self.packets_dropped += 1
                return False
                
            self.queue.append(packet)
            return True
            
        elif self.aqm_type == "PIE":
            # Update PIE parameters
            if current_time - self.last_update_time >= self.update_interval:
                current_delay = len(self.queue) * 0.001  # Assuming 1ms per packet processing
                error = current_delay - self.target_queue_delay
                
                # Update drop probability using PI controller
                self.drop_probability += self.alpha * error + self.beta * error * self.update_interval
                self.drop_probability = max(0.0, min(1.0, self.drop_probability))
                
                self.last_update_time = current_time
            
            # Apply drop probability
            if random.random() < self.drop_probability:
                self.packets_dropped += 1
                return False
                
            if len(self.queue) >= self.queue_size:
                self.packets_dropped += 1
                return False
                
            self.queue.append(packet)
            return True
    
    def process_packet(self, current_time: float) -> Optional[Packet]:
        if not self.queue:
            return None
            
        packet = self.queue.pop(0)
        self.packets_processed += 1
        
        # Calculate queue delay
        queue_delay = current_time - packet.arrival_time
        self.total_queue_delay += queue_delay
        
        return packet

class Server:
    def __init__(self):
        self.packets_processed = 0
        
    def process_packet(self, packet: Packet, current_time: float) -> Packet:
        # Simulate processing delay
        processing_time = packet.size / 2000  # Assuming 2Mbps processing speed
        packet.departure_time = current_time + processing_time
        self.packets_processed += 1
        return packet

class NetworkSimulation:
    def __init__(self, queue_size: int = 100, simulation_time: int = 60):
        self.queue_size = queue_size
        self.simulation_time = simulation_time
        self.results = {}
        
        # Packet size ranges (in bytes) for different host types
        self.packet_size_ranges = {
            HostType.FTP: (500, 1500),
            HostType.WEB: (100, 1000),
            HostType.VIDEO: (1000, 5000)
        }
        
    def run_simulation(self, aqm_type: str):
        # Set random seed for reproducibility
        random.seed(42)
        
        # Create network components
        hosts = [Host(host_type, self.packet_size_ranges[host_type]) 
                for host_type in HostType]
        router = Router(self.queue_size, aqm_type)
        servers = [Server() for _ in range(3)]
        
        current_time = 0.0
        time_step = 0.001  # 1ms time step
        
        while current_time < self.simulation_time:
            # Generate packets from hosts
            for host in hosts:
                if host.packets_sent < 100:  # Generate exactly 100 packets per host
                    if random.random() < 0.1:  # 10% chance to generate packet each time step
                        packet = host.generate_packet(current_time)
                        if router.receive_packet(packet, current_time):
                            host.packets.append(packet)
            
            # Process packets in router
            packet = router.process_packet(current_time)
            if packet:
                # Forward to server
                server_idx = packet.source.value % len(servers)
                server = servers[server_idx]
                processed_packet = server.process_packet(packet, current_time)
                
                # Update host statistics
                host_idx = packet.source.value
                host = hosts[host_idx]
                host.packets_received += 1
                host.total_delay += processed_packet.delay
            
            current_time += time_step
        
        # Collect metrics
        metrics = self._collect_metrics(hosts, router, servers)
        self.results[aqm_type] = metrics
        
    def _collect_metrics(self, hosts: List[Host], router: Router, servers: List[Server]) -> Dict:
        metrics = {
            'total_packets_sent': sum(host.packets_sent for host in hosts),
            'total_packets_received': sum(host.packets_received for host in hosts),
            'packets_dropped': router.packets_dropped,
            'average_queue_delay': router.total_queue_delay / router.packets_processed if router.packets_processed > 0 else 0,
            'throughput': sum(host.packets_received for host in hosts) / self.simulation_time,
            'host_metrics': {}
        }
        
        # Collect per-host metrics
        for host in hosts:
            metrics['host_metrics'][host.host_type.name] = {
                'packets_sent': host.packets_sent,
                'packets_received': host.packets_received,
                'average_delay': host.total_delay / host.packets_received if host.packets_received > 0 else 0
            }
            
        return metrics
    
    def plot_results(self):
        try:
            # Create figure with subplots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            # Plot 1: Packet Loss Comparison
            aqm_types = list(self.results.keys())
            packet_loss = [self.results[aqm]['packets_dropped'] for aqm in aqm_types]
            ax1.bar(aqm_types, packet_loss)
            ax1.set_title('Packet Loss Comparison')
            ax1.set_ylabel('Number of Dropped Packets')
            
            # Plot 2: Average Queue Delay
            queue_delays = [self.results[aqm]['average_queue_delay'] for aqm in aqm_types]
            ax2.bar(aqm_types, queue_delays)
            ax2.set_title('Average Queue Delay')
            ax2.set_ylabel('Delay (seconds)')
            
            # Plot 3: Throughput
            throughputs = [self.results[aqm]['throughput'] for aqm in aqm_types]
            ax3.bar(aqm_types, throughputs)
            ax3.set_title('Throughput')
            ax3.set_ylabel('Packets per Second')
            
            # Plot 4: Per-Host Average Delay
            host_types = list(self.results[aqm_types[0]]['host_metrics'].keys())
            delays = {
                aqm: [self.results[aqm]['host_metrics'][host]['average_delay'] for host in host_types]
                for aqm in aqm_types
            }
            
            x = range(len(host_types))
            width = 0.25  # Adjusted for three algorithms
            
            for i, aqm in enumerate(aqm_types):
                ax4.bar([xi + i*width for xi in x], delays[aqm], width, label=aqm)
            
            ax4.set_title('Per-Host Average Delay')
            ax4.set_ylabel('Delay (seconds)')
            ax4.set_xticks([xi + width for xi in x])
            ax4.set_xticklabels(host_types)
            ax4.legend()
            
            plt.tight_layout()
            
            # Save the plot
            plt.savefig('simulation_results.png')
            print("Plot saved as 'simulation_results.png'")
            
            # Try to show the plot if possible
            try:
                plt.show()
            except Exception as e:
                print("Note: Could not display plot interactively. The plot has been saved to 'simulation_results.png'")
            
            plt.close()
            
        except Exception as e:
            print(f"Error generating plots: {str(e)}")
            print("Continuing with report generation...")

    def generate_report(self):
        report = {
            'simulation_parameters': {
                'queue_size': self.queue_size,
                'simulation_time': self.simulation_time,
                'packet_size_ranges': {k.name: v for k, v in self.packet_size_ranges.items()}
            },
            'results': self.results
        }
        
        with open('simulation_report.json', 'w') as f:
            json.dump(report, f, indent=4)

def main():
    try:
        # Create and run simulation
        sim = NetworkSimulation(queue_size=100, simulation_time=60)
        
        # Run FIFO simulation
        print("Running FIFO simulation...")
        sim.run_simulation("FIFO")
        
        # Run CODEL simulation
        print("Running CODEL simulation...")
        sim.run_simulation("CODEL")
        
        # Run PIE simulation
        print("Running PIE simulation...")
        sim.run_simulation("PIE")
        
        # Generate plots and report
        sim.plot_results()
        sim.generate_report()
        
        print("Simulation complete! Results saved in simulation_results.png and simulation_report.json")
        
    except Exception as e:
        print(f"Error during simulation: {str(e)}")

if __name__ == "__main__":
    main() 