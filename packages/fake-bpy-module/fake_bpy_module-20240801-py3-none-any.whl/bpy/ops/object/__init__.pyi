import typing
import collections.abc
import typing_extensions
import bpy.ops.transform
import bpy.types
import mathutils

GenericType1 = typing.TypeVar("GenericType1")
GenericType2 = typing.TypeVar("GenericType2")

def add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    radius: float | None = 1.0,
    type: str | None = "EMPTY",
    enter_editmode: bool | None = False,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add an object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param radius: Radius
        :type radius: float | None
        :param type: Type
        :type type: str | None
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def add_modifier_menu(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def add_named(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    linked: bool | None = False,
    name: str = "",
    session_uid: int | None = 0,
    matrix: collections.abc.Sequence[collections.abc.Sequence[float]]
    | mathutils.Matrix
    | None = (
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
    ),
    drop_x: int | None = 0,
    drop_y: int | None = 0,
):
    """Add named object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param linked: Linked, Duplicate object but not object data, linking to the original data
    :type linked: bool | None
    :param name: Name, Name of the data-block to use by the operator
    :type name: str
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: int | None
    :param matrix: Matrix
    :type matrix: collections.abc.Sequence[collections.abc.Sequence[float]] | mathutils.Matrix | None
    :param drop_x: Drop X, X-coordinate (screen space) to place the new object under
    :type drop_x: int | None
    :param drop_y: Drop Y, Y-coordinate (screen space) to place the new object under
    :type drop_y: int | None
    """

    ...

def align(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    bb_quality: bool | None = True,
    align_mode: str | None = "OPT_2",
    relative_to: str | None = "OPT_4",
    align_axis: set[str] | None = {},
):
    """Align objects

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param bb_quality: High Quality, Enables high quality but slow calculation of the bounding box for perfect results on complex shape meshes with rotation/scale
        :type bb_quality: bool | None
        :param align_mode: Align Mode, Side of object to use for alignment
        :type align_mode: str | None
        :param relative_to: Relative To, Reference location to align to

    OPT_1
    Scene Origin -- Use the scene origin as the position for the selected objects to align to.

    OPT_2
    3D Cursor -- Use the 3D cursor as the position for the selected objects to align to.

    OPT_3
    Selection -- Use the selected objects as the position for the selected objects to align to.

    OPT_4
    Active -- Use the active object as the position for the selected objects to align to.
        :type relative_to: str | None
        :param align_axis: Align, Align to axis
        :type align_axis: set[str] | None
    """

    ...

def anim_transforms_to_deltas(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Convert object animation for normal transforms to delta transforms

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def armature_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add an armature object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param radius: Radius
        :type radius: float | None
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def assign_property_defaults(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    process_data: bool | None = True,
    process_bones: bool | None = True,
):
    """Assign the current values of custom properties as their defaults, for use as part of the rest pose state in NLA track mixing

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param process_data: Process data properties
    :type process_data: bool | None
    :param process_bones: Process bone properties
    :type process_bones: bool | None
    """

    ...

def bake(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "COMBINED",
    pass_filter: set[str] | None = {},
    filepath: str = "",
    width: int | None = 512,
    height: int | None = 512,
    margin: int | None = 16,
    margin_type: str | None = "EXTEND",
    use_selected_to_active: bool | None = False,
    max_ray_distance: float | None = 0.0,
    cage_extrusion: float | None = 0.0,
    cage_object: str = "",
    normal_space: str | None = "TANGENT",
    normal_r: str | None = "POS_X",
    normal_g: str | None = "POS_Y",
    normal_b: str | None = "POS_Z",
    target: str | None = "IMAGE_TEXTURES",
    save_mode: str | None = "INTERNAL",
    use_clear: bool | None = False,
    use_cage: bool | None = False,
    use_split_materials: bool | None = False,
    use_automatic_name: bool | None = False,
    uv_layer: str = "",
):
    """Bake image textures of selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Type of pass to bake, some of them may not be supported by the current render engine
    :type type: str | None
    :param pass_filter: Pass Filter, Filter to combined, diffuse, glossy, transmission and subsurface passes
    :type pass_filter: set[str] | None
    :param filepath: File Path, Image filepath to use when saving externally
    :type filepath: str
    :param width: Width, Horizontal dimension of the baking map (external only)
    :type width: int | None
    :param height: Height, Vertical dimension of the baking map (external only)
    :type height: int | None
    :param margin: Margin, Extends the baked result as a post process filter
    :type margin: int | None
    :param margin_type: Margin Type, Which algorithm to use to generate the margin
    :type margin_type: str | None
    :param use_selected_to_active: Selected to Active, Bake shading on the surface of selected objects to the active object
    :type use_selected_to_active: bool | None
    :param max_ray_distance: Max Ray Distance, The maximum ray distance for matching points between the active and selected objects. If zero, there is no limit
    :type max_ray_distance: float | None
    :param cage_extrusion: Cage Extrusion, Inflate the active object by the specified distance for baking. This helps matching to points nearer to the outside of the selected object meshes
    :type cage_extrusion: float | None
    :param cage_object: Cage Object, Object to use as cage, instead of calculating the cage from the active object with cage extrusion
    :type cage_object: str
    :param normal_space: Normal Space, Choose normal space for baking
    :type normal_space: str | None
    :param normal_r: R, Axis to bake in red channel
    :type normal_r: str | None
    :param normal_g: G, Axis to bake in green channel
    :type normal_g: str | None
    :param normal_b: B, Axis to bake in blue channel
    :type normal_b: str | None
    :param target: Target, Where to output the baked map
    :type target: str | None
    :param save_mode: Save Mode, Where to save baked image textures
    :type save_mode: str | None
    :param use_clear: Clear, Clear images before baking (only for internal saving)
    :type use_clear: bool | None
    :param use_cage: Cage, Cast rays to active object from a cage
    :type use_cage: bool | None
    :param use_split_materials: Split Materials, Split baked maps per material, using material name in output file (external only)
    :type use_split_materials: bool | None
    :param use_automatic_name: Automatic Name, Automatically name the output file with the pass type
    :type use_automatic_name: bool | None
    :param uv_layer: UV Layer, UV layer to override active
    :type uv_layer: str
    """

    ...

def bake_image(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Bake image textures of selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def camera_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    enter_editmode: bool | None = False,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add a camera object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def clear_override_library(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Delete the selected local overrides and relink their usages to the linked data-blocks if possible, else reset them and mark them as non editable

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def collection_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add an object to a new collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def collection_external_asset_drop(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    session_uid: int | None = 0,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
    use_instance: bool | None = True,
    drop_x: int | None = 0,
    drop_y: int | None = 0,
    collection: str | None = "",
):
    """Add the dragged collection to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param session_uid: Session UID, Session UID of the data-block to use by the operator
        :type session_uid: int | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
        :param use_instance: Instance, Add the dropped collection as collection instance
        :type use_instance: bool | None
        :param drop_x: Drop X, X-coordinate (screen space) to place the new object under
        :type drop_x: int | None
        :param drop_y: Drop Y, Y-coordinate (screen space) to place the new object under
        :type drop_y: int | None
        :param collection: Collection
        :type collection: str | None
    """

    ...

def collection_instance_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "Collection",
    collection: str | None = "",
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
    session_uid: int | None = 0,
    drop_x: int | None = 0,
    drop_y: int | None = 0,
):
    """Add a collection instance

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param name: Name, Collection name to add
        :type name: str
        :param collection: Collection
        :type collection: str | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
        :param session_uid: Session UID, Session UID of the data-block to use by the operator
        :type session_uid: int | None
        :param drop_x: Drop X, X-coordinate (screen space) to place the new object under
        :type drop_x: int | None
        :param drop_y: Drop Y, Y-coordinate (screen space) to place the new object under
        :type drop_y: int | None
    """

    ...

def collection_link(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    collection: str | None = "",
):
    """Add an object to an existing collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection: Collection
    :type collection: str | None
    """

    ...

def collection_objects_select(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Select all objects in collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def collection_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove the active object from this collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def collection_unlink(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Unlink the collection from all objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def constraint_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "",
):
    """Add a constraint to the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    """

    ...

def constraint_add_with_targets(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "",
):
    """Add a constraint to the active object, with target (where applicable) set to the selected objects/bones

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    """

    ...

def constraints_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Clear all constraints from the selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def constraints_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy constraints to other selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def convert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    target: str | None = "MESH",
    keep_original: bool | None = False,
    merge_customdata: bool | None = True,
    angle: float | None = 1.22173,
    thickness: int | None = 5,
    seams: bool | None = False,
    faces: bool | None = True,
    offset: float | None = 0.01,
):
    """Convert selected objects to another type

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param target: Target, Type of object to convert to

    CURVE
    Curve -- Curve from Mesh or Text objects.

    MESH
    Mesh -- Mesh from Curve, Surface, Metaball, Text, or Point Cloud objects.

    POINTCLOUD
    Point Cloud -- Point Cloud from Mesh objects.

    CURVES
    Curves -- Curves from evaluated curve data.

    GREASEPENCIL
    Grease Pencil -- Grease Pencil from Curve or Mesh objects.
        :type target: str | None
        :param keep_original: Keep Original, Keep original objects instead of replacing them
        :type keep_original: bool | None
        :param merge_customdata: Merge UVs, Merge UV coordinates that share a vertex to account for imprecision in some modifiers
        :type merge_customdata: bool | None
        :param angle: Threshold Angle, Threshold to determine ends of the strokes
        :type angle: float | None
        :param thickness: Thickness
        :type thickness: int | None
        :param seams: Only Seam Edges, Convert only seam edges
        :type seams: bool | None
        :param faces: Export Faces, Export faces as filled strokes
        :type faces: bool | None
        :param offset: Stroke Offset, Offset strokes from fill
        :type offset: float | None
    """

    ...

def correctivesmooth_bind(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Bind base pose in Corrective Smooth modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def curves_empty_hair_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add an empty curve object to the scene with the selected mesh as surface

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def curves_random_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add a curves object with random curves to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def data_instance_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "",
    session_uid: int | None = 0,
    type: str | None = "ACTION",
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
    drop_x: int | None = 0,
    drop_y: int | None = 0,
):
    """Add an object data instance

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param name: Name, Name of the data-block to use by the operator
        :type name: str
        :param session_uid: Session UID, Session UID of the data-block to use by the operator
        :type session_uid: int | None
        :param type: Type
        :type type: str | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
        :param drop_x: Drop X, X-coordinate (screen space) to place the new object under
        :type drop_x: int | None
        :param drop_y: Drop Y, Y-coordinate (screen space) to place the new object under
        :type drop_y: int | None
    """

    ...

def data_transfer(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_reverse_transfer: bool | None = False,
    use_freeze: bool | None = False,
    data_type: str | None = "",
    use_create: bool | None = True,
    vert_mapping: str | None = "NEAREST",
    edge_mapping: str | None = "NEAREST",
    loop_mapping: str | None = "NEAREST_POLYNOR",
    poly_mapping: str | None = "NEAREST",
    use_auto_transform: bool | None = False,
    use_object_transform: bool | None = True,
    use_max_distance: bool | None = False,
    max_distance: float | None = 1.0,
    ray_radius: float | None = 0.0,
    islands_precision: float | None = 0.1,
    layers_select_src: str | None = "ACTIVE",
    layers_select_dst: str | None = "ACTIVE",
    mix_mode: str | None = "REPLACE",
    mix_factor: float | None = 1.0,
):
    """Transfer data layer(s) (weights, edge sharp, etc.) from active to selected meshes

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param use_reverse_transfer: Reverse Transfer, Transfer from selected objects to active one
        :type use_reverse_transfer: bool | None
        :param use_freeze: Freeze Operator, Prevent changes to settings to re-run the operator, handy to change several things at once with heavy geometry
        :type use_freeze: bool | None
        :param data_type: Data Type, Which data to transfer

    VGROUP_WEIGHTS
    Vertex Group(s) -- Transfer active or all vertex groups.

    BEVEL_WEIGHT_VERT
    Bevel Weight -- Transfer bevel weights.

    COLOR_VERTEX
    Colors -- Color Attributes.

    SHARP_EDGE
    Sharp -- Transfer sharp mark.

    SEAM
    UV Seam -- Transfer UV seam mark.

    CREASE
    Subdivision Crease -- Transfer crease values.

    BEVEL_WEIGHT_EDGE
    Bevel Weight -- Transfer bevel weights.

    FREESTYLE_EDGE
    Freestyle Mark -- Transfer Freestyle edge mark.

    CUSTOM_NORMAL
    Custom Normals -- Transfer custom normals.

    COLOR_CORNER
    Colors -- Color Attributes.

    UV
    UVs -- Transfer UV layers.

    SMOOTH
    Smooth -- Transfer flat/smooth mark.

    FREESTYLE_FACE
    Freestyle Mark -- Transfer Freestyle face mark.
        :type data_type: str | None
        :param use_create: Create Data, Add data layers on destination meshes if needed
        :type use_create: bool | None
        :param vert_mapping: Vertex Mapping, Method used to map source vertices to destination ones
        :type vert_mapping: str | None
        :param edge_mapping: Edge Mapping, Method used to map source edges to destination ones
        :type edge_mapping: str | None
        :param loop_mapping: Face Corner Mapping, Method used to map source faces' corners to destination ones
        :type loop_mapping: str | None
        :param poly_mapping: Face Mapping, Method used to map source faces to destination ones
        :type poly_mapping: str | None
        :param use_auto_transform: Auto Transform, Automatically compute transformation to get the best possible match between source and destination meshes.Warning: Results will never be as good as manual matching of objects
        :type use_auto_transform: bool | None
        :param use_object_transform: Object Transform, Evaluate source and destination meshes in global space
        :type use_object_transform: bool | None
        :param use_max_distance: Only Neighbor Geometry, Source elements must be closer than given distance from destination one
        :type use_max_distance: bool | None
        :param max_distance: Max Distance, Maximum allowed distance between source and destination element, for non-topology mappings
        :type max_distance: float | None
        :param ray_radius: Ray Radius, 'Width' of rays (especially useful when raycasting against vertices or edges)
        :type ray_radius: float | None
        :param islands_precision: Islands Precision, Factor controlling precision of islands handling (the higher, the better the results)
        :type islands_precision: float | None
        :param layers_select_src: Source Layers Selection, Which layers to transfer, in case of multi-layers types
        :type layers_select_src: str | None
        :param layers_select_dst: Destination Layers Matching, How to match source and destination layers
        :type layers_select_dst: str | None
        :param mix_mode: Mix Mode, How to affect destination elements with source values
        :type mix_mode: str | None
        :param mix_factor: Mix Factor, Factor to use when applying data to destination (exact behavior depends on mix mode)
        :type mix_factor: float | None
    """

    ...

def datalayout_transfer(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    data_type: str | None = "",
    use_delete: bool | None = False,
    layers_select_src: str | None = "ACTIVE",
    layers_select_dst: str | None = "ACTIVE",
):
    """Transfer layout of data layer(s) from active to selected meshes

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param modifier: Modifier, Name of the modifier to edit
        :type modifier: str
        :param data_type: Data Type, Which data to transfer

    VGROUP_WEIGHTS
    Vertex Group(s) -- Transfer active or all vertex groups.

    BEVEL_WEIGHT_VERT
    Bevel Weight -- Transfer bevel weights.

    COLOR_VERTEX
    Colors -- Color Attributes.

    SHARP_EDGE
    Sharp -- Transfer sharp mark.

    SEAM
    UV Seam -- Transfer UV seam mark.

    CREASE
    Subdivision Crease -- Transfer crease values.

    BEVEL_WEIGHT_EDGE
    Bevel Weight -- Transfer bevel weights.

    FREESTYLE_EDGE
    Freestyle Mark -- Transfer Freestyle edge mark.

    CUSTOM_NORMAL
    Custom Normals -- Transfer custom normals.

    COLOR_CORNER
    Colors -- Color Attributes.

    UV
    UVs -- Transfer UV layers.

    SMOOTH
    Smooth -- Transfer flat/smooth mark.

    FREESTYLE_FACE
    Freestyle Mark -- Transfer Freestyle face mark.
        :type data_type: str | None
        :param use_delete: Exact Match, Also delete some data layers from destination if necessary, so that it matches exactly source
        :type use_delete: bool | None
        :param layers_select_src: Source Layers Selection, Which layers to transfer, in case of multi-layers types
        :type layers_select_src: str | None
        :param layers_select_dst: Destination Layers Matching, How to match source and destination layers
        :type layers_select_dst: str | None
    """

    ...

def delete(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_global: bool | None = False,
    confirm: bool | None = True,
):
    """Delete selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_global: Delete Globally, Remove object from all scenes
    :type use_global: bool | None
    :param confirm: Confirm, Prompt for confirmation
    :type confirm: bool | None
    """

    ...

def drop_geometry_nodes(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    session_uid: int | None = 0,
    show_datablock_in_modifier: bool | None = True,
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param session_uid: Session UID, Session UID of the geometry node group being dropped
    :type session_uid: int | None
    :param show_datablock_in_modifier: Show the datablock selector in the modifier
    :type show_datablock_in_modifier: bool | None
    """

    ...

def drop_named_material(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "",
    session_uid: int | None = 0,
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of the data-block to use by the operator
    :type name: str
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: int | None
    """

    ...

def duplicate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    linked: bool | None = False,
    mode: str | None = "TRANSLATION",
):
    """Duplicate selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param linked: Linked, Duplicate object but not object data, linking to the original data
    :type linked: bool | None
    :param mode: Mode
    :type mode: str | None
    """

    ...

def duplicate_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    OBJECT_OT_duplicate: duplicate | None = None,
    TRANSFORM_OT_translate: bpy.ops.transform.translate | None = None,
):
    """Duplicate the selected objects and move them

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param OBJECT_OT_duplicate: Duplicate Objects, Duplicate selected objects
    :type OBJECT_OT_duplicate: duplicate | None
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: bpy.ops.transform.translate | None
    """

    ...

def duplicate_move_linked(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    OBJECT_OT_duplicate: duplicate | None = None,
    TRANSFORM_OT_translate: bpy.ops.transform.translate | None = None,
):
    """Duplicate the selected objects, but not their object data, and move them

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param OBJECT_OT_duplicate: Duplicate Objects, Duplicate selected objects
    :type OBJECT_OT_duplicate: duplicate | None
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: bpy.ops.transform.translate | None
    """

    ...

def duplicates_make_real(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_base_parent: bool | None = False,
    use_hierarchy: bool | None = False,
):
    """Make instanced objects attached to this object real

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_base_parent: Parent, Parent newly created objects to the original instancer
    :type use_base_parent: bool | None
    :param use_hierarchy: Keep Hierarchy, Maintain parent child relationships
    :type use_hierarchy: bool | None
    """

    ...

def editmode_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Toggle object's edit mode

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def effector_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "FORCE",
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add an empty object with a physics effector to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type
        :type type: str | None
        :param radius: Radius
        :type radius: float | None
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def empty_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "PLAIN_AXES",
    radius: float | None = 1.0,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add an empty object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type
        :type type: str | None
        :param radius: Radius
        :type radius: float | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def empty_image_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = False,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = True,
    filter_movie: bool | None = True,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_obj: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 9,
    relative_path: bool | None = True,
    show_multiview: bool | None = False,
    use_multiview: bool | None = False,
    display_type: str | None = "DEFAULT",
    sort_method: str | None = "",
    name: str = "",
    session_uid: int | None = 0,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
    background: bool | None = False,
):
    """Add an empty image type to scene with data

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | None
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter Python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_obj: Filter OBJ files
        :type filter_obj: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: bool | None
        :param show_multiview: Enable Multi-View
        :type show_multiview: bool | None
        :param use_multiview: Use Multi-View
        :type use_multiview: bool | None
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: str | None
        :param sort_method: File sorting mode

    DEFAULT
    Default -- Automatically determine sort method for files.

    FILE_SORT_ALPHA
    Name -- Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension -- Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date -- Sort files by modification time.

    FILE_SORT_SIZE
    Size -- Sort files by size.
        :type sort_method: str | None
        :param name: Name, Name of the data-block to use by the operator
        :type name: str
        :param session_uid: Session UID, Session UID of the data-block to use by the operator
        :type session_uid: int | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
        :param background: Put in Background, Make the image render behind all objects
        :type background: bool | None
    """

    ...

def explode_refresh(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Refresh data in the Explode modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def forcefield_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Toggle object's force field

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def geometry_node_bake_delete_single(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    session_uid: int | None = 0,
    modifier_name: str = "",
    bake_id: int | None = 0,
):
    """Delete baked data of a single bake node or simulation

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: int | None
    :param modifier_name: Modifier Name, Name of the modifier that contains the node
    :type modifier_name: str
    :param bake_id: Bake ID, Nested node id of the node
    :type bake_id: int | None
    """

    ...

def geometry_node_bake_single(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    session_uid: int | None = 0,
    modifier_name: str = "",
    bake_id: int | None = 0,
):
    """Bake a single bake node or simulation

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: int | None
    :param modifier_name: Modifier Name, Name of the modifier that contains the node
    :type modifier_name: str
    :param bake_id: Bake ID, Nested node id of the node
    :type bake_id: int | None
    """

    ...

def geometry_node_tree_copy_assign(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy the active geometry node group and assign it to the active modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def geometry_nodes_input_attribute_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    input_name: str = "",
    modifier_name: str = "",
):
    """Switch between an attribute and a single value to define the data for every element

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param input_name: Input Name
    :type input_name: str
    :param modifier_name: Modifier Name
    :type modifier_name: str
    """

    ...

def geometry_nodes_move_to_nodes(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_selected_objects: bool | None = False,
):
    """Move inputs and outputs from in the modifier to a new node group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_selected_objects: Selected Objects, Affect all selected objects instead of just the active object
    :type use_selected_objects: bool | None
    """

    ...

def gpencil_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    radius: float | None = 1.0,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
    type: str | None = "EMPTY",
    use_in_front: bool | None = True,
    stroke_depth_offset: float | None = 0.05,
    use_lights: bool | None = False,
    stroke_depth_order: str | None = "3D",
):
    """Add a Grease Pencil object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param radius: Radius
        :type radius: float | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
        :param type: Type
        :type type: str | None
        :param use_in_front: Show In Front, Show Line Art grease pencil in front of everything
        :type use_in_front: bool | None
        :param stroke_depth_offset: Stroke Offset, Stroke offset for the Line Art modifier
        :type stroke_depth_offset: float | None
        :param use_lights: Use Lights, Use lights for this grease pencil object
        :type use_lights: bool | None
        :param stroke_depth_order: Stroke Depth Order, Defines how the strokes are ordered in 3D space (for objects not displayed 'In Front')

    2D
    2D Layers -- Display strokes using grease pencil layers to define order.

    3D
    3D Location -- Display strokes using real 3D position in 3D space.
        :type stroke_depth_order: str | None
    """

    ...

def grease_pencil_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "EMPTY",
    use_in_front: bool | None = True,
    stroke_depth_offset: float | None = 0.05,
    use_lights: bool | None = False,
    stroke_depth_order: str | None = "3D",
    radius: float | None = 1.0,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add a Grease Pencil object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type
        :type type: str | None
        :param use_in_front: Show In Front, Show Line Art grease pencil in front of everything
        :type use_in_front: bool | None
        :param stroke_depth_offset: Stroke Offset, Stroke offset for the Line Art modifier
        :type stroke_depth_offset: float | None
        :param use_lights: Use Lights, Use lights for this grease pencil object
        :type use_lights: bool | None
        :param stroke_depth_order: Stroke Depth Order, Defines how the strokes are ordered in 3D space (for objects not displayed 'In Front')

    2D
    2D Layers -- Display strokes using grease pencil layers to define order.

    3D
    3D Location -- Display strokes using real 3D position in 3D space.
        :type stroke_depth_order: str | None
        :param radius: Radius
        :type radius: float | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def grease_pencil_dash_modifier_segment_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Add a segment to the dash modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def grease_pencil_dash_modifier_segment_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    type: str | None = "UP",
):
    """Move the active dash segment up or down

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param type: Type
    :type type: str | None
    """

    ...

def grease_pencil_dash_modifier_segment_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    index: int | None = 0,
):
    """Remove the active segment from the dash modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param index: Index, Index of the segment to remove
    :type index: int | None
    """

    ...

def grease_pencil_time_modifier_segment_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Add a segment to the time modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def grease_pencil_time_modifier_segment_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    type: str | None = "UP",
):
    """Move the active time segment up or down

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param type: Type
    :type type: str | None
    """

    ...

def grease_pencil_time_modifier_segment_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    index: int | None = 0,
):
    """Remove the active segment from the time modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param index: Index, Index of the segment to remove
    :type index: int | None
    """

    ...

def hide_collection(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    collection_index: int | None = -1,
    toggle: bool | None = False,
    extend: bool | None = False,
):
    """Show only objects in collection (Shift to extend)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection_index: Collection Index, Index of the collection to change visibility
    :type collection_index: int | None
    :param toggle: Toggle, Toggle visibility
    :type toggle: bool | None
    :param extend: Extend, Extend visibility
    :type extend: bool | None
    """

    ...

def hide_render_clear_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Reveal all render objects by setting the hide render flag

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def hide_view_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    select: bool | None = True,
):
    """Reveal temporarily hidden objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param select: Select
    :type select: bool | None
    """

    ...

def hide_view_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    unselected: bool | None = False,
):
    """Temporarily hide objects from the viewport

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param unselected: Unselected, Hide unselected rather than selected objects
    :type unselected: bool | None
    """

    ...

def hook_add_newob(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Hook selected vertices to a newly created object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def hook_add_selob(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_bone: bool | None = False,
):
    """Hook selected vertices to the first selected object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_bone: Active Bone, Assign the hook to the hook object's active bone
    :type use_bone: bool | None
    """

    ...

def hook_assign(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str | None = "",
):
    """Assign the selected vertices to a hook

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Modifier number to assign to
    :type modifier: str | None
    """

    ...

def hook_recenter(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str | None = "",
):
    """Set hook center to cursor position

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Modifier number to assign to
    :type modifier: str | None
    """

    ...

def hook_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str | None = "",
):
    """Remove a hook from the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Modifier number to remove
    :type modifier: str | None
    """

    ...

def hook_reset(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str | None = "",
):
    """Recalculate and clear offset transformation

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Modifier number to assign to
    :type modifier: str | None
    """

    ...

def hook_select(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str | None = "",
):
    """Select affected vertices on mesh

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Modifier number to remove
    :type modifier: str | None
    """

    ...

def instance_offset_from_cursor(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Set offset used for collection instances based on cursor position

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def instance_offset_from_object(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Set offset used for collection instances based on the active object position

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def instance_offset_to_cursor(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Set cursor position to the offset used for collection instances

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def isolate_type_render(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Hide unselected render objects of same type as active by setting the hide render flag

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def join(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Join selected objects into active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def join_shapes(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy the current resulting shape of another selected object to this one

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def join_uvs(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Transfer UV Maps from active to selected objects (needs matching geometry)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def laplaciandeform_bind(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Bind mesh to system in laplacian deform modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def light_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "POINT",
    radius: float | None = 1.0,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add a light object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type
        :type type: str | None
        :param radius: Radius
        :type radius: float | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def light_linking_blocker_collection_new(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Create new light linking collection used by the active emitter

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def light_linking_blockers_link(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    link_state: str | None = "INCLUDE",
):
    """Light link selected blockers to the active emitter object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param link_state: Link State, State of the shadow linking

    INCLUDE
    Include -- Include selected blockers to cast shadows from the active emitter.

    EXCLUDE
    Exclude -- Exclude selected blockers from casting shadows from the active emitter.
        :type link_state: str | None
    """

    ...

def light_linking_blockers_select(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Select all objects which block light from this emitter

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def light_linking_receiver_collection_new(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Create new light linking collection used by the active emitter

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def light_linking_receivers_link(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    link_state: str | None = "INCLUDE",
):
    """Light link selected receivers to the active emitter object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param link_state: Link State, State of the light linking

    INCLUDE
    Include -- Include selected receivers to receive light from the active emitter.

    EXCLUDE
    Exclude -- Exclude selected receivers from receiving light from the active emitter.
        :type link_state: str | None
    """

    ...

def light_linking_receivers_select(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Select all objects which receive light from this emitter

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def light_linking_unlink_from_collection(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove this object or collection from the light linking collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def lightprobe_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "SPHERE",
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add a light probe object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    SPHERE
    Sphere -- Light probe that captures precise lighting from all directions at a single point in space.

    PLANE
    Plane -- Light probe that captures incoming light from a single direction on a plane.

    VOLUME
    Volume -- Light probe that captures low frequency lighting inside a volume.
        :type type: str | None
        :param radius: Radius
        :type radius: float | None
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def lightprobe_cache_bake(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    subset: str | None = "ALL",
):
    """Bake irradiance volume light cache

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param subset: Subset, Subset of probes to update

    ALL
    All Volumes -- Bake all light probe volumes.

    SELECTED
    Selected Only -- Only bake selected light probe volumes.

    ACTIVE
    Active Only -- Only bake the active light probe volume.
        :type subset: str | None
    """

    ...

def lightprobe_cache_free(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    subset: str | None = "SELECTED",
):
    """Delete cached indirect lighting

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param subset: Subset, Subset of probes to update

    ALL
    All Light Probes -- Delete all light probes' baked lighting data.

    SELECTED
    Selected Only -- Only delete selected light probes' baked lighting data.

    ACTIVE
    Active Only -- Only delete the active light probe's baked lighting data.
        :type subset: str | None
    """

    ...

def lineart_bake_strokes(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    bake_all: bool | None = False,
):
    """Bake Line Art for current Grease Pencil object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param bake_all: Bake All, Bake all line art modifiers
    :type bake_all: bool | None
    """

    ...

def lineart_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    clear_all: bool | None = False,
):
    """Clear all strokes in current Grease Pencil object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param clear_all: Clear All, Clear all line art modifier bakes
    :type clear_all: bool | None
    """

    ...

def link_to_collection(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    collection_index: int | None = -1,
    is_new: bool | None = False,
    new_collection_name: str = "",
):
    """Link objects to a collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection_index: Collection Index, Index of the collection to move to
    :type collection_index: int | None
    :param is_new: New, Move objects to a new collection
    :type is_new: bool | None
    :param new_collection_name: Name, Name of the newly added collection
    :type new_collection_name: str
    """

    ...

def location_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    clear_delta: bool | None = False,
):
    """Clear the object's location

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param clear_delta: Clear Delta, Clear delta location in addition to clearing the normal location transform
    :type clear_delta: bool | None
    """

    ...

def make_dupli_face(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Convert objects into instanced faces

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def make_links_data(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "OBDATA",
):
    """Transfer data from active object to selected objects

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    OBDATA
    Link Object Data -- Replace assigned Object Data.

    MATERIAL
    Link Materials -- Replace assigned Materials.

    ANIMATION
    Link Animation Data -- Replace assigned Animation Data.

    GROUPS
    Link Collections -- Replace assigned Collections.

    DUPLICOLLECTION
    Link Instance Collection -- Replace assigned Collection Instance.

    FONTS
    Link Fonts to Text -- Replace Text object Fonts.

    MODIFIERS
    Copy Modifiers -- Replace Modifiers.

    EFFECTS
    Copy Grease Pencil Effects -- Replace Grease Pencil Effects.
        :type type: str | None
    """

    ...

def make_links_scene(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    scene: str | None = "",
):
    """Link selection to another scene

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param scene: Scene
    :type scene: str | None
    """

    ...

def make_local(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "SELECT_OBJECT",
):
    """Make library linked data-blocks local to this file

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    """

    ...

def make_override_library(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    collection: int | None = 0,
):
    """Create a local override of the selected linked objects, and their hierarchy of dependencies

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection: Override Collection, Session UID of the directly linked collection containing the selected object, to make an override from
    :type collection: int | None
    """

    ...

def make_single_user(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "SELECTED_OBJECTS",
    object: bool | None = False,
    obdata: bool | None = False,
    material: bool | None = False,
    animation: bool | None = False,
    obdata_animation: bool | None = False,
):
    """Make linked data local to each object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    :param object: Object, Make single user objects
    :type object: bool | None
    :param obdata: Object Data, Make single user object data
    :type obdata: bool | None
    :param material: Materials, Make materials local to each data-block
    :type material: bool | None
    :param animation: Object Animation, Make object animation data local to each object
    :type animation: bool | None
    :param obdata_animation: Object Data Animation, Make object data (mesh, curve etc.) animation data local to each object
    :type obdata_animation: bool | None
    """

    ...

def material_slot_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add a new material slot

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def material_slot_assign(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Assign active material slot to selection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def material_slot_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy material to selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def material_slot_deselect(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Deselect by active material slot

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def material_slot_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    direction: str | None = "UP",
):
    """Move the active material up/down in the list

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction, Direction to move the active material towards
    :type direction: str | None
    """

    ...

def material_slot_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove the selected material slot

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def material_slot_remove_unused(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove unused material slots

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def material_slot_select(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Select by active material slot

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def meshdeform_bind(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Bind mesh to cage in mesh deform modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def metaball_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "BALL",
    radius: float | None = 2.0,
    enter_editmode: bool | None = False,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add an metaball object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Primitive
        :type type: str | None
        :param radius: Radius
        :type radius: float | None
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def mode_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: str | None = "OBJECT",
    toggle: bool | None = False,
):
    """Sets the object interaction mode

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: str | None
    :param toggle: Toggle
    :type toggle: bool | None
    """

    ...

def mode_set_with_submode(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: str | None = "OBJECT",
    toggle: bool | None = False,
    mesh_select_mode: set[str] | None = {},
):
    """Sets the object interaction mode

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: str | None
    :param toggle: Toggle
    :type toggle: bool | None
    :param mesh_select_mode: Mesh Mode
    :type mesh_select_mode: set[str] | None
    """

    ...

def modifier_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "SUBSURF",
    use_selected_objects: bool | None = False,
):
    """Add a procedural operation/effect to the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    :param use_selected_objects: Selected Objects, Affect all selected objects instead of just the active object
    :type use_selected_objects: bool | None
    """

    ...

def modifier_add_node_group(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    asset_library_type: str | None = "LOCAL",
    asset_library_identifier: str = "",
    relative_asset_identifier: str = "",
    session_uid: int | None = 0,
    use_selected_objects: bool | None = False,
):
    """Add a procedural operation/effect to the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param asset_library_type: Asset Library Type
    :type asset_library_type: str | None
    :param asset_library_identifier: Asset Library Identifier
    :type asset_library_identifier: str
    :param relative_asset_identifier: Relative Asset Identifier
    :type relative_asset_identifier: str
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: int | None
    :param use_selected_objects: Selected Objects, Affect all selected objects instead of just the active object
    :type use_selected_objects: bool | None
    """

    ...

def modifier_apply(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    report: bool | None = False,
    merge_customdata: bool | None = True,
    single_user: bool | None = False,
    use_selected_objects: bool | None = False,
):
    """Apply modifier and remove from the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param report: Report, Create a notification after the operation
    :type report: bool | None
    :param merge_customdata: Merge UVs, For mesh objects, merge UV coordinates that share a vertex to account for imprecision in some modifiers
    :type merge_customdata: bool | None
    :param single_user: Make Data Single User, Make the object's data single user if needed
    :type single_user: bool | None
    :param use_selected_objects: Selected Objects, Affect all selected objects instead of just the active object
    :type use_selected_objects: bool | None
    """

    ...

def modifier_apply_as_shapekey(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    keep_modifier: bool | None = False,
    modifier: str = "",
    report: bool | None = False,
):
    """Apply modifier as a new shape key and remove from the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param keep_modifier: Keep Modifier, Do not remove the modifier from stack
    :type keep_modifier: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param report: Report, Create a notification after the operation
    :type report: bool | None
    """

    ...

def modifier_convert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Convert particles to a mesh object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def modifier_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    use_selected_objects: bool | None = False,
):
    """Duplicate modifier at the same position in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param use_selected_objects: Selected Objects, Affect all selected objects instead of just the active object
    :type use_selected_objects: bool | None
    """

    ...

def modifier_copy_to_selected(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Copy the modifier from the active object to all selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def modifier_move_down(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Move modifier down in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def modifier_move_to_index(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    index: int | None = 0,
    use_selected_objects: bool | None = False,
):
    """Change the modifier's index in the stack so it evaluates after the set number of others

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param index: Index, The index to move the modifier to
    :type index: int | None
    :param use_selected_objects: Selected Objects, Affect all selected objects instead of just the active object
    :type use_selected_objects: bool | None
    """

    ...

def modifier_move_up(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Move modifier up in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def modifier_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    report: bool | None = False,
    use_selected_objects: bool | None = False,
):
    """Remove a modifier from the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param report: Report, Create a notification after the operation
    :type report: bool | None
    :param use_selected_objects: Selected Objects, Affect all selected objects instead of just the active object
    :type use_selected_objects: bool | None
    """

    ...

def modifier_set_active(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Activate the modifier to use as the context

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def modifiers_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Clear all modifiers from the selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def modifiers_copy_to_selected(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy modifiers to other selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def move_to_collection(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    collection_index: int | None = -1,
    is_new: bool | None = False,
    new_collection_name: str = "",
):
    """Move objects to a collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection_index: Collection Index, Index of the collection to move to
    :type collection_index: int | None
    :param is_new: New, Move objects to a new collection
    :type is_new: bool | None
    :param new_collection_name: Name, Name of the newly added collection
    :type new_collection_name: str
    """

    ...

def multires_base_apply(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Modify the base mesh to conform to the displaced mesh

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def multires_external_pack(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Pack displacements from an external file

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def multires_external_save(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = True,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = True,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_obj: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 9,
    relative_path: bool | None = True,
    display_type: str | None = "DEFAULT",
    sort_method: str | None = "",
    modifier: str = "",
):
    """Save displacements to an external file

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | None
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter Python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_obj: Filter OBJ files
        :type filter_obj: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: bool | None
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: str | None
        :param sort_method: File sorting mode
        :type sort_method: str | None
        :param modifier: Modifier, Name of the modifier to edit
        :type modifier: str
    """

    ...

def multires_higher_levels_delete(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Deletes the higher resolution mesh, potential loss of detail

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def multires_rebuild_subdiv(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Rebuilds all possible subdivisions levels to generate a lower resolution base mesh

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def multires_reshape(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Copy vertex coordinates from other object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def multires_subdivide(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    mode: str | None = "CATMULL_CLARK",
):
    """Add a new level of subdivision

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param modifier: Modifier, Name of the modifier to edit
        :type modifier: str
        :param mode: Subdivision Mode, How the mesh is going to be subdivided to create a new level

    CATMULL_CLARK
    Catmull-Clark -- Create a new level using Catmull-Clark subdivisions.

    SIMPLE
    Simple -- Create a new level using simple subdivisions.

    LINEAR
    Linear -- Create a new level using linear interpolation of the sculpted displacement.
        :type mode: str | None
    """

    ...

def multires_unsubdivide(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Rebuild a lower subdivision level of the current base mesh

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def ocean_bake(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    free: bool | None = False,
):
    """Bake an image sequence of ocean data

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param free: Free, Free the bake, rather than generating it
    :type free: bool | None
    """

    ...

def origin_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Clear the object's origin

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def origin_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "GEOMETRY_ORIGIN",
    center: str | None = "MEDIAN",
):
    """Set the object's origin, by either moving the data, or set to center of data, or use 3D cursor

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    GEOMETRY_ORIGIN
    Geometry to Origin -- Move object geometry to object origin.

    ORIGIN_GEOMETRY
    Origin to Geometry -- Calculate the center of geometry based on the current pivot point (median, otherwise bounding box).

    ORIGIN_CURSOR
    Origin to 3D Cursor -- Move object origin to position of the 3D cursor.

    ORIGIN_CENTER_OF_MASS
    Origin to Center of Mass (Surface) -- Calculate the center of mass from the surface area.

    ORIGIN_CENTER_OF_VOLUME
    Origin to Center of Mass (Volume) -- Calculate the center of mass from the volume (must be manifold geometry with consistent normals).
        :type type: str | None
        :param center: Center
        :type center: str | None
    """

    ...

def parent_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "CLEAR",
):
    """Clear the object's parenting

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    CLEAR
    Clear Parent -- Completely clear the parenting relationship, including involved modifiers if any.

    CLEAR_KEEP_TRANSFORM
    Clear and Keep Transformation -- As 'Clear Parent', but keep the current visual transformations of the object.

    CLEAR_INVERSE
    Clear Parent Inverse -- Reset the transform corrections applied to the parenting relationship, does not remove parenting itself.
        :type type: str | None
    """

    ...

def parent_inverse_apply(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Apply the object's parent inverse to its data

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def parent_no_inverse_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    keep_transform: bool | None = False,
):
    """Set the object's parenting without setting the inverse parent correction

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param keep_transform: Keep Transform, Preserve the world transform throughout parenting
    :type keep_transform: bool | None
    """

    ...

def parent_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "OBJECT",
    xmirror: bool | None = False,
    keep_transform: bool | None = False,
):
    """Set the object's parenting

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    :param xmirror: X Mirror, Apply weights symmetrically along X axis, for Envelope/Automatic vertex groups creation
    :type xmirror: bool | None
    :param keep_transform: Keep Transform, Apply transformation before parenting
    :type keep_transform: bool | None
    """

    ...

def particle_system_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add a particle system

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def particle_system_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove the selected particle system

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def paths_calculate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    display_type: str | None = "RANGE",
    range: str | None = "SCENE",
):
    """Generate motion paths for the selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param display_type: Display type
    :type display_type: str | None
    :param range: Computation Range
    :type range: str | None
    """

    ...

def paths_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    only_selected: bool | None = False,
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param only_selected: Only Selected, Only clear motion paths of selected objects
    :type only_selected: bool | None
    """

    ...

def paths_update(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Recalculate motion paths for selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def paths_update_visible(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Recalculate all visible motion paths for objects and poses

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def pointcloud_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add a point cloud object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def posemode_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Enable or disable posing/selecting bones

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def quadriflow_remesh(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_mesh_symmetry: bool | None = True,
    use_preserve_sharp: bool | None = False,
    use_preserve_boundary: bool | None = False,
    preserve_attributes: bool | None = False,
    smooth_normals: bool | None = False,
    mode: str | None = "FACES",
    target_ratio: float | None = 1.0,
    target_edge_length: float | None = 0.1,
    target_faces: int | None = 4000,
    mesh_area: float | None = -1.0,
    seed: int | None = 0,
):
    """Create a new quad based mesh using the surface data of the current mesh. All data layers will be lost

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param use_mesh_symmetry: Use Mesh Symmetry, Generates a symmetrical mesh using the mesh symmetry configuration
        :type use_mesh_symmetry: bool | None
        :param use_preserve_sharp: Preserve Sharp, Try to preserve sharp features on the mesh
        :type use_preserve_sharp: bool | None
        :param use_preserve_boundary: Preserve Mesh Boundary, Try to preserve mesh boundary on the mesh
        :type use_preserve_boundary: bool | None
        :param preserve_attributes: Preserve Attributes, Reproject attributes onto the new mesh
        :type preserve_attributes: bool | None
        :param smooth_normals: Smooth Normals, Set the output mesh normals to smooth
        :type smooth_normals: bool | None
        :param mode: Mode, How to specify the amount of detail for the new mesh

    RATIO
    Ratio -- Specify target number of faces relative to the current mesh.

    EDGE
    Edge Length -- Input target edge length in the new mesh.

    FACES
    Faces -- Input target number of faces in the new mesh.
        :type mode: str | None
        :param target_ratio: Ratio, Relative number of faces compared to the current mesh
        :type target_ratio: float | None
        :param target_edge_length: Edge Length, Target edge length in the new mesh
        :type target_edge_length: float | None
        :param target_faces: Number of Faces, Approximate number of faces (quads) in the new mesh
        :type target_faces: int | None
        :param mesh_area: Old Object Face Area, This property is only used to cache the object area for later calculations
        :type mesh_area: float | None
        :param seed: Seed, Random seed to use with the solver. Different seeds will cause the remesher to come up with different quad layouts on the mesh
        :type seed: int | None
    """

    ...

def quick_explode(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    style: str | None = "EXPLODE",
    amount: int | None = 100,
    frame_duration: int | None = 50,
    frame_start: int | None = 1,
    frame_end: int | None = 10,
    velocity: float | None = 1.0,
    fade: bool | None = True,
):
    """Make selected objects explode

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param style: Explode Style
    :type style: str | None
    :param amount: Number of Pieces
    :type amount: int | None
    :param frame_duration: Duration
    :type frame_duration: int | None
    :param frame_start: Start Frame
    :type frame_start: int | None
    :param frame_end: End Frame
    :type frame_end: int | None
    :param velocity: Outwards Velocity
    :type velocity: float | None
    :param fade: Fade, Fade the pieces over time
    :type fade: bool | None
    """

    ...

def quick_fur(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    density: str | None = "MEDIUM",
    length: float | None = 0.1,
    radius: float | None = 0.001,
    view_percentage: float | None = 1.0,
    apply_hair_guides: bool | None = True,
    use_noise: bool | None = True,
    use_frizz: bool | None = True,
):
    """Add a fur setup to the selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param density: Density
    :type density: str | None
    :param length: Length
    :type length: float | None
    :param radius: Hair Radius
    :type radius: float | None
    :param view_percentage: View Percentage
    :type view_percentage: float | None
    :param apply_hair_guides: Apply Hair Guides
    :type apply_hair_guides: bool | None
    :param use_noise: Noise
    :type use_noise: bool | None
    :param use_frizz: Frizz
    :type use_frizz: bool | None
    """

    ...

def quick_liquid(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    show_flows: bool | None = False,
):
    """Make selected objects liquid

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param show_flows: Render Liquid Objects, Keep the liquid objects visible during rendering
    :type show_flows: bool | None
    """

    ...

def quick_smoke(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    style: str | None = "SMOKE",
    show_flows: bool | None = False,
):
    """Use selected objects as smoke emitters

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param style: Smoke Style
    :type style: str | None
    :param show_flows: Render Smoke Objects, Keep the smoke objects visible during rendering
    :type show_flows: bool | None
    """

    ...

def randomize_transform(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    random_seed: int | None = 0,
    use_delta: bool | None = False,
    use_loc: bool | None = True,
    loc: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
    use_rot: bool | None = True,
    rot: collections.abc.Sequence[float] | mathutils.Euler | None = (0.0, 0.0, 0.0),
    use_scale: bool | None = True,
    scale_even: bool | None = False,
    scale: collections.abc.Iterable[float] | None = (1.0, 1.0, 1.0),
):
    """Randomize objects location, rotation, and scale

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param random_seed: Random Seed, Seed value for the random generator
    :type random_seed: int | None
    :param use_delta: Transform Delta, Randomize delta transform values instead of regular transform
    :type use_delta: bool | None
    :param use_loc: Randomize Location, Randomize the location values
    :type use_loc: bool | None
    :param loc: Location, Maximum distance the objects can spread over each axis
    :type loc: collections.abc.Sequence[float] | mathutils.Vector | None
    :param use_rot: Randomize Rotation, Randomize the rotation values
    :type use_rot: bool | None
    :param rot: Rotation, Maximum rotation over each axis
    :type rot: collections.abc.Sequence[float] | mathutils.Euler | None
    :param use_scale: Randomize Scale, Randomize the scale values
    :type use_scale: bool | None
    :param scale_even: Scale Even, Use the same scale value for all axis
    :type scale_even: bool | None
    :param scale: Scale, Maximum scale randomization over each axis
    :type scale: collections.abc.Iterable[float] | None
    """

    ...

def reset_override_library(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Reset the selected local overrides to their linked references values

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def rotation_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    clear_delta: bool | None = False,
):
    """Clear the object's rotation

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param clear_delta: Clear Delta, Clear delta rotation in addition to clearing the normal rotation transform
    :type clear_delta: bool | None
    """

    ...

def scale_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    clear_delta: bool | None = False,
):
    """Clear the object's scale

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param clear_delta: Clear Delta, Clear delta scale in addition to clearing the normal scale transform
    :type clear_delta: bool | None
    """

    ...

def select_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    action: str | None = "TOGGLE",
):
    """Change selection of all visible objects in scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param action: Action, Selection action to execute

    TOGGLE
    Toggle -- Toggle selection for all elements.

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.

    INVERT
    Invert -- Invert selection of all elements.
        :type action: str | None
    """

    ...

def select_by_type(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    extend: bool | None = False,
    type: str | None = "MESH",
):
    """Select all visible objects that are of a type

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param extend: Extend, Extend selection instead of deselecting everything first
    :type extend: bool | None
    :param type: Type
    :type type: str | None
    """

    ...

def select_camera(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    extend: bool | None = False,
):
    """Select the active camera

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param extend: Extend, Extend the selection
    :type extend: bool | None
    """

    ...

def select_grouped(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    extend: bool | None = False,
    type: str | None = "CHILDREN_RECURSIVE",
):
    """Select all visible objects grouped by various properties

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param extend: Extend, Extend selection instead of deselecting everything first
        :type extend: bool | None
        :param type: Type

    CHILDREN_RECURSIVE
    Children.

    CHILDREN
    Immediate Children.

    PARENT
    Parent.

    SIBLINGS
    Siblings -- Shared parent.

    TYPE
    Type -- Shared object type.

    COLLECTION
    Collection -- Shared collection.

    HOOK
    Hook.

    PASS
    Pass -- Render pass index.

    COLOR
    Color -- Object color.

    KEYINGSET
    Keying Set -- Objects included in active Keying Set.

    LIGHT_TYPE
    Light Type -- Matching light types.
        :type type: str | None
    """

    ...

def select_hierarchy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    direction: str | None = "PARENT",
    extend: bool | None = False,
):
    """Select object relative to the active object's position in the hierarchy

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction, Direction to select in the hierarchy
    :type direction: str | None
    :param extend: Extend, Extend the existing selection
    :type extend: bool | None
    """

    ...

def select_less(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Deselect objects at the boundaries of parent/child relationships

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def select_linked(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    extend: bool | None = False,
    type: str | None = "OBDATA",
):
    """Select all visible objects that are linked

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param extend: Extend, Extend selection instead of deselecting everything first
    :type extend: bool | None
    :param type: Type
    :type type: str | None
    """

    ...

def select_mirror(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    extend: bool | None = False,
):
    """Select the mirror objects of the selected object e.g. "L.sword" and "R.sword"

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param extend: Extend, Extend selection instead of deselecting everything first
    :type extend: bool | None
    """

    ...

def select_more(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Select connected parent/child objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def select_pattern(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    pattern: str = "*",
    case_sensitive: bool | None = False,
    extend: bool | None = True,
):
    """Select objects matching a naming pattern

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param pattern: Pattern, Name filter using '*', '?' and '[abc]' unix style wildcards
    :type pattern: str
    :param case_sensitive: Case Sensitive, Do a case sensitive compare
    :type case_sensitive: bool | None
    :param extend: Extend, Extend the existing selection
    :type extend: bool | None
    """

    ...

def select_random(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    ratio: float | None = 0.5,
    seed: int | None = 0,
    action: str | None = "SELECT",
):
    """Select or deselect random visible objects

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param ratio: Ratio, Portion of items to select randomly
        :type ratio: float | None
        :param seed: Random Seed, Seed for the random number generator
        :type seed: int | None
        :param action: Action, Selection action to execute

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.
        :type action: str | None
    """

    ...

def select_same_collection(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    collection: str = "",
):
    """Select object in the same collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection: Collection, Name of the collection to select
    :type collection: str
    """

    ...

def shade_auto_smooth(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_auto_smooth: bool | None = True,
    angle: float | None = 0.523599,
):
    """Add modifier to automatically set the sharpness of mesh edges based on the angle between the neighboring faces

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_auto_smooth: Auto Smooth, Add modifier to set edge sharpness automatically
    :type use_auto_smooth: bool | None
    :param angle: Angle, Maximum angle between face normals that will be considered as smooth
    :type angle: float | None
    """

    ...

def shade_flat(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    keep_sharp_edges: bool | None = True,
):
    """Render and display faces uniform, using face normals

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param keep_sharp_edges: Keep Sharp Edges, Don't remove sharp edges, which are redundant with faces shaded smooth
    :type keep_sharp_edges: bool | None
    """

    ...

def shade_smooth(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    keep_sharp_edges: bool | None = True,
):
    """Render and display faces smooth, using interpolated vertex normals

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param keep_sharp_edges: Keep Sharp Edges, Don't remove sharp edges. Tagged edges will remain sharp
    :type keep_sharp_edges: bool | None
    """

    ...

def shade_smooth_by_angle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    angle: float | None = 0.523599,
    keep_sharp_edges: bool | None = True,
):
    """Set the sharpness of mesh edges based on the angle between the neighboring faces

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param angle: Angle, Maximum angle between face normals that will be considered as smooth
    :type angle: float | None
    :param keep_sharp_edges: Keep Sharp Edges, Only add sharp edges instead of clearing existing tags first
    :type keep_sharp_edges: bool | None
    """

    ...

def shaderfx_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "FX_BLUR",
):
    """Add a visual effect to the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    """

    ...

def shaderfx_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    shaderfx: str = "",
):
    """Duplicate effect at the same position in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param shaderfx: Shader, Name of the shaderfx to edit
    :type shaderfx: str
    """

    ...

def shaderfx_move_down(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    shaderfx: str = "",
):
    """Move effect down in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param shaderfx: Shader, Name of the shaderfx to edit
    :type shaderfx: str
    """

    ...

def shaderfx_move_to_index(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    shaderfx: str = "",
    index: int | None = 0,
):
    """Change the effect's position in the list so it evaluates after the set number of others

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param shaderfx: Shader, Name of the shaderfx to edit
    :type shaderfx: str
    :param index: Index, The index to move the effect to
    :type index: int | None
    """

    ...

def shaderfx_move_up(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    shaderfx: str = "",
):
    """Move effect up in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param shaderfx: Shader, Name of the shaderfx to edit
    :type shaderfx: str
    """

    ...

def shaderfx_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    shaderfx: str = "",
    report: bool | None = False,
):
    """Remove a effect from the active grease pencil object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param shaderfx: Shader, Name of the shaderfx to edit
    :type shaderfx: str
    :param report: Report, Create a notification after the operation
    :type report: bool | None
    """

    ...

def shape_key_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    from_mix: bool | None = True,
):
    """Add shape key to the object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param from_mix: From Mix, Create the new shape key from the existing mix of keys
    :type from_mix: bool | None
    """

    ...

def shape_key_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Reset the weights of all shape keys to 0 or to the closest value respecting the limits

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def shape_key_lock(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    action: str | None = "LOCK",
):
    """Change the lock state of all shape keys of active object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param action: Action, Lock action to execute on vertex groups

    LOCK
    Lock -- Lock all shape keys.

    UNLOCK
    Unlock -- Unlock all shape keys.
        :type action: str | None
    """

    ...

def shape_key_mirror(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_topology: bool | None = False,
):
    """Mirror the current shape key along the local X axis

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_topology: Topology Mirror, Use topology based mirroring (for when both sides of mesh have matching, unique topology)
    :type use_topology: bool | None
    """

    ...

def shape_key_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "TOP",
):
    """Move the active shape key up/down in the list

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    TOP
    Top -- Top of the list.

    UP
    Up.

    DOWN
    Down.

    BOTTOM
    Bottom -- Bottom of the list.
        :type type: str | None
    """

    ...

def shape_key_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    all: bool | None = False,
    apply_mix: bool | None = False,
):
    """Remove shape key from the object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param all: All, Remove all shape keys
    :type all: bool | None
    :param apply_mix: Apply Mix, Apply current mix of shape keys to the geometry before removing them
    :type apply_mix: bool | None
    """

    ...

def shape_key_retime(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Resets the timing for absolute shape keys

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def shape_key_transfer(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: str | None = "OFFSET",
    use_clamp: bool | None = False,
):
    """Copy the active shape key of another selected object to this one

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Transformation Mode, Relative shape positions to the new shape method

    OFFSET
    Offset -- Apply the relative positional offset.

    RELATIVE_FACE
    Relative Face -- Calculate relative position (using faces).

    RELATIVE_EDGE
    Relative Edge -- Calculate relative position (using edges).
        :type mode: str | None
        :param use_clamp: Clamp Offset, Clamp the transformation to the distance each vertex moves in the original shape
        :type use_clamp: bool | None
    """

    ...

def simulation_nodes_cache_bake(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    selected: bool | None = False,
):
    """Bake simulations in geometry nodes modifiers

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param selected: Selected, Bake cache on all selected objects
    :type selected: bool | None
    """

    ...

def simulation_nodes_cache_calculate_to_frame(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    selected: bool | None = False,
):
    """Calculate simulations in geometry nodes modifiers from the start to current frame

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param selected: Selected, Calculate all selected objects instead of just the active object
    :type selected: bool | None
    """

    ...

def simulation_nodes_cache_delete(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    selected: bool | None = False,
):
    """Delete cached/baked simulations in geometry nodes modifiers

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param selected: Selected, Delete cache on all selected objects
    :type selected: bool | None
    """

    ...

def skin_armature_create(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Create an armature that parallels the skin layout

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def skin_loose_mark_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    action: str | None = "MARK",
):
    """Mark/clear selected vertices as loose

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param action: Action

    MARK
    Mark -- Mark selected vertices as loose.

    CLEAR
    Clear -- Set selected vertices as not loose.
        :type action: str | None
    """

    ...

def skin_radii_equalize(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Make skin radii of selected vertices equal on each axis

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def skin_root_mark(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Mark selected vertices as roots

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def speaker_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    enter_editmode: bool | None = False,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add a speaker object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def subdivision_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    level: int | None = 1,
    relative: bool | None = False,
):
    """Sets a Subdivision Surface level (1 to 5)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param level: Level
    :type level: int | None
    :param relative: Relative, Apply the subdivision surface level as an offset relative to the current level
    :type relative: bool | None
    """

    ...

def surfacedeform_bind(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Bind mesh to target in surface deform modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

    ...

def text_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add a text object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param radius: Radius
        :type radius: float | None
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def track_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "CLEAR",
):
    """Clear tracking constraint or flag from object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    """

    ...

def track_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "DAMPTRACK",
):
    """Make the object track another object, using various methods/constraints

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    """

    ...

def transfer_mode(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_flash_on_transfer: bool | None = True,
):
    """Switches the active object and assigns the same mode to a new one under the mouse cursor, leaving the active mode in the current one

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_flash_on_transfer: Flash On Transfer, Flash the target object when transferring the mode
    :type use_flash_on_transfer: bool | None
    """

    ...

def transform_apply(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    location: bool | None = True,
    rotation: bool | None = True,
    scale: bool | None = True,
    properties: bool | None = True,
    isolate_users: bool | None = False,
):
    """Apply the object's transformation to its data

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param location: Location
    :type location: bool | None
    :param rotation: Rotation
    :type rotation: bool | None
    :param scale: Scale
    :type scale: bool | None
    :param properties: Apply Properties, Modify properties such as curve vertex radius, font size and bone envelope
    :type properties: bool | None
    :param isolate_users: Isolate Multi User Data, Create new object-data users if needed
    :type isolate_users: bool | None
    """

    ...

def transform_axis_target(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Interactively point cameras and lights to a location (Ctrl translates)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def transform_to_mouse(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "",
    session_uid: int | None = 0,
    matrix: collections.abc.Sequence[collections.abc.Sequence[float]]
    | mathutils.Matrix
    | None = (
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
    ),
    drop_x: int | None = 0,
    drop_y: int | None = 0,
):
    """Snap selected item(s) to the mouse location

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Object name to place (uses the active object when this and 'session_uid' are unset)
    :type name: str
    :param session_uid: Session UUID, Session UUID of the object to place (uses the active object when this and 'name' are unset)
    :type session_uid: int | None
    :param matrix: Matrix
    :type matrix: collections.abc.Sequence[collections.abc.Sequence[float]] | mathutils.Matrix | None
    :param drop_x: Drop X, X-coordinate (screen space) to place the new object under
    :type drop_x: int | None
    :param drop_y: Drop Y, Y-coordinate (screen space) to place the new object under
    :type drop_y: int | None
    """

    ...

def transforms_to_deltas(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: str | None = "ALL",
    reset_values: bool | None = True,
):
    """Convert normal object transforms to delta transforms, any existing delta transforms will be included as well

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Mode, Which transforms to transfer

    ALL
    All Transforms -- Transfer location, rotation, and scale transforms.

    LOC
    Location -- Transfer location transforms only.

    ROT
    Rotation -- Transfer rotation transforms only.

    SCALE
    Scale -- Transfer scale transforms only.
        :type mode: str | None
        :param reset_values: Reset Values, Clear transform values after transferring to deltas
        :type reset_values: bool | None
    """

    ...

def unlink_data(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def vertex_group_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add a new vertex group to the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def vertex_group_assign(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Assign the selected vertices to the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def vertex_group_assign_new(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Assign the selected vertices to a new vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def vertex_group_clean(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    limit: float | None = 0.0,
    keep_single: bool | None = False,
):
    """Remove vertex group assignments which are not required

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of groups shall be used
    :type group_select_mode: str | None
    :param limit: Limit, Remove vertices which weight is below or equal to this limit
    :type limit: float | None
    :param keep_single: Keep Single, Keep verts assigned to at least one group when cleaning
    :type keep_single: bool | None
    """

    ...

def vertex_group_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Make a copy of the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def vertex_group_copy_to_selected(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Replace vertex groups of selected objects by vertex groups of active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def vertex_group_deselect(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Deselect all selected vertices assigned to the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def vertex_group_invert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    auto_assign: bool | None = True,
    auto_remove: bool | None = True,
):
    """Invert active vertex group's weights

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of groups shall be used
    :type group_select_mode: str | None
    :param auto_assign: Add Weights, Add vertices from groups that have zero weight before inverting
    :type auto_assign: bool | None
    :param auto_remove: Remove Weights, Remove vertices from groups that have zero weight after inverting
    :type auto_remove: bool | None
    """

    ...

def vertex_group_levels(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    offset: float | None = 0.0,
    gain: float | None = 1.0,
):
    """Add some offset and multiply with some gain the weights of the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of groups shall be used
    :type group_select_mode: str | None
    :param offset: Offset, Value to add to weights
    :type offset: float | None
    :param gain: Gain, Value to multiply weights by
    :type gain: float | None
    """

    ...

def vertex_group_limit_total(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    limit: int | None = 4,
):
    """Limit deform weights associated with a vertex to a specified number by removing lowest weights

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of groups shall be used
    :type group_select_mode: str | None
    :param limit: Limit, Maximum number of deform weights
    :type limit: int | None
    """

    ...

def vertex_group_lock(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    action: str | None = "TOGGLE",
    mask: str | None = "ALL",
):
    """Change the lock state of all or some vertex groups of active object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param action: Action, Lock action to execute on vertex groups

    TOGGLE
    Toggle -- Unlock all vertex groups if there is at least one locked group, lock all in other case.

    LOCK
    Lock -- Lock all vertex groups.

    UNLOCK
    Unlock -- Unlock all vertex groups.

    INVERT
    Invert -- Invert the lock state of all vertex groups.
        :type action: str | None
        :param mask: Mask, Apply the action based on vertex group selection

    ALL
    All -- Apply action to all vertex groups.

    SELECTED
    Selected -- Apply to selected vertex groups.

    UNSELECTED
    Unselected -- Apply to unselected vertex groups.

    INVERT_UNSELECTED
    Invert Unselected -- Apply the opposite of Lock/Unlock to unselected vertex groups.
        :type mask: str | None
    """

    ...

def vertex_group_mirror(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mirror_weights: bool | None = True,
    flip_group_names: bool | None = True,
    all_groups: bool | None = False,
    use_topology: bool | None = False,
):
    """Mirror vertex group, flip weights and/or names, editing only selected vertices, flipping when both sides are selected otherwise copy from unselected

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mirror_weights: Mirror Weights, Mirror weights
    :type mirror_weights: bool | None
    :param flip_group_names: Flip Group Names, Flip vertex group names
    :type flip_group_names: bool | None
    :param all_groups: All Groups, Mirror all vertex groups weights
    :type all_groups: bool | None
    :param use_topology: Topology Mirror, Use topology based mirroring (for when both sides of mesh have matching, unique topology)
    :type use_topology: bool | None
    """

    ...

def vertex_group_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    direction: str | None = "UP",
):
    """Move the active vertex group up/down in the list

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction, Direction to move the active vertex group towards
    :type direction: str | None
    """

    ...

def vertex_group_normalize(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Normalize weights of the active vertex group, so that the highest ones are now 1.0

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def vertex_group_normalize_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    lock_active: bool | None = True,
):
    """Normalize all weights of all vertex groups, so that for each vertex, the sum of all weights is 1.0

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of groups shall be used
    :type group_select_mode: str | None
    :param lock_active: Lock Active, Keep the values of the active group while normalizing others
    :type lock_active: bool | None
    """

    ...

def vertex_group_quantize(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    steps: int | None = 4,
):
    """Set weights to a fixed number of steps

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of groups shall be used
    :type group_select_mode: str | None
    :param steps: Steps, Number of steps between 0 and 1
    :type steps: int | None
    """

    ...

def vertex_group_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    all: bool | None = False,
    all_unlocked: bool | None = False,
):
    """Delete the active or all vertex groups from the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param all: All, Remove all vertex groups
    :type all: bool | None
    :param all_unlocked: All Unlocked, Remove all unlocked vertex groups
    :type all_unlocked: bool | None
    """

    ...

def vertex_group_remove_from(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_all_groups: bool | None = False,
    use_all_verts: bool | None = False,
):
    """Remove the selected vertices from active or all vertex group(s)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_all_groups: All Groups, Remove from all groups
    :type use_all_groups: bool | None
    :param use_all_verts: All Vertices, Clear the active group
    :type use_all_verts: bool | None
    """

    ...

def vertex_group_select(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Select all the vertices assigned to the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def vertex_group_set_active(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group: str | None = "",
):
    """Set the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group: Group, Vertex group to set as active
    :type group: str | None
    """

    ...

def vertex_group_smooth(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    factor: float | None = 0.5,
    repeat: int | None = 1,
    expand: float | None = 0.0,
):
    """Smooth weights for selected vertices

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of groups shall be used
    :type group_select_mode: str | None
    :param factor: Factor
    :type factor: float | None
    :param repeat: Iterations
    :type repeat: int | None
    :param expand: Expand/Contract, Expand/contract weights
    :type expand: float | None
    """

    ...

def vertex_group_sort(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    sort_type: str | None = "NAME",
):
    """Sort vertex groups

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param sort_type: Sort Type, Sort type
    :type sort_type: str | None
    """

    ...

def vertex_parent_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Parent selected objects to the selected vertices

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def vertex_weight_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy weights from active to selected

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def vertex_weight_delete(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    weight_group: int | None = -1,
):
    """Delete this weight from the vertex (disabled if vertex group is locked)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param weight_group: Weight Index, Index of source weight in active vertex group
    :type weight_group: int | None
    """

    ...

def vertex_weight_normalize_active_vertex(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Normalize active vertex's weights

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def vertex_weight_paste(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    weight_group: int | None = -1,
):
    """Copy this group's weight to other selected vertices (disabled if vertex group is locked)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param weight_group: Weight Index, Index of source weight in active vertex group
    :type weight_group: int | None
    """

    ...

def vertex_weight_set_active(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    weight_group: int | None = -1,
):
    """Set as active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param weight_group: Weight Index, Index of source weight in active vertex group
    :type weight_group: int | None
    """

    ...

def visual_transform_apply(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Apply the object's visual transformation to its data

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def volume_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Add a volume object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def volume_import(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    directory: str = "",
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    hide_props_region: bool | None = True,
    check_existing: bool | None = False,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_obj: bool | None = False,
    filter_volume: bool | None = True,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 9,
    relative_path: bool | None = True,
    display_type: str | None = "DEFAULT",
    sort_method: str | None = "",
    use_sequence_detection: bool | None = True,
    align: str | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
):
    """Import OpenVDB volume file

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param directory: Directory, Directory of the file
        :type directory: str
        :param files: Files
        :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] | None
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | None
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter Python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_obj: Filter OBJ files
        :type filter_obj: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: bool | None
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: str | None
        :param sort_method: File sorting mode
        :type sort_method: str | None
        :param use_sequence_detection: Detect Sequences, Automatically detect animated sequences in selected volume files (based on file names)
        :type use_sequence_detection: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

    ...

def voxel_remesh(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Calculates a new manifold mesh based on the volume of the current mesh. All data layers will be lost

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def voxel_size_edit(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Modify the mesh voxel size interactively used in the voxel remesher

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...
