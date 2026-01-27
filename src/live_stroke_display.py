"""
Live Stroke Length Display
Large numeric display of current and average stroke length
"""

import tkinter as tk
from tkinter import font
from collections import deque


class LiveStrokeDisplay:
    """Large numeric display for stroke length metrics"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stroke Length Monitor")
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Set window size and position
        window_width = 600
        window_height = 400
        
        # Position in top-right corner of screen
        screen_width = self.root.winfo_screenwidth()
        x_position = screen_width - window_width - 20
        y_position = 20
        
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.configure(bg='black')
        
        # Create large fonts
        title_font = font.Font(family='Helvetica', size=24, weight='bold')
        number_font = font.Font(family='Helvetica', size=72, weight='bold')
        label_font = font.Font(family='Helvetica', size=18)
        
        # Title
        title = tk.Label(
            self.root,
            text="STROKE LENGTH",
            font=title_font,
            bg='black',
            fg='white'
        )
        title.pack(pady=20)
        
        # Current stroke length
        current_label = tk.Label(
            self.root,
            text="CURRENT",
            font=label_font,
            bg='black',
            fg='cyan'
        )
        current_label.pack()
        
        self.current_display = tk.Label(
            self.root,
            text="0.00 m",
            font=number_font,
            bg='black',
            fg='cyan'
        )
        self.current_display.pack(pady=10)
        
        # 5-stroke average
        avg_label = tk.Label(
            self.root,
            text="5-STROKE AVERAGE",
            font=label_font,
            bg='black',
            fg='orange'
        )
        avg_label.pack(pady=(30, 0))
        
        self.avg_display = tk.Label(
            self.root,
            text="0.00 m",
            font=number_font,
            bg='black',
            fg='orange'
        )
        self.avg_display.pack(pady=10)
        
        # Data tracking
        self.recent_lengths = deque(maxlen=5)
        self.last_stroke_count = 0
        
        # Start update loop
        self.running = True
    
    def update(self, current_stroke_length, stroke_count):
        """Update the display with new stroke data"""
        if not self.running:
            return
        
        # Only update on new strokes
        if stroke_count > self.last_stroke_count:
            self.last_stroke_count = stroke_count
            
            # Add to recent lengths
            self.recent_lengths.append(current_stroke_length)
            
            # Update current display
            self.current_display.config(text=f"{current_stroke_length:.2f} m")
            
            # Calculate and update 5-stroke average
            if len(self.recent_lengths) > 0:
                avg = sum(self.recent_lengths) / len(self.recent_lengths)
                self.avg_display.config(text=f"{avg:.2f} m")
    
    def start(self):
        """Start the display (non-blocking)"""
        self.root.update()
    
    def process_events(self):
        """Process GUI events (call this regularly from main loop)"""
        if self.running:
            try:
                self.root.update()
            except tk.TclError:
                self.running = False
    
    def stop(self):
        """Close the display"""
        self.running = False
        try:
            self.root.destroy()
        except:
            pass


# Test code
if __name__ == "__main__":
    import time
    import random
    
    print("Testing Live Stroke Display...")
    print("A window will appear with large numbers")
    print("Press Ctrl+C to stop")
    
    display = LiveStrokeDisplay()
    display.start()
    
    # Simulate strokes
    stroke_count = 0
    try:
        while display.running:
            stroke_count += 1
            stroke_length = 1.45 + random.uniform(-0.15, 0.15)
            
            display.update(stroke_length, stroke_count)
            display.process_events()
            
            time.sleep(1)  # One stroke per second
            
    except KeyboardInterrupt:
        print("\nStopping...")
    
    display.stop()
    print("Display closed")
