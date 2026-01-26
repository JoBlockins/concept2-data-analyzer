"""
Data Recorder Module
Records workout data to CSV files
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


class DataRecorder:
    """Records PM5 workout data to CSV files"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.current_file = None
        self.csv_writer = None
        self.file_handle = None
        self.recording = False
        
        # Data buffer for in-memory storage
        self.data_buffer: List[Dict[str, Any]] = []
    
    def start_recording(self, workout_name: str = None) -> str:
        """
        Start recording workout data to a new CSV file
        Returns the filename
        """
        if self.recording:
            print("Already recording. Stop current recording first.")
            return None
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if workout_name:
            filename = f"{workout_name}_{timestamp}.csv"
        else:
            filename = f"workout_{timestamp}.csv"
        
        filepath = self.data_dir / filename
        
        # Open file and create CSV writer
        self.file_handle = open(filepath, 'w', newline='')
        self.csv_writer = csv.DictWriter(
            self.file_handle,
            fieldnames=['timestamp', 'time', 'distance', 'stroke_rate', 
                       'pace', 'power', 'calories', 'heart_rate', 'stroke_count',
                       'stroke_length']
        )
        self.csv_writer.writeheader()
        
        self.current_file = filepath
        self.recording = True
        self.data_buffer = []
        
        print(f"Started recording to: {filepath}")
        return str(filepath)
    
    def record_data(self, data: Dict[str, Any]):
        """Record a single data point"""
        if not self.recording:
            print("Not currently recording. Call start_recording() first.")
            return
        
        # Add timestamp
        data_with_time = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            **data
        }
        
        # Write to CSV
        self.csv_writer.writerow(data_with_time)
        
        # Add to buffer
        self.data_buffer.append(data_with_time)
    
    def stop_recording(self) -> Path:
        """Stop recording and close the file"""
        if not self.recording:
            print("Not currently recording.")
            return None
        
        if self.file_handle:
            self.file_handle.close()
        
        filepath = self.current_file
        data_points = len(self.data_buffer)
        
        self.recording = False
        self.current_file = None
        self.csv_writer = None
        self.file_handle = None
        
        print(f"Stopped recording. Saved {data_points} data points to: {filepath}")
        return filepath
    
    def get_buffer_data(self) -> List[Dict[str, Any]]:
        """Get the current data buffer"""
        return self.data_buffer.copy()


# Test code
if __name__ == "__main__":
    print("Testing Data Recorder...")
    
    recorder = DataRecorder()
    
    # Start recording
    recorder.start_recording("test_workout")
    
    # Simulate recording some data
    for i in range(10):
        data = {
            'time': i * 0.5,
            'distance': i * 10,
            'stroke_rate': 24,
            'pace': 120,
            'power': 200,
            'calories': i * 2,
            'heart_rate': 145,
            'stroke_count': i,
            'stroke_length': 10.0
        }
        recorder.record_data(data)
    
    # Stop recording
    recorder.stop_recording()
    
    print("\nCheck the 'data' folder for the CSV file!")
