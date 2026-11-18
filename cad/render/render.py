import bpy, math, sys, json, os
from mathutils import Vector

# args: json config path
# Usage:  blender -b -P cad/render/render.py -- cad/render/jobs/hero.json   (run from project root)
#    or:  python3 cad/render/render.py -- cad/render/jobs/hero.json         (with `pip install bpy`)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
cfg = json.load(open(sys.argv[-1]))
R = lambda p: p if os.path.isabs(p) else os.path.join(ROOT, p)
BODY = R('cad/stl/body.stl'); BEZEL = R('cad/stl/bezel.stl'); BACK = R('cad/stl/back_plate.stl')

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def hexrgb(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return [((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c] + [1]

def imp(path, name):
    bpy.ops.wm.stl_import(filepath=path)
    o = bpy.context.selected_objects[0]; o.name = name
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    return o

def pla(name, hexc, rough=0.45, matte=False):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexrgb(hexc)
    b.inputs['Roughness'].default_value = 0.7 if matte else rough
    b.inputs['Specular IOR Level'].default_value = 0.35 if matte else 0.5
    # subtle layer lines: bump from a wave texture along Z
    nt = m.node_tree
    if cfg.get('layers', True):
        tc = nt.nodes.new('ShaderNodeTexCoord'); wv = nt.nodes.new('ShaderNodeTexWave')
        wv.wave_type = 'BANDS'; wv.bands_direction = 'Z'; wv.inputs['Scale'].default_value = cfg.get('layer_scale', 70)
        bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.04
        nt.links.new(tc.outputs['Object'], wv.inputs['Vector']); nt.links.new(wv.outputs['Color'], bp.inputs['Height'])
        nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m

S = 0.01  # mm -> scene units
body = imp(BODY, 'body'); bezel = imp(BEZEL, 'bezel'); back = imp(BACK, 'back')
for o in (body, bezel, back):
    o.scale = (S, S, S); o.location = (0, 0, 0)
# body: front faces +Z in CAD; rotate so front faces -Y, up stays up
from mathutils import Matrix
def place(o, q):
    """Explicit placement from assembly_tool.html: mirror(local XYZ) -> spin(local Z) -> Euler XYZ -> position (mm)."""
    m = q.get('mirror', [0, 0, 0])
    if any(m):
        o.data.transform(Matrix.Diagonal([-1 if v else 1 for v in m] + [1]))
        if sum(1 for v in m if v) % 2: o.data.flip_normals()
    o.data.transform(Matrix.Rotation(math.radians(q.get('spin', 0)), 4, 'Z'))
    o.rotation_mode = 'ZYX'  # three.js 'XYZ' (assembly_tool.html) == Blender 'ZYX' with the same x,y,z angles
    o.rotation_euler = [math.radians(a) for a in q['rot']]
    o.location = [v * S for v in q['pos']]

D = 40.64 * S
win_y = cfg.get('win_y', 3.0) * S  # window centre in CAD: x 0, y ~ -3 mm
if cfg.get('parts'):
    for o, k in ((body, 'body'), (bezel, 'bezel'), (back, 'back')): place(o, cfg['parts'][k])
    if cfg.get('explode'):
        e = cfg['explode']  # optional per-part distances: explode_bezel / explode_back
        bezel.location.y -= cfg.get('explode_bezel', e) * S; back.location.y += cfg.get('explode_back', e) * S
else:
    body.rotation_euler = (math.radians(90), math.radians(180), 0)
    bz = body.dimensions  # after scale, before rotation dims are local
    bezel.rotation_euler = (math.radians(90), math.radians(180), math.radians(cfg.get('bezel_rot', 0)))
    bezel.location = (0, -D / 2 + cfg.get('bezel_inset', 2.0) * S, win_y)
    back.data.transform(Matrix.Rotation(math.radians(cfg.get('back_rot', 90)), 4, 'Z'))
    if cfg.get('back_mirror'):  # mirror left/right (local X), port stays at the bottom
        back.data.transform(Matrix.Scale(-1, 4, (1, 0, 0))); back.data.flip_normals()
    back.rotation_euler = (math.radians(90), math.radians(180), 0)
    back.location = (0, D / 2 + 2 * S + cfg.get('back_gap', 0) * S, cfg.get('back_y', 0) * S)
    if cfg.get('explode'):
        e = cfg['explode']
        bezel.location.y -= e * S; back.location.y += e * S


body.data.materials.append(pla('body', cfg['body'], matte=cfg.get('matte', True)))
bezel.data.materials.append(pla('bezel', cfg['bezel'], matte=cfg.get('matte', True)))
back.data.materials.append(pla('back', cfg['back'], matte=cfg.get('matte', True)))
for o in (body, bezel, back):
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
if cfg.get('subd', 1):
    md = body.modifiers.new('sub', 'SUBSURF'); md.levels = md.render_levels = cfg.get('subd', 1)
    body.data.polygons.foreach_set('use_smooth', [True] * len(body.data.polygons))

# screen: emissive plane with face bitmap, behind the bezel
if cfg.get('face'):
    bpy.ops.mesh.primitive_plane_add(size=1)
    scr = bpy.context.active_object; scr.name = 'screen'
    sw, sh = cfg.get('screen_w', 30), cfg.get('screen_h', 15)
    scr.scale = (sw * S, sh * S, 1)
    scr.rotation_euler = (math.radians(90), 0, 0)
    scr.location = (cfg.get('screen_x', 0) * S, -D / 2 + cfg.get('screen_depth', 4) * S, win_y + cfg.get('screen_dy', 0) * S)
    m = bpy.data.materials.new('screen'); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL': nt.nodes.remove(n)
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(R(cfg['face'])); tex.interpolation = 'Closest'
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = cfg.get('glow', 3.0)
    mix = nt.nodes.new('ShaderNodeMixShader'); bs = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bs.inputs['Base Color'].default_value = (0.005, 0.005, 0.006, 1); bs.inputs['Roughness'].default_value = 0.12
    nt.links.new(tex.outputs['Color'], em.inputs['Color'])
    add = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(em.outputs[0], add.inputs[0]); nt.links.new(bs.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], nt.nodes['Material Output'].inputs[0])
    scr.data.materials.append(m)

# world + lights
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = hexrgb(cfg.get('bg', '#282020'))
w.node_tree.nodes['Background'].inputs['Strength'].default_value = cfg.get('world', 0.35)

def area(name, loc, size, energy, color='#FFF4E8'):
    bpy.ops.object.light_add(type='AREA', location=loc)
    l = bpy.context.active_object; l.data.size = size; l.data.energy = energy; l.data.color = hexrgb(color)[:3]
    d = Vector((0, 0, 0)) - l.location; l.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return l
area('key', (-1.2, -1.6, 1.4), 1.2, cfg.get('key', 60))
area('fill', (1.6, -1.2, 0.4), 1.5, cfg.get('fill', 18))
area('rim', (0.9, 1.4, 1.2), 0.6, cfg.get('rim', 20), cfg.get('rim_color', '#2F9083'))
area('top', (0, 0, 2), 1.0, 15)

# floor (shadow catcher or coloured)
if cfg.get('floor', True):
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -0.375 - 0.002))
    fl = bpy.context.active_object
    fm = bpy.data.materials.new('floor'); fm.use_nodes = True
    fm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = hexrgb(cfg.get('bg', '#282020'))
    fm.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.9
    fl.data.materials.append(fm)
    if cfg.get('transparent'): fl.is_shadow_catcher = True

# camera
cam_d = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam_d.lens = cfg.get('lens', 85)
az, el, dist = math.radians(cfg.get('az', 0)), math.radians(cfg.get('el', 8)), cfg.get('dist', 3.2)
tgt = Vector(cfg.get('target', (0, 0, 0)))
cam.location = tgt + Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el))) * dist
cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()

sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = cfg.get('samples', 64); sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = cfg.get('res', (1200, 1200))
sc.render.film_transparent = bool(cfg.get('transparent'))
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.filepath = R(cfg['out'])
if cfg.get('gpu', True):
    try:
        pr = bpy.context.preferences.addons['cycles'].preferences
        for t in ('METAL', 'OPTIX', 'CUDA'):
            try:
                pr.compute_device_type = t; pr.get_devices()
                if any(d.type == t for d in pr.devices):
                    for d in pr.devices: d.use = True
                    sc.cycles.device = 'GPU'; break
            except Exception: pass
    except Exception: pass
if cfg.get('face'):
    from bpy_extras.object_utils import world_to_camera_view
    bpy.context.view_layer.update()
    pts=[world_to_camera_view(sc, cam, scr.matrix_world @ v.co) for v in scr.data.vertices]
    rx,ry=sc.render.resolution_x,sc.render.resolution_y
    print('SCREENRECT', [(round(p.x*rx,1), round((1-p.y)*ry,1)) for p in pts])
if not cfg.get('norender'):
    bpy.ops.render.render(write_still=True)
print('WROTE', cfg['out'])
