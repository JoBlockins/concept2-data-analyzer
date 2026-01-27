"""
Main application entry point
Simplified controls for better Mac compatibility
"""

import sys
import time
import threading
from pm5_connection import PM5Connection
from pm5_simulator import PM5Simulator
from data_recorder import DataRecorder
from data_analyzer import DataAnalyzer


class WorkoutMonitor:
    def __init__(self, pm5):
        self.pm5 = pm5
        self.recorder = DataRecorder()
        self.recording = False
        self.running = True
        self.command = None
        self.recent_stroke_lengths = []  # Track last 5 strokes
        self.last_stroke_count = 0
    
    def input_thread(self):
        """Separate thread to handle user input"""
        while self.running:
            try:
                cmd = input().strip().lower()
                self.command = cmd
            except:
                break
    
    def run(self):
        """Main monitoring loop"""
        # Start input thread
        input_handler = threading.Thread(target=self.input_thread, daemon=True)
        input_handler.start()
        
        print("\n" + "="*60)
        print("CONTROLS:")
        print("  Type 'start' and press Enter to start recording")
        print("  Type 'stop' and press Enter to stop recording and see analysis")
        print("  Type 'quit' and press Enter to exit")
        print("="*60)
        print("\nMonitoring workout data...\n")
        
        try:
            while self.running:
                # Check for commands
                if self.command:
                    cmd = self.command
                    self.command = None
                    
                    if cmd == 'start':
                        if not self.recording:
                            self.recorder.start_recording()
                            self.recording = True
                            print("\n🔴 RECORDING STARTED\n")
                        else:
                            print("\n⚠️  Already recording!\n")
                    
                    elif cmd == 'stop':
                        if self.recording:
                            filepath = self.recorder.stop_recording()
                            self.recording = False
                            print(f"\n⏹️  RECORDING STOPPED\n")
                            
                            # Analyze the workout
                            print("Analyzing workout...")
                            data = self.recorder.get_buffer_data()
                            analyzer = DataAnalyzer(data)
                            analyzer.print_summary()
                            
                            # Show splits
                            splits = analyzer.get_split_analysis(500)
                            if splits:
                                print("\n500m SPLIT ANALYSIS:")
                                print("-"*60)
                                for split in splits:
                                    print(f"Split {split['split_number']}: "
                                          f"DPS: {split['avg_stroke_length']:.2f}m | "
                                          f"Pace: {analyzer.format_pace(split['avg_pace'])} | "
                                          f"Power: {split['avg_power']:.0f}W")
                                print("-"*60 + "\n")
                            
                            print("Type 'start' to record another workout, or 'quit' to exit\n")
                        else:
                            print("\n⚠️  Not recording!\n")
                    
                    elif cmd == 'quit' or cmd == 'q':
                        if self.recording:
                            print("\n⚠️  Still recording! Stopping recording first...\n")
                            self.recorder.stop_recording()
                        print("Quitting...")
                        self.running = False
                        break
                
                # Get current data
                data = self.pm5.get_monitor_data()
                
                if data:
                    # Record if recording is active
                    if self.recording:
                        self.recorder.record_data(data)
                    
                    # Track stroke length changes
                    current_stroke_count = data.get('stroke_count', 0)
                    if current_stroke_count > self.last_stroke_count:
                        # New stroke detected
                        self.recent_stroke_lengths.append(data['stroke_length'])
                        # Keep only last 5 strokes
                        if len(self.recent_stroke_lengths) > 5:
                            self.recent_stroke_lengths.pop(0)
                        self.last_stroke_count = current_stroke_count
                    
                    # Calculate 5-stroke average
                    if len(self.recent_stroke_lengths) > 0:
                        avg_5_strokes = sum(self.recent_stroke_lengths) / len(self.recent_stroke_lengths)
                    else:
                        avg_5_strokes = 0
                    
                    # Display current metrics with stroke length tracking
                    status = "🔴 REC" if self.recording else "⚪️    "
                    print(f"{status} | "
                          f"Time: {data['time']:6.1f}s | "
                          f"Dist: {data['distance']:6.0f}m | "
                          f"SPM: {data['stroke_rate']:5.1f} | "
                          f"Current DPS: {data['stroke_length']:5.2f}m | "
                          f"Avg(5): {avg_5_strokes:5.2f}m | "
                          f"Pace: {data['pace']:5.1f} | "
                          f"Power: {data['power']:6.1f}W", end='\r')                

                # Wait before next reading
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by Ctrl+C")
            if self.recording:
                print("Stopping recording...")
                self.recorder.stop_recording()
        finally:
            self.running = False


def main():
    print("="*60)
    print("CONCEPT2 PM5 DATA ANALYZER")
    print("="*60)
    
    # Check if user wants to use simulator
    use_simulator = False
    
    if len(sys.argv) > 1 and sys.argv[1] == "--simulate":
        use_simulator = True
        print("\n🔧 Running in SIMULATION mode")
        pm5 = PM5Simulator()
    else:
        print("\n📡 Running in REAL mode (connecting to actual PM5)")
        print("   Tip: Use --simulate flag to test without PM5\n")
        pm5 = PM5Connection()
    
    # Connect
    if not pm5.connect():
        print("❌ Unable to connect. Exiting.")
        return
    
    print(f"✅ Status: {pm5.get_status()}")
    
    # Run monitor
    monitor = WorkoutMonitor(pm5)
    monitor.run()
    
    # Disconnect
    pm5.disconnect()
    print("\n✅ Program ended.\n")


if __name__ == "__main__":
    main()
