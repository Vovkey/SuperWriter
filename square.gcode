G21 ; units are mm
G90 ; absolute positioning
G28 ; home all axes
G0 Z5.00 F600 ; pen up
G0 X20.00 Y20.00 F6000 ; travel to stroke start
G0 Z0.00 F600 ; pen down
G1 X61.00 Y20.00 F1200
G1 X60.00 Y60.00 F1200
G1 X20.00 Y60.00 F1200
G1 X20.00 Y20.00 F1200
G0 Z5.00 F600 ; pen up
G0 X0 Y220 F6000 ; park the head
