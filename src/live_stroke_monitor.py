"""
Live Stroke Length Monitor
Real-time graphical display of stroke length while rowing
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import threading
import time


class LiveStrokeMonitor:
    """Real-time graphical display of stroke length metrics"""
    
    def __init__(self, max_points=50):
        """
        max_points: how many data points to show on screen (last N strokes)
        """
        self.max_points = max_points
        
        # Data storage
        self.stroke_numbers = deque(maxlen=max_points)
        self.current_lengths = deque(maxlen=max_points)
        self.avg_5_lengths = deque(maxlen=max_points)
        
        self.stroke_count = 0
        self.recent_lengths = []
        
        # Thread control
        self.running = False
        self.fig = None
        self.ax = None
        
    def start(self):
        """Start the live display in a separate thread"""
        self.running = True
        
        # Create the plot
        plt.ion()  # Interactive mode
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.fig.canvas.manager.set_window_title('Live Stroke Length Monitor')
        
        # Initialize empty lines
        self.line_current, = self.ax.plot([], [], 'b-', linewidth=2, label='Current Stroke Length')
        self.line_avg, = self.ax.plot([], [], 'r--', linewidth=2, label='5-Stroke Average')
        
        # Setup plot
        self.ax.set_xlabel('Stroke Number', fontsize=14)
        self.ax.set_ylabel('Stroke Length (meters)', fontsize=14)
        self.ax.set_title('Real-Time Stroke Length Tracking', fontsize=16, fontweight='bold')
        self.ax.legend(loc='upper right', fontsize=12)
        self.ax.grid(True, alpha=0.3)
        
        # Set initial limits
        self.ax.set_xlim(0, self.max_points)
        self.ax.set_ylim(0, 2.0)  # Adjust based on your typical stroke length
        
        plt.show(block=False)
        
    def update(self, current_stroke_length, stroke_count):
        """
        Update the display with new data
        current_stroke_length: the stroke length in meters
        stroke_count: total stroke count
        """
        if not self.running:
            return
        
        # Only update on new strokes
        if stroke_count > self.stroke_count:
            self.stroke_count = stroke_count
            
            # Add to recent lengths for 5-stroke average
            self.recent_lengths.append(current_stroke_length)
            if len(self.recent_lengths) > 5:
                self.recent_lengths.pop(0)
            
            # Calculate 5-stroke average
            avg_5 = sum(self.recent_lengths) / len(self.recent_lengths)
            
            # Add to plot data
            self.stroke_numbers.append(stroke_count)
            self.current_lengths.append(current_stroke_length)
            self.avg_5_lengths.append(avg_5)
            
            # Update the plot
            self.line_current.set_data(list(self.stroke_numbers), list(self.current_lengths))
            self.line_avg.set_data(list(self.stroke_numbers), list(self.avg_5_lengths))
            
            # Adjust x-axis to show last N strokes
            if stroke_count > self.max_points:
                self.ax.set_xlim(stroke_count - self.max_points, stroke_count)
            
            # Auto-scale y-axis based on data
            if self.current_lengths:
                all_values = list(self.current_lengths) + list(self.avg_5_lengths)
                y_min = max(0, min(all_values) - 0.2)
                y_max = max(all_values) + 0.2
                self.ax.set_ylim(y_min, y_max)
            
            # Redraw
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
    
    def stop(self):
        """Stop the live display"""
        self.running = False
        if self.fig:
            plt.close(self.fig)


# Test code
if __name__ == "__main__":
    print("Testing Live Stroke Monitor...")
    print("This will simulate 30 strokes with varying lengths")
    
    import random
    
    monitor = LiveStrokeMonitor(max_points=30)
    monitor.start()
    
    # Simulate strokes
    for i in range(1, 31):
        # Simulate varying stroke length (1.3-1.6m)
        stroke_length = 1.45 + random.uniform(-0.15, 0.15)
        monitor.update(stroke_length, i)
        time.sleep(1)  # One stroke per second for demo
        print(f"Stroke {i}: {stroke_length:.2f}m")
    
    print("\nTest complete! Close the window to exit.")
    input("Press Enter to close...")
    monitor.stop()
