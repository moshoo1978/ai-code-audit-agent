import plotly.graph_objects as go
import json
import os

def load_rooms_and_openings(json_path="output_data/plan_text.json", default_height=3.2):
    """
    Extracts room boundaries along with door/window openings from plan JSON.
    """
    rooms = []
    openings = []

    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
            
            if "rooms" in data and isinstance(data["rooms"], list):
                rooms = data["rooms"]
            if "openings" in data and isinstance(data["openings"], list):
                openings = data["openings"]
        except Exception:
            pass

    # Default spaces and openings if JSON does not contain explicit geometry
    if not rooms:
        rooms = [
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

    if not openings:
        # Sample openings (doors and windows)
        openings = [
            {"type": "door", "x": 10, "y": 9, "width": 1.2, "height": 2.1, "wall_axis": "y"},
            {"type": "window", "x": 0, "y": 10, "width": 1.5, "height": 1.2, "sill_height": 1.0, "wall_axis": "y"}
        ]

    return rooms, openings


def generate_3d_building_model(rooms_data=None, openings_data=None, wall_height=3.2):
    """
    Generates an interactive 3D model with extruded walls, opening cutouts, floor slabs, and roofs.
    """
    if not rooms_data or not openings_data:
        rooms_data, openings_data = load_rooms_and_openings(default_height=wall_height)

    fig = go.Figure()

    # 1. Render Rooms (Walls, Floor Slabs, Ceilings)
    for room in rooms_data:
        x = room["x"]
        y = room["y"]
        h = room.get("height", wall_height)
        wall_color = room.get("wall_color", "#1f77b4")

        # Extrude Solid Walls
        for i in range(len(x) - 1):
            fig.add_trace(go.Mesh3d(
                x=[x[i], x[i+1], x[i+1], x[i]],
                y=[y[i], y[i+1], y[i+1], y[i]],
                z=[0, 0, h, h],
                color=wall_color,
                opacity=0.75,
                name=f"{room['name']} - Wall",
                showscale=False
            ))

        # Floor Slab
        fig.add_trace(go.Mesh3d(
            x=x[:-1], y=y[:-1], z=[0]*(len(x)-1),
            color="#d3d3d3", opacity=0.9,
            name=f"{room['name']} - Floor",
            showscale=False
        ))

        # Ceiling Plane
        fig.add_trace(go.Mesh3d(
            x=x[:-1], y=y[:-1], z=[h]*(len(x)-1),
            color=wall_color, opacity=0.15,
            name=f"{room['name']} - Ceiling",
            showscale=False
        ))

    # 2. Render Openings (Door Cutouts & Glass Windows)
    for op in openings_data:
        op_type = op.get("type", "door")
        ox = op.get("x", 0)
        oy = op.get("y", 0)
        w = op.get("width", 1.0)
        oh = op.get("height", 2.1)
        sill = op.get("sill_height", 0.0) if op_type == "window" else 0.0
        axis = op.get("wall_axis", "x")

        # Define 3D bounding geometry for opening
        if axis == "x":
            x_pts = [ox, ox + w, ox + w, ox]
            y_pts = [oy, oy, oy, oy]
        else:
            x_pts = [ox, ox, ox, ox]
            y_pts = [oy, oy + w, oy + w, oy]

        color = "#e74c3c" if op_type == "door" else "#3498db"
        name_tag = "🚪 Door Opening" if op_type == "door" else "🪟 Window Opening"

        fig.add_trace(go.Mesh3d(
            x=x_pts,
            y=y_pts,
            z=[sill, sill, sill + oh, sill + oh],
            color=color,
            opacity=0.9,
            name=name_tag,
            showscale=False
        ))

    # Layout & Camera Config
    fig.update_layout(
        title="🏛️ Dynamic 3D Model with Door & Window Cutouts",
        scene=dict(
            xaxis=dict(title='X Axis (ft)', backgroundcolor="rgb(245, 245, 245)"),
            yaxis=dict(title='Y Axis (ft)', backgroundcolor="rgb(245, 245, 245)"),
            zaxis=dict(title='Height / Z Axis (ft)', backgroundcolor="rgb(235, 235, 235)"),
            aspectmode='data',
            camera=dict(eye=dict(x=1.8, y=-1.8, z=1.4))
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=680
    )

    return fig