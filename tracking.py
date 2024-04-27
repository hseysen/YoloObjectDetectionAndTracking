import geometry


class IDGenerator:
    def __init__(self):
        self.next_id = -1
    
    def get_id(self):
        self.next_id += 1
        return self.next_id


idgen = IDGenerator()
line1 = geometry.Line(372, 500, 1324, 500)
line2 = geometry.Line(1324, 500, 1801, 1080)


class Object:
    def __init__(self, x, y):
        self.point = geometry.Point(x, y)
        self.id = idgen.get_id()
        self.remaining_frames = 30
        self.fell = False
    
    def __eq__(self, other):
        if not isinstance(other, Object):
            return False
        return self.id == other.id
    
    def __str__(self):
        return f"Object {self.id} ({self.remaining_frames}/30)"
    
    def get_distance(self, target_x, target_y):
        return ((target_x - self.point.pt[0])**2 + (target_y - self.point.pt[1])**2)**0.5
    
    def can_remove(self):
        self.remaining_frames -= 1
        return self.remaining_frames == 0
    
    def update(self, new_x, new_y):
        newpt = geometry.Point(new_x, new_y)

        if not self.fell:
            object_start_side_line1 = geometry.point_side(line1, self.point)
            object_end_side_line1 = geometry.point_side(line1, newpt)
            crosses_line1 = (object_start_side_line1 != object_end_side_line1) and (line1.start[0] < self.point.pt[0] < line1.end[0])

            object_start_side_line2 = geometry.point_side(line2, self.point)
            object_end_side_line2 = geometry.point_side(line2, newpt)
            crosses_line2 = (object_start_side_line2 != object_end_side_line2) and (line2.start[0] < self.point.pt[0] < line2.end[0])

            if crosses_line1 or crosses_line2:
                self.fell = True

        self.point = newpt
        self.remaining_frames = 30

