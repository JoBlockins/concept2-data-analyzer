"""
Web-based Live Stroke Display
Opens in browser - large, easy-to-read numbers
"""

from flask import Flask, render_template
import threading
import webbrowser
import time
import os


class WebStrokeDisplay:
    """Web-based stroke length display"""
    
    def __init__(self, port=5000):
        self.port = port
        self.app = Flask(__name__)
        self.current_length = 0.0
        self.avg_length = 0.0
        self.recent_lengths = []
        self.last_stroke_count = 0
        self.running = False
        
        # Setup routes
        @self.app.route('/')
        def index():
            return self.get_html()
        
        @self.app.route('/data')
        def get_data():
            return {
                'current': round(self.current_length, 2),
                'average': round(self.avg_length, 2)
            }
    
    def get_html(self):
        """Generate the HTML display"""
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>Stroke Length Monitor</title>
    <style>
        body {
            background-color: #000;
            color: #fff;
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        .title {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 40px;
            color: #fff;
        }
        .metric {
            margin: 40px 0;
        }
        .label {
            font-size: 28px;
            margin-bottom: 10px;
        }
        .current .label {
            color: #00ffff;
        }
        .average .label {
            color: #ffa500;
        }
        .value {
            font-size: 120px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        }
        .current .value {
            color: #00ffff;
        }
        .average .value {
            color: #ffa500;
        }
        .unit {
            font-size: 48px;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="title">STROKE LENGTH MONITOR</div>
    
    <div class="metric current">
        <div class="label">CURRENT</div>
        <div>
            <span class="value" id="current">0.00</span>
            <span class="unit">m</span>
        </div>
    </div>
    
    <div class="metric average">
        <div class="label">5-STROKE AVERAGE</div>
        <div>
            <span class="value" id="average">0.00</span>
            <span class="unit">m</span>
        </div>
    </div>
    
    <script>
        function updateDisplay() {
            fetch('/data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('current').textContent = data.current.toFixed(2);
                    document.getElementById('average').textContent = data.average.toFixed(2);
                });
        }
        
        // Update every 200ms
        setInterval(updateDisplay, 200);
        updateDisplay();
    </script>
</body>
</html>
        '''
    
    def update(self, current_stroke_length, stroke_count):
        """Update the display with new data"""
        if stroke_count > self.last_stroke_count:
            self.last_stroke_count = stroke_count
            self.current_length = current_stroke_length
            
            # Update 5-stroke average
            self.recent_lengths.append(current_stroke_length)
            if len(self.recent_lengths) > 5:
                self.recent_lengths.pop(0)
            
            if self.recent_lengths:
                self.avg_length = sum(self.recent_lengths) / len(self.recent_lengths)
    
    def start(self):
        """Start the web server and open browser"""
        self.running = True
        
        # Start Flask in background thread
        server_thread = threading.Thread(
            target=lambda: self.app.run(port=self.port, debug=False, use_reloader=False),
            daemon=True
        )
        server_thread.start()
        
        # Wait a moment for server to start
        time.sleep(1)
        
        # Open browser
        url = f'http://localhost:{self.port}'
        webbrowser.open(url)
        print(f"\n📊 Stroke display opened in browser: {url}")
        print("   (If browser doesn't open, copy this URL manually)\n")
    
    def process_events(self):
        """Compatibility with tkinter version - does nothing for web version"""
        pass
    
    def stop(self):
        """Stop the display"""
        self.running = False


# Test code
if __name__ == "__main__":
    import random
    
    print("Starting web-based stroke display...")
    print("Press Ctrl+C to stop")
    
    display = WebStrokeDisplay()
    display.start()
    
    # Simulate strokes
    stroke_count = 0
    try:
        while True:
            stroke_count += 1
            stroke_length = 1.45 + random.uniform(-0.15, 0.15)
            display.update(stroke_length, stroke_count)
            time.sleep(1)
            print(f"Stroke {stroke_count}: {stroke_length:.2f}m")
    except KeyboardInterrupt:
        print("\nStopping...")
    
    display.stop()
