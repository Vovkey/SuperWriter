def strokes_to_gcode(strokes, origin=(20.0, 20.0), z_up=5.0, z_down=0.0,
    feed_draw=1200, feed_travel=6000, feed_z=600,
    bed=(220, 220)):

    ox, oy = origin

    lines = [
        "G21 ; units are mm",
        "G90 ; absolute positioning",
        "G28 ; home all axes",
        f"G0 Z{z_up:.2f} F{feed_z} ; pen up",
    ]

    for stroke in strokes:
        if len(stroke) < 2:
            continue

        pts = [(ox + x, oy + y) for x, y in stroke]

        for x, y in pts:
            if not(0 <= x <= bed[0] and 0 <= y <= bed[1]):
                raise ValueError(f"Point ({x:.1f}, {y:.1f}) is outside the bed {bed}")

        x0, y0 = pts[0]
        lines.append(f"G0 X{x0:.2f} Y{y0:.2f} F{feed_travel} ; travel to stroke start")
        lines.append(f"G0 Z{z_down:.2f} F{feed_z} ; pen down")
        for x, y in pts[1:]:
            lines.append(f"G1 X{x:.2f} Y{y:.2f} F{feed_draw}")
        lines.append(f"G0 Z{z_up:.2f} F{feed_z} ; pen up")

    lines.append(f"G0 X0 Y{bed[1]} F{feed_travel} ; park the head")
    return "\n".join(lines) + "\n"
