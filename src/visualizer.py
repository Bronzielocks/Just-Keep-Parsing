import os

from matplotlib import lines  as mlines
from matplotlib import pyplot as plt

from src.reader import FormCSV

def display_cumulative(form_dict: dict[str, FormCSV], out_filename: str) -> None:
    # Display the data collectively so we can see compare them
    # Ignore the fact that the resting period is sometimes wrong,
    # let's just use the cumulative time for now
    plt.figure(figsize=(12, 6))

    marker_map = {'FR': 'o', 'BK': '^', 'BR': 's'}

    # Get a color cycle from matplotlib
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    # Helper function to extract date from filename
    def extract_date_from_filename(filename):
        return os.path.basename(filename).split('_')[1]

    # Map filenames to colors. If more files than default colors, colors will repeat.
    filename_to_color = {filename: colors[i % len(colors)] for i, filename in enumerate(form_dict.keys())}

    # Prepare handles and labels for the file color legend
    file_legend_handles = []
    file_legend_labels = []

    for filename, form_csv in form_dict.items():
        # Only consider up to a certain distance threshold
        # df = form_csv.swim_df[form_csv.swim_df["Cumul Dist (yd)"] <= dist_max]
        df = form_csv.swim_df
        # Filter out all the rests
        df = df[df["Strk"] != "REST"]

        current_color = filename_to_color[filename]
        # Changed linestyle to '-' to make the color visible in the legend
        file_legend_handles.append(mlines.Line2D([], [], color=current_color, marker='None', linestyle='-'))
        file_legend_labels.append(extract_date_from_filename(filename))

        # Plot each stroke type with a different marker
        for stroke_type, marker_shape in marker_map.items():
            stroke_df = df[df["Strk"] == stroke_type]
            if not stroke_df.empty:
                # Convert 'Cumul Time (s)' to minutes for plotting
                plt.scatter(stroke_df["Cumul Time (s)"] / 60, stroke_df["Cumul Dist (yd)"],
                            label=f"{extract_date_from_filename(filename)} - {stroke_type}", # Use date in label
                            marker=marker_shape,
                            color=current_color) # Assign the color for the current file

    plt.xlabel("Cumulative Time (minutes)") # Update x-axis label
    plt.ylabel("Cumulative Distance (yards)")
    plt.title("Progression of Distance Swimming Over Time by Stroke Type")
    plt.grid(True)

    # Create a legend for marker shapes (stroke types)
    # Create dummy handles for the stroke type legend
    stroke_legend_handles = [mlines.Line2D([], [], color='black', marker=marker_map[s_type], linestyle='None', markersize=8)
                            for s_type in marker_map.keys()]
    stroke_legend_labels = ['Freestyle' if s_type == 'FR' else 'Backstroke' if s_type == 'BK' else 'Breaststroke' for s_type in marker_map.keys()]
    stroke_legend = plt.legend(stroke_legend_handles, stroke_legend_labels,
                            title="Swim Stroke", bbox_to_anchor=(0.02, 0.98), loc='upper left') # Moved to top left

    # Create a second legend for file colors
    file_legend = plt.legend(file_legend_handles, file_legend_labels,
                            title="Swim Session", bbox_to_anchor=(0.98, 0.02), loc='lower right') # Moved inside plot

    # Add the first legend back to the figure
    plt.gca().add_artist(stroke_legend)

    plt.tight_layout() # Adjust layout to prevent labels from being cut off
    plt.savefig(out_filename)
