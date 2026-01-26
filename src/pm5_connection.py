"""
PM5 Connection Module
Handles USB connection to Concept2 PM5 monitor
"""

import pyrow
from typing import Optional, Dict, Any


class PM5Connection:
    """Manages connection to Concept2 PM5 monitor via USB"""
    
    def __init__(self):
        self.erg = None
        self.connected = False
    
    def connect(self) -> bool:
        """
        Attempt to connect to PM5 via USB
        Returns True if successful, False otherwise
        """
        try:
            # Find all connected ergs
            ergs = list(pyrow.find())
            
            if not ergs:
                print("No PM5 monitors found. Please check USB connection.")
                return False
            
            # Connect to the first erg found
            self.erg = pyrow.pyrow(ergs[0])
            self.connected = True
            print(f"Successfully connected to PM5!")
            return True
            
        except Exception as e:
            print(f"Error connecting to PM5: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Safely disconnect from the PM5"""
        if self.erg:
            try:
                # PyRow doesn't have an explicit close method
                # but we can clean up our reference
                self.erg = None
                self.connected = False
                print("Disconnected from PM5")
            except Exception as e:
                print(f"Error disconnecting: {e}")
    
    def get_monitor_data(self) -> Optional[Dict[str, Any]]:
        """
        Get current workout data from the monitor
        Returns dictionary with current metrics or None if error
        """
        if not self.connected or not self.erg:
            print("Not connected to PM5")
            return None
        
        try:
            # Get current monitor status
            monitor = self.erg.get_monitor()

            distance = monitor.get('distance', 0)
            stroke_count = monitor.get('strokes', 0)  # PyRow might use 'strokes' field
            
            # Calculate stroke length
            stroke_length = distance / stroke_count if stroke_count > 0 else 0
            
            
            # Return the data as a dictionary
            return {
                'time': monitor.get('time', 0),
                'distance': monitor.get('distance', 0),
                'stroke_rate': monitor.get('spm', 0),  # strokes per minute
                'pace': monitor.get('pace', 0),  # seconds per 500m
                'power': monitor.get('power', 0),  # watts
                'calories': monitor.get('calories', 0),
                'heart_rate': monitor.get('heartrate', 0),
                'stroke_count': 0  # PyRow might not have this, set to 0
                'stroke_length': round(stroke_length, 2) 
            }
            
        except Exception as e:
            print(f"Error reading monitor data: {e}")
            return None
    
    def get_status(self) -> str:
        """Get current status of the PM5"""
        if not self.connected:
            return "Disconnected"
        
        try:
            status = self.erg.get_status()
            return status.get('status', 'Unknown')
        except:
            return "Error reading status"
