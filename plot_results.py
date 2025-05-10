import matplotlib.pyplot as plt
import numpy as np

# Data for packet processing
traffic_types = ['Web', 'FTP', 'Video']
fifo_packets = [970, 942, 951]  # FIFO processed packets
pie_packets = [974, 947, 950]   # PIE processed packets

# Data for dropped packets
fifo_dropped = [30, 58, 49]     # FIFO dropped packets
pie_dropped = [26, 53, 50]      # PIE dropped packets

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 14))

# Plot 1: Packet Processing Comparison
x = np.arange(len(traffic_types))
width = 0.35

# Plot processed packets
ax1.bar(x - width/2, fifo_packets, width, label='FIFO Processed', color='blue', alpha=0.7)
ax1.bar(x + width/2, pie_packets, width, label='PIE Processed', color='red', alpha=0.7)

# Plot dropped packets on top
ax1.bar(x - width/2, fifo_dropped, width, bottom=fifo_packets, label='FIFO Dropped', color='lightblue', alpha=0.7)
ax1.bar(x + width/2, pie_dropped, width, bottom=pie_packets, label='PIE Dropped', color='pink', alpha=0.7)

ax1.set_ylabel('Number of Packets')
ax1.set_title('Packet Processing and Dropping Comparison')
ax1.set_xticks(x)
ax1.set_xticklabels(traffic_types)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Add value labels
for i, v in enumerate(fifo_packets):
    ax1.text(i - width/2, v/2, f'{v}\n({v/10:.1f}%)', ha='center', va='center')
for i, v in enumerate(pie_packets):
    ax1.text(i + width/2, v/2, f'{v}\n({v/10:.1f}%)', ha='center', va='center')

# Plot 2: Success Rate Comparison
success_rates_fifo = [97.0, 94.2, 95.1]  # FIFO success rates
success_rates_pie = [97.4, 94.7, 95.0]   # PIE success rates

ax2.bar(x - width/2, success_rates_fifo, width, label='FIFO', color='blue', alpha=0.7)
ax2.bar(x + width/2, success_rates_pie, width, label='PIE', color='red', alpha=0.7)

ax2.set_ylabel('Success Rate (%)')
ax2.set_title('Packet Processing Success Rate Comparison')
ax2.set_xticks(x)
ax2.set_xticklabels(traffic_types)
ax2.legend()
ax2.grid(True, alpha=0.3)

# Add value labels
for i, v in enumerate(success_rates_fifo):
    ax2.text(i - width/2, v + 0.5, f'{v:.1f}%', ha='center')
for i, v in enumerate(success_rates_pie):
    ax2.text(i + width/2, v + 0.5, f'{v:.1f}%', ha='center')

# Adjust layout and save
plt.tight_layout()
plt.savefig('simulation_results_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("Plot has been saved as 'simulation_results_comparison.png'") 