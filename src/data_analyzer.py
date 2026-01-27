"""
Data Analysis Module
Analyzes recorded workout data and generates statistics
"""

from typing import Dict, List, Any
import statistics


class DataAnalyzer:
    """Analyzes workout data and calculates performance metrics"""
    
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Calculate summary statistics for the workout"""
        if not self.data:
            return {}
        
        # Extract metrics from data
        stroke_lengths = [d['stroke_length'] for d in self.data if d.get('stroke_length', 0) > 0]
        stroke_rates = [d['stroke_rate'] for d in self.data if d.get('stroke_rate', 0) > 0]
        paces = [d['pace'] for d in self.data if d.get('pace', 0) > 0]
        powers = [d['power'] for d in self.data if d.get('power', 0) > 0]
        
        # Get final values
        final_data = self.data[-1]
        total_time = final_data.get('time', 0)
        total_distance = final_data.get('distance', 0)
        total_strokes = final_data.get('stroke_count', 0)
        
        # Calculate averages
        avg_stroke_length = statistics.mean(stroke_lengths) if stroke_lengths else 0
        avg_stroke_rate = statistics.mean(stroke_rates) if stroke_rates else 0
        avg_pace = statistics.mean(paces) if paces else 0
        avg_power = statistics.mean(powers) if powers else 0
        
        # Calculate consistency (standard deviation as % of mean)
        if len(stroke_lengths) > 1:
            stroke_length_stdev = statistics.stdev(stroke_lengths)
            stroke_length_consistency = (1 - (stroke_length_stdev / avg_stroke_length)) * 100
        else:
            stroke_length_consistency = 100
        
        # Find best/worst stroke lengths
        best_stroke_length = max(stroke_lengths) if stroke_lengths else 0
        worst_stroke_length = min(stroke_lengths) if stroke_lengths else 0
        
        return {
            'total_time': total_time,
            'total_distance': total_distance,
            'total_strokes': total_strokes,
            'avg_stroke_length': avg_stroke_length,
            'best_stroke_length': best_stroke_length,
            'worst_stroke_length': worst_stroke_length,
            'stroke_length_consistency': stroke_length_consistency,
            'avg_stroke_rate': avg_stroke_rate,
            'avg_pace': avg_pace,
            'avg_power': avg_power,
            'avg_calories_per_hour': (final_data.get('calories', 0) / (total_time / 3600)) if total_time > 0 else 0
        }
    
    def format_time(self, seconds: float) -> str:
        """Convert seconds to MM:SS.d format"""
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}:{secs:04.1f}"
    
    def format_pace(self, pace_seconds: float) -> str:
        """Convert pace in seconds to M:SS.d per 500m format"""
        mins = int(pace_seconds // 60)
        secs = pace_seconds % 60
        return f"{mins}:{secs:04.1f}"
    
    def print_summary(self):
        """Print a formatted summary of the workout"""
        stats = self.get_summary_stats()
        
        if not stats:
            print("No data to analyze.")
            return
        
        print("\n" + "="*60)
        print("WORKOUT SUMMARY")
        print("="*60)
        
        print(f"\nTotal Time:     {self.format_time(stats['total_time'])}")
        print(f"Total Distance: {stats['total_distance']:.0f} meters")
        print(f"Total Strokes:  {stats['total_strokes']}")
        
        print(f"\n--- STROKE LENGTH (Custom Metric) ---")
        print(f"Average:        {stats['avg_stroke_length']:.2f} m/stroke")
        print(f"Best:           {stats['best_stroke_length']:.2f} m/stroke")
        print(f"Worst:          {stats['worst_stroke_length']:.2f} m/stroke")
        print(f"Consistency:    {stats['stroke_length_consistency']:.1f}%")
        
        print(f"\n--- PERFORMANCE METRICS ---")
        print(f"Avg Stroke Rate: {stats['avg_stroke_rate']:.1f} spm")
        print(f"Avg Pace:        {self.format_pace(stats['avg_pace'])} /500m")
        print(f"Avg Power:       {stats['avg_power']:.0f} watts")
        print(f"Calories/Hour:   {stats['avg_calories_per_hour']:.0f} cal/hr")
        
        print("="*60 + "\n")
    
    def get_split_analysis(self, split_distance: int = 500) -> List[Dict[str, Any]]:
        """
        Analyze performance by splits
        split_distance: distance for each split in meters (default 500m)
        """
        splits = []
        current_split = {'start_idx': 0, 'start_distance': 0}
        
        for i, point in enumerate(self.data):
            distance = point.get('distance', 0)
            
            # Check if we've completed a split
            if distance >= current_split['start_distance'] + split_distance:
                # Calculate split metrics
                split_data = self.data[current_split['start_idx']:i+1]
                
                if split_data:
                    split_stroke_lengths = [d['stroke_length'] for d in split_data if d.get('stroke_length', 0) > 0]
                    split_paces = [d['pace'] for d in split_data if d.get('pace', 0) > 0]
                    split_powers = [d['power'] for d in split_data if d.get('power', 0) > 0]
                    
                    split_info = {
                        'split_number': len(splits) + 1,
                        'distance': split_distance,
                        'avg_stroke_length': statistics.mean(split_stroke_lengths) if split_stroke_lengths else 0,
                        'avg_pace': statistics.mean(split_paces) if split_paces else 0,
                        'avg_power': statistics.mean(split_powers) if split_powers else 0,
                        'time': split_data[-1]['time'] - split_data[0]['time']
                    }
                    
                    splits.append(split_info)
                
                # Start new split
                current_split = {'start_idx': i, 'start_distance': distance}
        
        return splits


# Test code
if __name__ == "__main__":
    print("Testing Data Analyzer...")
    
    # Create sample data
    sample_data = []
    for i in range(100):
        sample_data.append({
            'time': i * 2,
            'distance': i * 20,
            'stroke_rate': 24 + (i % 5),
            'pace': 120 + (i % 10),
            'power': 200 + (i % 20),
            'calories': i * 4,
            'heart_rate': 145,
            'stroke_count': i,
            'stroke_length': 10.0 - (i % 3) * 0.5
        })
    
    # Analyze
    analyzer = DataAnalyzer(sample_data)
    analyzer.print_summary()
    
    # Show splits
    print("\n500m SPLIT ANALYSIS:")
    splits = analyzer.get_split_analysis(500)
    for split in splits:
        print(f"Split {split['split_number']}: "
              f"DPS: {split['avg_stroke_length']:.2f}m, "
              f"Pace: {split['avg_pace']:.1f}s, "
              f"Power: {split['avg_power']:.0f}W")
