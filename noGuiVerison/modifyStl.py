import bpy
import os
import time
from pathlib import Path

# Specify the directory path
directory_path = "/Users/harryhicks/Downloads/allarus/"

# Recursively get a list of all .stl files
stl_files = [str(f) for f in Path(directory_path).rglob("*.stl")]

for stl in stl_files:
    # Clear all mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    print("Processing file: ", stl, flush=True)

    # Import STL file
    start_time = time.time()
    bpy.ops.wm.stl_import(filepath=os.path.join(directory_path, stl))
    print("Time to import: ", time.time() - start_time, "seconds", flush=True)

    # Get the current object
    obj = bpy.context.active_object

    print("Denoising the surface - Laplacian Smooth...", flush=True)
    start_time = time.time()
    # Denoise the surface using Laplacian Smooth
    bpy.ops.object.modifier_add(type='LAPLACIANSMOOTH')
    obj.modifiers["LaplacianSmooth"].lambda_factor = 0.1
    bpy.ops.object.modifier_apply(modifier="LaplacianSmooth")
    print("Time for Laplacian Smooth denoising: ", time.time() - start_time, "seconds", flush=True)

   
    print("Making edges crisp...", flush=True)
    start_time = time.time()
    # Make edges more crisp
    bpy.ops.object.modifier_add(type='BEVEL')
    obj.modifiers["Bevel"].width = 0.01
    bpy.ops.object.modifier_apply(modifier="Bevel")
    print("Time for making edges crisp: ", time.time() - start_time, "seconds", flush=True)

    print("Cleaning up the mesh...", flush=True)
    start_time = time.time()
    # Clean up the mesh
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.fill_holes()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    print("Time for cleaning up the mesh: ", time.time() - start_time, "seconds", flush=True)

    print("Applying final decimation...", flush=True)
    start_time = time.time() 
    # Decimate the model to 50k polygons
    final_decimate_ratio = 150000 / len(obj.data.polygons)
    bpy.ops.object.modifier_add(type='DECIMATE')
    obj.modifiers["Decimate"].ratio = final_decimate_ratio
    bpy.ops.object.modifier_apply(modifier="Decimate")
    print("Time for final decimation: ", time.time() - start_time, "seconds", flush=True)

    print("Exporting the processed STL...", flush=True)
    start_time = time.time()
    # Export the processed STL
    bpy.ops.wm.stl_export(filepath=os.path.join(directory_path, ((stl.rsplit(" ", 1)[0]) +".stl") if stl.lower().endswith(" v2.stl") else stl))
    print("Time for exporting: ", time.time() - start_time, "seconds", flush=True)

    print("Done processing ", stl, "\n", flush=True)
