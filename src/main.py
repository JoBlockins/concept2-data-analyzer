"""
Main application entry point
Supports both real PM5 and simulated data
"""

import sys
import time
from pm5_connection import PM5Connection
from pm5_simulator import PM5Simulator


def main():
    print("=== Concept2 PM5 Data Analyzer ===\n")
    
    # Check if user wants to use simulator
    use_simulator = False
    
    if len(sys.argv) > 1 and sys.argv[1] == "--simulate":
        use_simulator = True
        print("Running in SIMULATION mode")
        pm5 = PM5Simulator()
    else:
        print("Running in REAL mode (connecting to actual PM5)")
        print("Tip: Use --simulate flag to test without PM5 connected\n")
        pm5 = PM5Connection()
    
    # Connect
    if not pm5.connect():
        print("Unable to connect. Exiting.")
        return
    
    print(f"\nStatus: {pm5.get_status()}")
    print("\nMonitoring workout data (Press Ctrl+C to stop)...\n")
    
    try:
        while True:
            # Get current data
            data = pm5.get_monitor_data()
            
            if data:
                # Display current metrics
                print(f"Time: {data['time']:6.1f}s | "
                      f"Distance: {data['distance']:6.0f}m | "
                      f"SPM: {data['stroke_rate']:5.1f} | "
                      f"DPS: {data['stroke_length']:5.2f}m | " 
                      f"Pace: {data['pace']:5.1f} | "
                      f"Power: {data['power']:6.1f}W | "
                      f"HR: {data['heart_rate']:3.0f}")
            
            # Wait before next reading
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\nStopping monitoring...")
    finally:
        pm5.disconnect()
        print("Program ended.")


if __name__ == "__main__":
    main()
