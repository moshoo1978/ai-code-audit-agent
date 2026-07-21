import plotly.graph_objects as go

def generate_3d_building_model(rooms_data=None):
    """
    Generates an interactive 3D model of walls, floor slabs, and ceiling planes.
    """
    if not rooms_data:
        rooms_data = [
            {
                "name": "OFFICE-101",
                "x": [0, 10, 10, 0, 0],
                "y": [0, 0, 8, 8, 0],
                "height": 3.2,
                "wall_color": "#1f77b4",
                "floor_color": "#aec7e8"
            },
            {
                "name": "Egress Corridor",
                "x": [10, 15, 15, 10, 10],
                "y": [0, 0, 8, 8, 0],
                "height": 3.2,
                "wall_color": "#ff7f0e",
                "floor_color": "#ffbb78"
            }
        ]

    fig = go.Figure()

    for room in rooms_data:
        x = room["x"]
        y = room["y"]
        h = room["height"]
        wall_color = room.get("wall_color", "#3366cc")
        floor_color = room.get("floor_color", "#cccccc")

        # 1. Vertical Wall Extrusion
        for i in range(len(x) - 1):
            fig.add_trace(go.Mesh3d(
                x=[x[i], x[i+1], x[i+1], x[i]],
                y=[y[i], y[i+1], y[i+1], y[i]],
                z=[0, 0, h, h],
                color=wall_color,
                opacity=0.85,
                name=f"{room['name']} - Wall",
                showscale=False
            ))

        # 2. Floor Slab
        fig.add_trace(go.Mesh3d(
            x=x[:-1], y=y[:-1], z=[0]*(len(x)-1),
            color=floor_color, opacity=0.9,
            name=f"{room['name']} - Floor",
            showscale=False
        ))

        # 3. Transparent Ceiling Plane
        fig.add_trace(go.Mesh3d(
            x=x[:-1], y=y[:-1], z=[h]*(len(x)-1),
            color=wall_color, opacity=0.2,
            name=f"{room['name']} - Ceiling",
            showscale=False
        ))

    fig.update_layout(
        title="🏛️ Interactive 3D Building Extrusion",
        scene=dict(
            xaxis=dict(title='X (Feet/Meters)', backgroundcolor="rgb(240, 240, 240)"),
            yaxis=dict(title='Y (Feet/Meters)', backgroundcolor="rgb(240, 240, 240)"),
            zaxis=dict(title='Height / Z-Axis', backgroundcolor="rgb(230, 230, 230)"),
            aspectmode='data',
            camera=dict(
                eye=dict(x=1.6, y=-1.6, z=1.2)
            )
        ),
        margin=dict(l=0, r=0, b=0, t=50),
        height=650
    )

    return fig