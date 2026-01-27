"""
Data Visualization Module
Creates graphs and charts from workout data
"""

import matplotlib
matplotlib.use('TkAgg')  # Force interactive backend for Mac
import matplotlib.pyplot as plt

class DataVisualizer:
    """Creates visualizations of workout data"""
    
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
    
    def plot_stroke_length(self, save_path: str = None, show: bool = True):
        """
        Plot stroke length over time
        This is the key metric that Concept2 doesn't track!
        """
        if not self.data:
            print("No data to visualize")
            return
        
        times = [d['time'] for d in self.data]
        stroke_lengths = [d['stroke_length'] for d in self.data]
        
        plt.figure(figsize=(12, 6))
        plt.plot(times, stroke_lengths, 'b-', linewidth=2, label='Stroke Length')
        
        # Add average line
        avg_length = sum(stroke_lengths) / len(stroke_lengths)
        plt.axhline(y=avg_length, color='r', linestyle='--', 
                   label=f'Average: {avg_length:.2f}m')
        
        plt.xlabel('Time (seconds)', fontsize=12)
        plt.ylabel('Stroke Length (meters)', fontsize=12)
        plt.title('Stroke Length Over Time', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Graph saved to: {save_path}")
        
        if show:
            plt.show()
        
        plt.close()
    
    def plot_all_metrics(self, save_path: str = None, show: bool = True):
        """Create a combined dashboard with all key metrics"""
        if not self.data:
            print("No data to visualize")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Workout Dashboard', fontsize=16, fontweight='bold')
        
        times = [d['time'] for d in self.data]
        
        # Stroke Length
        stroke_lengths = [d['stroke_length'] for d in self.data]
        axes[0, 0].plot(times, stroke_lengths, 'b-', linewidth=2)
        avg_sl = sum(stroke_lengths) / len(stroke_lengths)
        axes[0, 0].axhline(y=avg_sl, color='r', linestyle='--', alpha=0.7)
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('Stroke Length (m)')
        axes[0, 0].set_title('Stroke Length (Custom Metric)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Pace
        paces = [d['pace'] for d in self.data if d['pace'] > 0]
        pace_times = [d['time'] for d in self.data if d['pace'] > 0]
        axes[0, 1].plot(pace_times, paces, 'g-', linewidth=2)
        if paces:
            avg_pace = sum(paces) / len(paces)
            axes[0, 1].axhline(y=avg_pace, color='r', linestyle='--', alpha=0.7)
        axes[0, 1].set_xlabel('Time (s)')
        axes[0, 1].set_ylabel('Pace (s/500m)')
        axes[0, 1].set_title('Pace')
        axes[0, 1].invert_yaxis()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Power
        powers = [d['power'] for d in self.data if d['power'] > 0]
        power_times = [d['time'] for d in self.data if d['power'] > 0]
        axes[1, 0].plot(power_times, powers, 'orange', linewidth=2)
        if powers:
            avg_power = sum(powers) / len(powers)
            axes[1, 0].axhline(y=avg_power, color='r', linestyle='--', alpha=0.7)
        axes[1, 0].set_xlabel('Time (s)')
        axes[1, 0].set_ylabel('Power (W)')
        axes[1, 0].set_title('Power Output')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Stroke Rate
        stroke_rates = [d['stroke_rate'] for d in self.data if d['stroke_rate'] > 0]
        spm_times = [d['time'] for d in self.data if d['stroke_rate'] > 0]
        axes[1, 1].plot(spm_times, stroke_rates, 'purple', linewidth=2)
        if stroke_rates:
            avg_spm = sum(stroke_rates) / len(stroke_rates)
            axes[1, 1].axhline(y=avg_spm, color='r', linestyle='--', alpha=0.7)
        axes[1, 1].set_xlabel('Time (s)')
        axes[1, 1].set_ylabel('Stroke Rate (spm)')
        axes[1, 1].set_title('Stroke Rate')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Dashboard saved to: {save_path}")
        
        if show:
            plt.show()
        
        plt.close()
# Test code
if __name__ == "__main__":
    print("Testing Data Visualizer...")
    
    # Create sample data
    sample_data = []
    for i in range(100):
        sample_data.append({
            'time': i * 2,
            'distance': i * 20,
            'stroke_rate': 35 + (i % 5),
            'pace': 100 + (i % 10),
            'power': 450 + (i % 50),
            'calories': i * 4,
            'heart_rate': 175,
            'stroke_count': i,
            'stroke_length': 1.4 - (i % 3) * 0.05
        })
    
    # Create visualizer
    viz = DataVisualizer(sample_data)
    
    # Show all graphs
    print("\nGenerating graphs...")
    viz.plot_all_metrics(save_path='graphs/test_dashboard.png', show=False)
    print("Graph saved! Opening...")
    
    import os
    os.system('open graphs/test_dashboard.png')
