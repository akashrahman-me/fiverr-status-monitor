import csv
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.patches as patches

# Read data from CSV file
timestamps = []
statuses = []

with open("status.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) == 2:
            t, s = row
            timestamps.append(datetime.fromisoformat(t.split("+")[0]))
            statuses.append(s)

# Color mapping
color_map = {"ONLINE": "#10B981", "ERROR": "#F59E0B", "OFFLINE": "#EF4444"}

# Group data by hour
hourly_data = {}
for ts, status in zip(timestamps, statuses):
    hour_key = ts.strftime('%Y-%m-%d %H:00')  # Include date to avoid mixing different days
    if hour_key not in hourly_data:
        hourly_data[hour_key] = []
    hourly_data[hour_key].append((ts, status))

# Create figure with rows for each hour
hours = sorted(hourly_data.keys())
num_rows = len(hours)
fig, ax = plt.subplots(figsize=(14, num_rows * 1.5))

# Set up the canvas
ax.set_xlim(0, 4)
ax.set_ylim(-0.8, num_rows)
ax.axis('off')

# Remove all spines (axis lines)
for spine in ax.spines.values():
    spine.set_visible(False)

# Draw grid for each hour
for row_idx, hour in enumerate(hours):
    row = num_rows - 1 - row_idx  # Start from top
    data_points = hourly_data[hour]

    # Draw each data point in this hour
    for col_idx, (ts, status) in enumerate(data_points):
        if col_idx >= 4:  # Max 4 columns
            break

        # Draw rectangle
        rect = patches.Rectangle((col_idx, row), 1, 1,
                                 linewidth=2,
                                 edgecolor='white',
                                 facecolor=color_map[status])
        ax.add_patch(rect)

        # Add time label inside the box
        time_text = ts.strftime('%H:%M')
        ax.text(col_idx + 0.5, row + 0.5, time_text,
                ha='center', va='center',
                fontsize=11, weight='bold', color='white')

# Add legend at the bottom
legend_y = -0.5
legend_items = [
    ('ONLINE', '#10B981'),
    ('ERROR', '#F59E0B'),
    ('OFFLINE', '#EF4444')
]

for idx, (label, color) in enumerate(legend_items):
    x_pos = 0.5 + idx * 1.2
    rect = patches.Rectangle((x_pos, legend_y), 0.3, 0.3,
                             facecolor=color, edgecolor='white', linewidth=2)
    ax.add_patch(rect)
    ax.text(x_pos + 0.45, legend_y + 0.15, label,
            ha='left', va='center', fontsize=10, weight='bold')

plt.tight_layout()
plt.savefig("status_timeline.png", dpi=300, bbox_inches='tight')
