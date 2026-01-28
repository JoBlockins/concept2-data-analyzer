"""
PM5 Connection Module
Handles USB connection to Concept2 PM5 monitor
"""

from typing import Optional, Dict, Any

# Set up USB backend BEFORE importing pyrow
import usb.core
import usb.backend.libusb1

# Initialize libusb backend for Mac
_backend = usb.backend.libusb1.get_backend(
    find_library=lambda x: "/opt/homebrew/lib/libusb-1.0.dylib"
)

# Set it as the default backend
import os
os.environ['PYUSB_DEBUG'] = 'debug'

# Now import pyrow
import pyrow.pyrow as pyrow


class PM5Connection:
    """Manages connection to Concept2 PM5 monitor via USB"""
    
    def __init__(self):
        self.erg = None
        self.connected = False
        self.backend = _backend
    
    def connect(self) -> bool:
        """
        Attempt to connect to PM5 via USB
        Returns True if successful, False otherwise
        """
        try:
            # Find USB devices with our backend
            devices = list(usb.core.find(find_all=True, backend=self.backend))
            print(f"Found {len(devices)} USB devices")
            
            # Look for Concept2 device (vendor ID 0x17a4)
            c2_devices = [d for d in devices if d.idVendor == 0x17a4]
            
            if not c2_devices:
                print("No PM5 monitors found. Please check USB connection.")
                print("Make sure the PM5 is powered on.")
                return False
            
            print(f"Found {len(c2_devices)} Concept2 device(s)")
            
            # Connect using PyRow
            self.erg = pyrow.PyErg(c2_devices[0])
            self.connected = True
            print("Successfully connected to PM5!")
            return True
            
        except Exception as e:
            print(f"Error connecting to PM5: {e}")
            import traceback
            traceback.print_exc()
            self.connected = False
            return False
    
    def disconnect(self):
        """Safely disconnect from the PM5"""
        if self.erg:
            try:
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
            stroke_count = monitor.get('strokes', 0)
            
            # Calculate stroke length
            stroke_length = distance / stroke_count if stroke_count > 0 else 0
            
            # Return the data as a dictionary
            return {
                'time': monitor.get('time', 0),
                'distance': distance,
                'stroke_rate': monitor.get('spm', 0),
                'pace': monitor.get('pace', 0),
                'power': monitor.get('power', 0),
                'calories': monitor.get('calories', 0),
                'heart_rate': monitor.get('heartrate', 0),
                'stroke_count': stroke_count,
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
