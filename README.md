# Concept2 PM5 Data Analyzer

Real-time data recording and analysis application for Concept2 rowing machines with PM5 displays.

## Project Overview
This application connects to a Concept2 rowing machine via USB to collect real-time performance data during workouts. Built as a personal project to enhance training analysis for competitive rowing.

## Features (Planned)
- ✅ USB connection to PM5 monitor
- ⏳ Real-time data collection (stroke rate, split, watts, etc.)
- ⏳ Stroke-by-stroke analysis
- ⏳ Performance visualization
- ⏳ Workout session recording
- ⏳ Export to CSV for further analysis

## Technical Stack
- **Language**: Python 3.8+
- **Hardware**: Concept2 PM5 monitor
- **Connection**: USB cable
- **Platform**: Cross-platform (Mac development, Windows deployment)

## Requirements
- Python 3.8 or higher
- Concept2 PM5 Performance Monitor
- USB A-B cable (standard printer cable)
- PyRow library
- PyUSB library

## Installation
```bash
# Clone the repository
git clone https://github.com/JoBlockins/concept2-data-analyzer.git
cd concept2-data-analyzer

# Install dependencies
pip install -r requirements.txt
```

## Development Status
🚧 **In Active Development** - January 2026

Current Phase: Initial setup and PM5 connection development

## Author
**JoBlockins** - Bedford High School Rowing Team & Amoskeag Rowing Club

## License
MIT License - See LICENSE file for details

## Development Notes

### Current Status (January 26, 2026)
✅ **Completed Features:**
- PM5 USB connection module
- Data simulator for testing without hardware
- Real-time data monitoring with live display
- Interactive recording (start/stop commands)
- Stroke length calculation and tracking (custom metric not in Concept2 app)
- Post-workout analysis with detailed statistics
- 500m split analysis
- CSV data export
- All modules tested and working in simulation mode

🔜 **Next Steps (After Wednesday when USB cable arrives):**
- Test with real PM5 hardware
- Verify stroke length accuracy with actual erg
- May need to adjust PyRow field names based on real PM5 data

💡 **Future Enhancements:**
- Data visualization (graphs of stroke length, pace, power over time)
- Compare multiple workouts
- Enhanced GUI with buttons and live graphs
- Interval workout simulator
- Export to other formats (Excel, Google Sheets)

### Testing the Application
```bash
# Activate virtual environment
source venv/bin/activate

# Run with simulator
python3 src/main.py --simulate

# Commands:
#   Type 'start' + Enter to begin recording
#   Type 'stop' + Enter to stop and see analysis
#   Type 'quit' + Enter to exit

# When cable arrives Wednesday, test with real PM5:
python3 src/main.py
```

### Project Structure
- `src/pm5_connection.py` - Real PM5 USB connection
- `src/pm5_simulator.py` - Simulated data for testing
- `src/data_recorder.py` - Records workout data to CSV
- `src/data_analyzer.py` - Calculates statistics and splits
- `src/main.py` - Main application with interactive controls
- `data/` - Saved workout CSV files (not committed to git)
