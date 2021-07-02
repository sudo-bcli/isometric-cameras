import bpy
from mathutils import Vector
from math import radians

bl_info = {
    "name": "Isometric Cameras",
    "author": "Benjamin Lee",
    "version": (1, 0),
    "blender": (2, 93, 1),
    "location": "View3D > Add > Camera > Isometric Cameras",
    "description": "Adds Isometric Cameras to the Scene",
    "warning": "",
    "doc_url": "https://github.com/sudo-bcli/isometric-cameras",
    "category": "Camera",
}

def deg2rad(vec):
    """ convert degree vector to radians vector

    Args:
        vec (mathutils.Vector): rotation vector
    """
    vec.x = radians(vec.x)
    vec.y = radians(vec.y)
    vec.z = radians(vec.z)

def add_isometric_camera(self, context, name, loc, rot, ortho_scale, ratio = 0, lock_rot = True, active = True):
    """ add different types isometric camera based on provided arguments

    Args:
        context (bpy.context): scene context
        name (string): camera name
        loc (mathutils.Vector): initial location
        rot (mathutils.Vector): initial rotation
        ortho_scale (float): Orthographic scale
        ratio (float): adjust camera size ratio. Default to 0 (no adjust)
        lock_rot (bool, optional): Lock camera rotation. Default to True
        active (bool, optional): As active camera. Default to True
    """
    bpy.ops.object.camera_add() # once added, camera become active object
    cam = context.active_object
    cam.name = name # rename camera
    cam.data.type = 'ORTHO' # set camera type to orthographic
    cam.data.ortho_scale = ortho_scale # set orthographic scale
    cam.location = loc # set camera location
    deg2rad(rot); cam.rotation_euler = rot# set camera rotation
    if ratio != 0:
        bpy.context.scene.render.resolution_y = round(bpy.context.scene.render.resolution_x * (1/ratio)) # adjust camera size
    if lock_rot:
        cam.lock_rotation = (True,True,True)
    if active:
        bpy.ops.view3d.object_as_camera()


class AddIsometric(bpy.types.Operator):
    """ Add isometric camera for technical drawings"""
    bl_idname = "object.add_isometric_camera"
    bl_label = "Add Isometric Camera"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        name = "Isometric Camera"
        loc = Vector((30,-30,30))
        rot = Vector((54.736,0,45))
        ortho_scale = 14.123
        add_isometric_camera(self, context,name, loc, rot, ortho_scale)
        return {'FINISHED'}

class AddGameIsometric21(bpy.types.Operator):
    """ Add isometric camera for tiled games (tile ratio 2:1)"""
    bl_idname = "object.add_game_isometric_camera_21"
    bl_label = "Add Game Isometric Camera (2:1)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        name = "Game Isometric Camera (2:1)"
        loc = Vector((30.60861, -30.60861, 25.00000))
        rot = Vector((60,0,45))
        ortho_scale = 14.123
        ratio = 2
        add_isometric_camera(self, context,name, loc, rot, ortho_scale, ratio)
        return {'FINISHED'}

class AddGameIsometric43(bpy.types.Operator):
    """ Add isometric camera for tiled games (tile ratio 4:3)"""
    bl_idname = "object.add_game_isometric_camera_43"
    bl_label = "Add Game Isometric Camera (4:3)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        name = "Game Isometric Camera (4:3)"
        loc = Vector((23.42714, -23.42714, 37.4478))
        rot = Vector((41.5,0,45))
        ortho_scale = 14.123
        ratio = 4/3
        add_isometric_camera(self, context,name, loc, rot, ortho_scale,ratio)
        return {'FINISHED'}

class AddReferencePlane(bpy.types.Operator):
    """Add isometric reference plane"""
    bl_idname = "object.add_isometric_reference_plane"
    bl_label = "Add isometric reference plane"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0)) 
        plane = context.active_object
        plane.scale = Vector((5, 5, 0)) # scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True) # apply scale
        return {'FINISHED'}   

def btn_add_isometric(self, context):
    self.layout.operator(
        AddIsometric.bl_idname,
        text="Isometric Camera",
        icon='OUTLINER_OB_CAMERA')

def btn_add_game_isometric_21(self, context):
    self.layout.operator(
        AddGameIsometric21.bl_idname,
        text="Isometric Game Camera (2:1) ",
        icon='OUTLINER_OB_CAMERA')

def btn_add_game_isometric_43(self, context):
    self.layout.operator(
        AddGameIsometric43.bl_idname,
        text="Isometric Game Camera (4:3)",
        icon='OUTLINER_OB_CAMERA')

def btn_add_reference_plane(self, context):
    self.layout.operator(
        AddReferencePlane.bl_idname,
        text="Isometric Reference Plane",
        icon='OUTLINER_OB_CAMERA')
  
def register():
    bpy.utils.register_class(AddIsometric)
    bpy.utils.register_class(AddGameIsometric21)
    bpy.utils.register_class(AddGameIsometric43)
    bpy.utils.register_class(AddReferencePlane)
    bpy.types.VIEW3D_MT_camera_add.append(btn_add_isometric)
    bpy.types.VIEW3D_MT_camera_add.append(btn_add_game_isometric_21)
    bpy.types.VIEW3D_MT_camera_add.append(btn_add_game_isometric_43)
    bpy.types.VIEW3D_MT_camera_add.append(btn_add_reference_plane)

def unregister():
    bpy.utils.unregister_class(AddIsometric)
    bpy.utils.unregister_class(AddGameIsometric21)
    bpy.utils.unregister_class(AddGameIsometric43)
    bpy.utils.unregister_class(AddReferencePlane)
    bpy.types.VIEW3D_MT_camera_add.remove(btn_add_isometric)
    bpy.types.VIEW3D_MT_camera_add.remove(btn_add_game_isometric_21)
    bpy.types.VIEW3D_MT_camera_add.remove(btn_add_game_isometric_43)
    bpy.types.VIEW3D_MT_camera_add.remove(btn_add_reference_plane)

if __name__ == "__main__":
    register()