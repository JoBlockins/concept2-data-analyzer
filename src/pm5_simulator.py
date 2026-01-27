"""
PM5 Data Simulator
Simulates realistic rowing data for testing without actual PM5 connection
"""

import random
import time
from typing import Dict, Any


class PM5Simulator:
    """Simulates PM5 monitor data for testing"""
    
    def __init__(self):
        self.connected = False
        self.workout_time = 0.0
        self.total_distance = 0
        self.stroke_count = 0
        self.is_rowing = False
        
        # Realistic rowing parameters
        self.target_spm = 35  # strokes per minute
        self.target_pace = 100  # 2:00/500m split
        self.last_stroke_time = 0
    
    def connect(self) -> bool:
        """Simulate connection to PM5"""
        print("Simulating PM5 connection...")
        time.sleep(0.5)
        self.connected = True
        print("Successfully connected to simulated PM5!")
        return True
    
    def disconnect(self):
        """Simulate disconnection"""
        self.connected = False
        print("Disconnected from simulated PM5")
    
    def get_monitor_data(self) -> Dict[str, Any]:
        """
        Generate realistic rowing data
        Simulates someone rowing at steady state
        """
        if not self.connected:
            return None
        
        # Simulate time passing
        current_time = time.time()
        
        # Initialize default values
        current_spm = 0
        current_pace = 0
        power = 0
        heart_rate = 140
        calories = 0
        
        # If rowing (simulate 80% of the time)
        if random.random() < 0.8:
            if not self.is_rowing:
                self.is_rowing = True
                self.last_stroke_time = current_time
            
            # Update workout time (increments in real-time)
            self.workout_time += 0.5
            
            # Simulate strokes
            time_since_last_stroke = current_time - self.last_stroke_time
            stroke_interval = 60.0 / self.target_spm  # time between strokes
            
            if time_since_last_stroke >= stroke_interval:
                self.stroke_count += 1
                self.last_stroke_time = current_time
                
                # Add distance for this stroke (realistic values)
                meters_per_stroke = 1.4 + random.uniform(-0.1, 0.15)
                self.total_distance += meters_per_stroke
            
            # Calculate metrics with realistic variation
            current_spm = self.target_spm + random.uniform(-3, 5)
            current_pace = self.target_pace + random.uniform(-5, 5)
            
            # Calculate power (watts) from pace
            # Formula: watts = 2.8 / (pace/500)^3
            pace_factor = (current_pace / 500.0) ** 3
            power = 2.8 / pace_factor if pace_factor > 0 else 0
            
            # Calories (rough estimate)
            calories = (self.workout_time / 3600) * (power * 4)
            
            # Simulated heart rate
            heart_rate = 175 + random.randint(-15, 15)
        
        # Calculate stroke length (distance per stroke)
        stroke_length = self.total_distance / self.stroke_count if self.stroke_count > 0 else 0
        
        return {
            'time': round(self.workout_time, 1),
            'distance': int(self.total_distance),
            'stroke_rate': round(current_spm, 1),
            'pace': round(current_pace, 1),
            'power': round(power, 1),
            'calories': round(calories, 1),
            'heart_rate': heart_rate,
            'stroke_count': self.stroke_count,
            'stroke_length': round(stroke_length, 2)
        }
    
    def get_status(self) -> str:
        """Return simulated status"""
        if self.is_rowing:
            return "Rowing"
        return "Ready"


# Test code
if __name__ == "__main__":
    print("Testing PM5 Simulator...")
    
    sim = PM5Simulator()
    sim.connect()
    
    print("\nSimulating 10 seconds of rowing data:\n")
    
    for i in range(20):  # 20 readings = 10 seconds at 0.5s intervals
        data = sim.get_monitor_data()
        print(f"Time: {data['time']:6.1f}s | "
              f"Distance: {data['distance']:6.0f}m | "
              f"SPM: {data['stroke_rate']:5.1f} | "
              f"Pace: {data['pace']:5.1f} | "
              f"Power: {data['power']:6.1f}W | "
              f"Strokes: {data['stroke_count']}")
        time.sleep(0.5)
    
    sim.disconnect()
