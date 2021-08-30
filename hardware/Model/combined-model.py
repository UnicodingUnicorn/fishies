import cadquery as cq
import math

food_disc_radius = 35 / 2
food_hole_radius = 5 / 2

layer_height = 2
additional_thickness = 2
tolerance = 0.6
elephants_compensation = 0.4

m4hole = 4 + tolerance

length = food_disc_radius * 2 + additional_thickness * 2
screw_length = length - m4hole - additional_thickness

servo_horn_tooth_count = 21
servo_horn_radius = 4.6 / 2
servo_horn_height = 3.2

food_hole_offset = food_disc_radius - food_hole_radius - additional_thickness / 2
bigger_food_hole_radius = food_hole_radius + additional_thickness / 2

servo_centre_offset = 5.5
servo_length = 22.6
servo_tab_length = 32.2
servo_width = 12.2
servo_height = 8.3

hopper_hole_offset = math.radians(30)
hopper_radius = math.sqrt((food_hole_offset - (servo_tab_length / 2 - servo_centre_offset)) ** 2 + ((servo_width + additional_thickness) / 2) ** 2) - additional_thickness / 2
hopper_outer_radius = hopper_radius + additional_thickness / 2
hopper_height = 30

food_disc = cq.Workplane("XY")\
    .circle(food_disc_radius)\
    .moveTo(food_hole_offset * math.cos(hopper_hole_offset), food_hole_offset * math.sin(hopper_hole_offset))\
    .circle(food_hole_radius)\
    .extrude(layer_height)\
    .faces(">Z")\
    .workplane()\
    .circle(servo_horn_radius + additional_thickness / 2)\
    .extrude(servo_horn_height - layer_height)\
    .faces(">Z").workplane()
    
for i in range(servo_horn_tooth_count):
    base_angle = i * math.radians(360 / servo_horn_tooth_count)
    angle = math.radians(360 / servo_horn_tooth_count) / 2
    x = (servo_horn_radius * math.sin(angle)) / math.sin(math.radians(180 - 45) - angle)
    y = x / math.sqrt(2)
    radius = servo_horn_radius - y
    
    x1 = radius * math.cos(base_angle)
    y1 = radius * math.sin(base_angle)
    x2 = servo_horn_radius * math.cos(base_angle + angle)
    y2 = servo_horn_radius * math.sin(base_angle + angle)
    x3 = radius * math.cos(base_angle + angle * 2)
    y3 = radius * math.sin(base_angle + angle * 2)
    
    food_disc = food_disc.moveTo(x1, y1)\
        .lineTo(x2, y2)\
        .lineTo(x3, y3)
    
food_disc = food_disc.close()\
    .cutThruAll()
'''
    .faces("<Z")\
    .chamfer(elephants_compensation)
'''
    
food_disc_carrier = cq.Workplane("XY")\
    .rect(length, length)\
    .moveTo(food_hole_offset, 0)\
    .circle(hopper_outer_radius)\
    .extrude(layer_height)\
    .faces(">Z").workplane()\
    .rect(screw_length, screw_length, forConstruction=True)\
    .vertices()\
    .hole(m4hole)\
    .pushPoints([(0, 0)])\
    .hole(food_disc_radius * 2 + tolerance)\
    .edges("|Z")\
    .fillet((m4hole + additional_thickness) / 2)
'''
    .faces("<Z")\
    .chamfer(elephants_compensation)
'''

bottom_plate = cq.Workplane("XY")\
    .rect(length, length)\
    .moveTo(food_hole_offset, 0)\
    .circle(hopper_outer_radius)\
    .extrude(-layer_height)\
    .faces(">Z").workplane()\
    .rect(screw_length, screw_length, forConstruction=True)\
    .vertices()\
    .hole(m4hole)\
    .pushPoints([(0, 0)])\
    .hole(servo_horn_radius * 2)\
    .pushPoints([(food_hole_offset * math.cos(hopper_hole_offset), food_hole_offset * math.sin(hopper_hole_offset))])\
    .hole(bigger_food_hole_radius * 2)\
    .edges("|Z")\
    .fillet((m4hole + additional_thickness) / 2)
'''
    .faces("<Z")\
    .chamfer(elephants_compensation)
'''

base_top_plate_height = servo_horn_height - layer_height
top_plate = cq.Workplane("XY", (0, 0, layer_height))\
    .rect(length, length)\
    .extrude(base_top_plate_height)\
    .faces(">Z")\
    .rect(screw_length, screw_length, forConstruction=True)\
    .vertices()\
    .hole(m4hole)\
    .pushPoints([(0, 0)])\
    .hole(servo_horn_radius * 2)\
    .pushPoints([(food_hole_offset, 0)])\
    .hole(bigger_food_hole_radius * 2)\
    .edges("|Z")\
    .fillet((m4hole + additional_thickness) / 2)\
    .faces(">Z")\
    .moveTo(food_hole_offset, 0)\
    .circle(hopper_radius)\
    .circle(hopper_outer_radius)\
    .extrude(hopper_height)\
    .faces(">Z")\
    .moveTo(-servo_centre_offset, 0)\
    .rect(servo_tab_length, servo_width + additional_thickness)\
    .cutBlind(hopper_height)\
    .faces(">>Z[-2]")\
    .moveTo(-servo_centre_offset, 0)\
    .rect(servo_tab_length, servo_width + additional_thickness)\
    .rect(servo_length + tolerance, servo_width + tolerance)\
    .extrude(servo_height + base_top_plate_height)\
    .faces(">>Z[-2]")\
    .moveTo(servo_tab_length / 2 - servo_centre_offset + additional_thickness / 2 / 2, 0)\
    .rect(additional_thickness / 2, servo_width + additional_thickness)\
    .extrude(hopper_height)
'''
    .faces("<Z")\
    .chamfer(elephants_compensation)
'''
    
cq.exporters.export(food_disc, 'food_disc.stl')
cq.exporters.export(food_disc_carrier, 'food_disc_carrier.stl')
cq.exporters.export(bottom_plate, 'bottom_plate.stl')
cq.exporters.export(top_plate, 'top_plate.stl')