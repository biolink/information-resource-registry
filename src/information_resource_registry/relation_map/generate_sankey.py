import sys
import pandas as pd
import plotly.graph_objects as go

# Step 1: Read the command line argument for the path to the CSV file
if len(sys.argv) < 2:
    print("Usage: python script_name.py path_to_your_file.csv")
    sys.exit(1)  # Exit the script if no argument is provided

csv_file_path = sys.argv[1]

# Step 2: Read data from the CSV file
data = pd.read_csv(csv_file_path)

# Step 3: Create the nodes and links for the Sankey diagram
all_nodes = pd.concat([data['ID'], data['Consumed By']]).unique()
node_dict = {node: i for i, node in enumerate(all_nodes)}

source_indices = [node_dict[src] for src in data['ID']]
target_indices = [node_dict[tgt] for tgt in data['Consumed By']]

# Step 4: Create the figure
fig = go.Figure(data=[go.Sankey(
    node=dict(
      pad=15,
      thickness=20,
      line=dict(color="black", width=0.5),
      label=all_nodes,
      color="blue"
    ),
    link=dict(
      source=source_indices,
      target=target_indices,
      value=data['Value']
    ))])

fig.update_layout(title_text="Sankey Diagram", font_size=10,
                  width=1200, height=5000)

# Display the plot
fig.show()

# Step 5: Save the plot to a PNG file
fig.write_image('data/sankey_diagram.png', scale=2)
