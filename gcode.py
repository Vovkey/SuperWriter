def strokes_to_gcode(strokes, cfg):
    pr, pen, d = cfg["printer"], cfg["pen"], cfg["drawing"]
    z_up, z_down = pen["z_up"], pen["z_down"]
    ox, oy = d["origin_x"], d["origin_y"]
    bed_x, bed_y = pr["bed_x"], pr["bed_y"]

    lines = [
        "G21 ; units are mm",
        "G90 ; absolute positioning"
    ]
    if pr["home_before_print"]:
        lines.append("G28 ; home all axes")
    lines += pr["extra_start_gcode"]
    lines.append(f"g0 Z{z_up:.2f} F{pen['feed_z']} ; pen up")


    for stroke in strokes:
        if len(stroke) < 2:
            continue

        pts = [(ox + x, oy + y) for x, y in stroke]

        for x, y in pts:
            if not(0 <= x <= bed_x and 0 <= y <= bed_y):
                raise ValueError(f"Point ({x:.1f}, {y:.1f}) is outside the bed")

        x0, y0 = pts[0]
        lines.append(f"G0 X{x0:.2f} Y{y0:.2f} F{pen['feed_travel']} ; travel to stroke start")
        lines.append(f"G0 Z{z_down:.2f} F{pen['feed_z']} ; pen down")
        for x, y in pts[1:]:
            lines.append(f"G1 X{x:.2f} Y{y:.2f} F{pen['feed_draw']}")
        lines.append(f"G0 Z{z_up:.2f} F{pen['feed_z']} ; pen up")

    lines.append(f"G0 X{pr['park_x']} Y{pr['park_y']} F{pen['feed_travel']} ; park the head")
    lines += pr["extra_end_gcode"]
    return "\n".join(lines) + "\n"
