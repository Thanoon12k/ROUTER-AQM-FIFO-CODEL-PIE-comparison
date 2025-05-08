import simpy
import random
import numpy as np
import matplotlib.pyplot as plt
from network_components import Host, Router, Server, HostType
import pandas as pd
from typing import Dict, List
import json

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
        np.random.seed(42)
        
        # Create simulation environment
        env = simpy.Environment()
        
        # Create servers
        servers = [Server(env, []) for _ in range(3)]
        
        # Create router
        router = Router(env, self.queue_size, aqm_type, servers)
        
        # Create hosts
        hosts = []
        for host_type in HostType:
            host = Host(env, host_type, self.packet_size_ranges[host_type], router)
            hosts.append(host)
            env.process(host.send_packet())
        
        # Update server references to hosts
        for server in servers:
            server.hosts = hosts
        
        # Run simulation
        env.run(until=self.simulation_time)
        
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
            metrics['host_metrics'][host.host_type.value] = {
                'packets_sent': host.packets_sent,
                'packets_received': host.packets_received,
                'average_delay': host.total_delay / host.packets_received if host.packets_received > 0 else 0
            }
            
        return metrics
    
    def plot_results(self):
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
        
        x = np.arange(len(host_types))
        width = 0.35
        
        for i, aqm in enumerate(aqm_types):
            ax4.bar(x + i*width, delays[aqm], width, label=aqm)
        
        ax4.set_title('Per-Host Average Delay')
        ax4.set_ylabel('Delay (seconds)')
        ax4.set_xticks(x + width/2)
        ax4.set_xticklabels(host_types)
        ax4.legend()
        
        plt.tight_layout()
        plt.savefig('simulation_results.png')
        plt.close()
    
    def generate_report(self):
        report = {
            'simulation_parameters': {
                'queue_size': self.queue_size,
                'simulation_time': self.simulation_time,
                'packet_size_ranges': {k.value: v for k, v in self.packet_size_ranges.items()}
            },
            'results': self.results
        }
        
        with open('simulation_report.json', 'w') as f:
            json.dump(report, f, indent=4)

def main():
    # Create and run simulation
    sim = NetworkSimulation(queue_size=100, simulation_time=60)
    
    # Run FIFO simulation
    print("Running FIFO simulation...")
    sim.run_simulation("FIFO")
    
    # Run CODEL simulation
    print("Running CODEL simulation...")
    sim.run_simulation("CODEL")
    
    # Generate plots and report
    sim.plot_results()
    sim.generate_report()
    
    print("Simulation complete! Results saved in simulation_results.png and simulation_report.json")

if __name__ == "__main__":
    main() 