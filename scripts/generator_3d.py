import plotly.graph_objects as go
import json
import os

def load_rooms_from_json(json_path="output_data/plan_text.json", default_height=3.2):
    """
    Extracts room boundaries and dimensions from the parsed plan JSON.
    Falls back to default spaces if coordinates are not yet extracted.
    """
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
            
            # Extract rooms if structured room data exists
            if "rooms" in data and isinstance(data["rooms"], list) and len(data["rooms"]) > 0:
                parsed_rooms = []
                for room in data["rooms"]:
                    parsed_rooms.append({
                        "name": room.get("name", "Unknown Space"),
                        "x": room.get("x", [0, 5, 5, 0, 0]),
                        "y": room.get("y", [0, 0, 5, 5, 0]),
                        "height": room.get("height", default_height),
                        "wall_color": room.get("color", "#1f77b4")
                    })
                return parsed_rooms
        except Exception:
            pass

    # Default fallback spaces matching sheet layout
    return [
        {
            "name": "OFFICE 101",
            "x": [0, 10, 10, 0, 0],
            "y": [5, 5, 15, 15, 5],
            "height": default_height,
            "wall_color": "#1f77b4"
        },
        {
            "name": "Corridor / Egress",
            "x": [10, 20, 20, 10, 10],
            "y": [5, 5, 15, 15, 5],
            "height": default_height,
            "wall_color": "#2ca02c"
        }
    ]


def generate_3d_building_model(rooms_data=None, wall_height=3.2):
    """
    Generates an interactive 3D model with extruded walls, floor slabs, and hover labels.
    """
    if not rooms_data:
        rooms_data = load_rooms_from_json(default_height=wall_height)

    fig = go.Figure()

    for room in rooms_data:
        x = room["x"]
        y = room["y"]
        h = room.get("height", wall_height)
        wall_color = room.get("wall_color", "#1f77b4")

        # 1. Extrude Walls
        for i in range(len(x) - 1):
            fig.add_trace(go.Mesh3d(
                x=[x[i], x[i+1], x[i+1], x[i]],
                y=[y[i], y[i+1], y[i+1], y[i]],
                z=[0, 0, h, h],
                color=wall_color,
                opacity=0.8,
                name=f"{room['name']} - Wall",
                hoverinfo="name",
                showscale=False
            ))

        # 2. Floor Slab
        fig.add_trace(go.Mesh3d(
            x=x[:-1], y=y[:-1], z=[0]*(len(x)-1),
            color="#d3d3d3", opacity=0.9,
            name=f"{room['name']} - Floor",
            hoverinfo="name",
            showscale=False
        ))

        # 3. Transparent Ceiling / Roof Slab
        fig.add_trace(go.Mesh3d(
            x=x[:-1], y=y[:-1], z=[h]*(len(x)-1),
            color=wall_color, opacity=0.15,
            name=f"{room['name']} - Ceiling",
            hoverinfo="name",
            showscale=False
        ))

    # Scene Layout & Camera Angle Settings
    fig.update_layout(
        title="🏛️ Dynamic 3D Architectural Model",
        scene=dict(
            xaxis=dict(title='X Axis (ft)', backgroundcolor="rgb(245, 245, 245)"),
            yaxis=dict(title='Y Axis (ft)', backgroundcolor="rgb(245, 245, 245)"),
            zaxis=dict(title='Height / Z Axis (ft)', backgroundcolor="rgb(235, 235, 235)"),
            aspectmode='data',
            camera=dict(
                eye=dict(x=1.8, y=-1.8, z=1.4)
            )
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=680
    )

    return fig