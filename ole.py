import bpy, csv

bl_info = {
    'name': "Object Location Export",
    'author': "Nicolai Waniek <rochus at rochus dot net>",
    'version': (0,0,1),
    'blender': (2,5,9),
    'location': "Render > Object Location Export",
    'description': "Save the location of an object to a file",
    'wiki_url': "",
    'tracker_url': "",
    'category': "Render"}

class OBJECT_PT_ObjectLocationExport(bpy.types.Panel):
    bl_label = "Object Location Export"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"

    bpy.types.Scene.ole_use_active_object = bpy.props.BoolProperty(
        attr="ole_use_active_object",
        name="ole_use_active_object",
        default=False)

    bpy.types.Scene.ole_use_dimension_settings = bpy.props.BoolProperty(
        attr="ole_use_dimension_settings",
        name="ole_use_dimension_settings",
        default=True)

    bpy.types.Scene.ole_frame_start = bpy.props.IntProperty(
        attr="ole_frame_start",
        name="Start",
        min=1,
        max=10000,
        default=1)

    bpy.types.Scene.ole_frame_end = bpy.props.IntProperty(
        attr="ole_frame_end",
        name="End",
        min=1,
        max=10000,
        default=255)

    bpy.types.Scene.ole_frame_step = bpy.props.IntProperty(
        attr="ole_frame_step",
        name="Step",
        min=1,
        max=1000,
        default=1)

    bpy.types.Scene.ole_file_path = bpy.props.StringProperty(
        attr="ole_file_path",
        name="File Path",
        default="/tmp/objloc.cvs")

    bpy.types.Scene.ole_objects = bpy.props.EnumProperty(
        items=[(str(1), "bla", str(1))],
        attr="ole_object_list",
        name="ole_object_list",
        description="Choose the object which location shall be exported")

    # TODO: use file browser to set the file path
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, "ole_file_path", text="")

        row = layout.row()
        row.prop(scene, "ole_use_active_object", text="Use Active Object (default: Camera)")

        row = layout.row()
        row.prop(scene, "ole_use_dimension_settings", text="Use Dimension Settings")

        row = layout.row(align=True)
        row.prop(scene, "ole_frame_start")
        row.prop(scene, "ole_frame_step")
        row.prop(scene, "ole_frame_end")
        row.active = not scene.ole_use_dimension_settings

        row = layout.row()
        split = row.split(percentage=0.5)
        colL = split.column()
        colR = split.column()
        colL.operator("ole.save_object_location", text="Save")
        pass


class OBJECT_OT_ObjectLocationExport(bpy.types.Operator):
    bl_label = "Object Location Export"
    bl_idname = "ole.save_object_location"
    bl_description = "Export the location of an object to a file"

    def invoke(self, context, event):
        scene = context.scene
        frame_reset = scene.frame_current

        # active object:
        if scene.ole_use_active_object:
            obj = context.active_object
        else:
            obj = scene.camera

        if obj == None:
            return {"FINISHED"}

        # frame settings
        if scene.ole_use_dimension_settings:
            frame_start = scene.frame_start
            frame_end = scene.frame_end
            frame_step = scene.frame_step
        else:
            frame_start = scene.ole_frame_start
            frame_end = scene.ole_frame_end
            frame_step = scene.ole_frame_step

        f = open(scene.ole_file_path, "w")
        writer = csv.writer(f)
        scene.frame_set(frame_start)

        while scene.frame_current <= frame_end:
            loc = obj.matrix_world.to_translation()
            rot = obj.matrix_world.to_euler()
            writer.writerow([scene.frame_current, loc[0], loc[1], loc[2], rot[0], rot[1], rot[2]])
            scene.frame_set(scene.frame_current + frame_step)

        f.close()
        scene.frame_set(frame_reset)
        return {"FINISHED"}

def register():
    bpy.utils.register_class(OBJECT_PT_ObjectLocationExport)
    bpy.utils.register_class(OBJECT_OT_ObjectLocationExport)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_ObjectLocationExport)
    bpy.utils.unregister_class(OBJECT_OT_ObjectLocationExport)

if __name__ == "__main__":
    register()
