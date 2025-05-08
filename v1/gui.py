from classes import *
import tkinter as tk
from tkinter import messagebox
import tkinter as tk
import time
import threading


class Wire:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

class Office:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nodes = []
        self.wires = []

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def connect_nodes(self, node1, node2):
        self.add_node(node1)
        self.add_node(node2)
        wire = Wire(node1, node2)
        self.wires.append(wire)


    def send_packet_gui(self, canvas, source, destination, packet):
        """ Animate packet movement in GUI from source to destination with ID display """
        def animate_packet():
            start_x, start_y = self.node_positions[source]
            end_x, end_y = self.node_positions[destination]

            print(f"📦 Packet {packet.packet_id} created. Sending from Node {source.node_id} to Node {destination.node_id}.")

            # Create packet representation (red circle)
            packet_obj = canvas.create_oval(start_x - 5, start_y - 5, start_x + 5, start_y + 5, fill="red")
            packet_label = canvas.create_text(start_x, start_y - 15, text=f"📦 {packet.packet_id}", font=("Arial", 10))

            dx = (end_x - start_x) / 50  # Move in small steps
            dy = (end_y - start_y) / 50

            for _ in range(50):  # Move smoothly to destination
                canvas.move(packet_obj, dx, dy)
                canvas.move(packet_label, dx, dy)
                canvas.update()
                time.sleep(0.02)

            # Remove packet after reaching destination
            canvas.delete(packet_obj)
            canvas.delete(packet_label)

            print(f"✅ Packet {packet.packet_id} received at Node {destination.node_id}.")

        # Run animation in a separate thread
        threading.Thread(target=animate_packet).start()

    def display_network_gui(self, packets=[], time_generate=[]):
        root = tk.Tk()
        root.title("Office Network")

        canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white")
        canvas.pack()

        # Position nodes dynamically
        self.node_positions = {}
        for node in self.nodes:
            if isinstance(node, Router):
                self.node_positions[node] = (self.width // 2, self.height // 2)
            elif isinstance(node, Host):
                if not any(n for n in self.node_positions if isinstance(n, Host)):  # First host (Left)
                    self.node_positions[node] = (self.width // 4, self.height // 2)
                else:  # Second host (Right)
                    self.node_positions[node] = (self.width * 3 // 4, self.height // 2)

        # **Draw nodes with increased size**
        for node in self.nodes:
            x, y = self.node_positions[node]
            canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill="lightblue")  # Enlarged nodes
            canvas.create_text(x, y, text=node.icon, font=("Arial", 30,))  # Larger font for icons
            canvas.create_text(x, y + 10, text=node.node_id, font=("Arial", 10,))  # Larger node ID

        # **Draw thicker wires**
        for wire in self.wires:
            node1_x, node1_y = self.node_positions[wire.node1]
            node2_x, node2_y = self.node_positions[wire.node2]
            canvas.create_line(node1_x, node1_y, node2_x, node2_y, width=2, fill="black")  # Thicker lines

        # Simulate packet movement (unchanged)
        for i, packet in enumerate(packets):
            root.after(int(time_generate[i] * 1000), lambda p=packet: self.send_packet_gui(canvas, self.nodes[1], self.nodes[0], p))
            root.after(int(time_generate[i] * 1000) + 2000, lambda p=packet: self.send_packet_gui(canvas, self.nodes[0], self.nodes[2], p))

        root.mainloop()
