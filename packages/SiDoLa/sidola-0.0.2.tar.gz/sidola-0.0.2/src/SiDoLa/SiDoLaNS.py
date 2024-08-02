import io
import os
#os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True' # This may be useful
import torch
import copy
from ultralytics import YOLO
from ultralytics.data.augment import LetterBox
from ultralytics.utils.plotting import Annotator, colors, save_one_box
from copy import deepcopy
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import pandas as pd
import ast
from IPython.display import clear_output
import socket
import time
from collections import defaultdict
import types
from datetime import datetime
import shutil
from random import randint
import random
import re
import colorsys
import math
import json
from scipy.spatial import Voronoi
import matplotlib.path as mpltPath
import matplotlib.pyplot as plt

# Functions

def sanitize_for_filesystem(input_string, len = 6):
    safe_string = re.sub(r'[^a-zA-Z0-9]', '', input_string)
    return safe_string[:len]

def yoloName_fromPath(path):
    parts = path.split(os.sep)
    if 'weights' in parts:
        index = parts.index('weights')
        if index > 0: return parts[index-1]
    return "UNK"

def save_tile_results(res2, save_path, max_tile_cols = 6, divider_width = 4, drawMode = 4, show=False): #DrawMode 0=Boxes Only, 1=MaskClass, 2=MaskInstance, 3=BoxInstance, 4=Box/Mask by Class
    divider_color = (255, 0, 0)  # Red divider color
    drawBoxes_byClass = drawMode==0 or drawMode==4
    drawMasks_byClass = drawMode==1 or drawMode==4 or drawMode==2
    drawMasks_byInstance = drawMode==2

    def calculate_canvas_size(images, max_cols, img_width, img_height, divider_width):
        canvas_width = (img_width + divider_width) * min(len(images), max_cols) - divider_width
        canvas_height = (img_height * 2 + divider_width) 
        return canvas_width, canvas_height

    def draw_polygons(draw, polygons):
        for i, polygon in enumerate(polygons):
            color = get_color_by_id(i, len(polygons))
            draw.polygon(polygon, fill=color, outline='white')

    image_pairs = []

    for result in res2:
        img_orig = result.orig_img
        img_labeled = result.plot(labels=False, conf=False, boxes=drawBoxes_byClass, masks=drawMasks_byClass)
        img_orig_pil = Image.fromarray(img_orig)
        img_labeled_pil = Image.fromarray(img_labeled)

        if (drawMasks_byInstance):
            polygons = result.masks.xy
            #print(result.path, len(result), len(result.masks), len(result.masks.xy))
            draw_orig = ImageDraw.Draw(img_orig_pil); draw_polygons(draw_orig, polygons)          # Draw polygons on original imag
            #draw_labeled = ImageDraw.Draw(img_labeled_pil); draw_polygons(draw_labeled, polygons)  # Draw polygons on labeled image
        
        image_pairs.append((img_orig_pil, img_labeled_pil))

    if not image_pairs:
        print("No images to display.")
    else:
        img_width, img_height = image_pairs[0][0].size
        canvas_width, canvas_height = calculate_canvas_size(image_pairs, max_tile_cols, img_width, img_height, divider_width)
        canvas = Image.new('RGB', (canvas_width, canvas_height), "white")
        draw = ImageDraw.Draw(canvas)

        for i, (img_orig, img_labeled) in enumerate(image_pairs[:max_tile_cols]):
            col = i % max_tile_cols; row = i // max_tile_cols
            top_left_x = col * (img_width + divider_width); top_left_y = row * (img_height * 2 + divider_width)
            canvas.paste(img_orig, (top_left_x, top_left_y))
            canvas.paste(img_labeled, (top_left_x, top_left_y + img_height + divider_width))

        if show:
            display(canvas)
        if save_path:
            canvas.save(save_path)

def results_toDF(res2, addIDCol = False):
    data = []
    for result in res2:
        boxes = result.boxes
        inst = 0
        for box in boxes:
            x, y, w, h = box.xywh[0].tolist()
            inst += 1
            data.append({
                'Fullpath': result.path,
                'Filename' : os.path.basename(result.path),
                'Instance' : inst,
                'Class': box.cls[0].item(),
                'Conf': box.conf[0].item(),
                'x': x, 'y': y,
                'w': w, 'h': h,
                'xc' : x + w/2,
                'yc' : y + h/2,
                'Circ Area' : (0.858 * w * h)
            })
    df = pd.DataFrame(data)
    if (addIDCol): 
        df['ID'] = df.groupby('path').cumcount()
    return df

def results_toCSV(res2, save_path):
    df = results_toDF(res2)
    df.to_csv(save_path, index=False)

def polygon_area(coords):
    x = coords[:, 0]; y = coords[:, 1]
    i = np.arange(len(x))
    # 'shoelace' formula
    # return 0.5*np.abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
    return np.abs(np.sum(x[i-1]*y[i]-x[i]*y[i-1])*0.5)

def find_parents(classes, image):
    class0_indices = np.where(classes == 0)[0]
    class1_indices = np.where(classes == 1)[0]
    
    class1_centers = image.boxes.xywh[class1_indices]
    class0_centers = image.boxes.xywh[class0_indices]
    
    class1_parents = []
    for class1_coord in class1_centers.numpy():
                # print("the class1 instance: ", class1_coord)
                
                droplet_x = class1_coord[0]
                droplet_y = class1_coord[1]
                # print("droplet x, y coords: ", droplet_x, droplet_y)
                min_distance_from_cells = math.inf
                parent_cell_index = 0
                for i, class0_coord in enumerate(class0_centers.numpy()):
                    # print("the class0 instance: ", class0_coord)
                    
                    cell_x = class0_coord[0]
                    cell_y = class0_coord[1]
                    # print("cell x, y coords: ", cell_x, cell_y)
                    point1 = np.array((droplet_x, droplet_y))
                    point2 = np.array((cell_x, cell_y))
                    dist = np.linalg.norm(point1 - point2)
                    # print("dist from class0 instance: ", dist)
                    if dist < min_distance_from_cells:
                        min_distance_from_cells = dist
                        parent_cell_index = i
                        
                # print("parent cell index: ", parent_cell_index)        
                class1_parents.append(class0_indices[parent_cell_index])
    return class1_parents

def find_first_file(m_folder, m_contains):
    for root, dirs, files in os.walk(m_folder):
        for file in files:
            if m_contains in file:
                return os.path.join(root, file)
    return None

cPredImgFldr = "_PredImgs"
def create_multichannel_array(folder_path, down_x = 1, down_y = 1):
    image_arrays = []
    image_names = []
    for root, dirs, files in os.walk(folder_path):
        if (os.path.basename(root) == cPredImgFldr): continue
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg','.bmp','.tif')):
                print("loading ", file)
                file_path = os.path.join(root, file)
                #t_img = Image.open(file_path).convert('L');  # Convert to grayscale if not already # Old Way
                
                t_img = Image.open(file_path); 
                width, height = t_img.size  
                new_width = int(width * down_x); new_height = int(height * down_y)
                t_img = t_img.resize((new_width, new_height), Image.Resampling.BILINEAR) # Resize the image

                t_arr = np.array(t_img) 
                #max_intensity = np.max(t_arr); 
                #img_8bit = (255.0 * img_array / max_intensity).astype('uint8')
                #img = Image.fromarray(img_8bit).convert('RGB'); width, height = img.size
                
                if t_arr.ndim == 2:  # Ensure the image is grayscale
                    image_arrays.append(t_arr)
                    image_names.append(file)
    
    if not image_arrays:
        return None  # Or raise an exception if you prefer

    # Stack the arrays along a new axis to create a multi-channel array
    multi_channel_array = np.stack(image_arrays, axis=-1)
    return multi_channel_array, image_names

def get_color_by_id(point_region_id, total_ids):
    hue = point_region_id / total_ids # Scale the hue by the number of unique IDs, wrapping around the hue circle
    saturation = 0.9; value = 0.9  # Keep saturation and value high for bright colors
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    return tuple(int(c * 255) for c in rgb) # Convert to 0-255 scale for RGB colors in PIL

def get_vor_boundaries(boxes, ImgIfDesired = None):
    points= []; vor_verts = {}
    for idx in range(len(boxes)): points.append((boxes[idx][0], boxes[idx][1]))
    vor_verts_list = []
    try:
        vor = Voronoi(points)
    except:
        return vor_verts_list
    for point_region_id, region_id in enumerate(vor.point_region): #this is needed to preserve the order
        if (-1 not in vor.regions[region_id]):
            region_vertices = vor.vertices[vor.regions[region_id]]
            vor_verts[point_region_id] = region_vertices.tolist()

    default_triangle_height = 2; default_triangle_base_length = 4
    for idx, point in enumerate(points):
        if idx in vor_verts:  # Voronoi region exists
            vor_verts_list.append(vor_verts[idx])
        else:  # Create default triangle for missing regions
            bl_vertex = (point[0] - default_triangle_base_length / 2, point[1])
            br_vertex = (point[0] + default_triangle_base_length / 2, point[1])
            top_vertex = (point[0], point[1] + default_triangle_height)  
            vor_verts_list.append([bl_vertex, br_vertex, top_vertex])
    
    if (ImgIfDesired):
        drawV = ImageDraw.Draw(ImgIfDesired)
        r = 2  # radius of the points
        for point_region_id, point in enumerate(points):
            outline_color = get_color_by_id(point_region_id, len(points))
            left_up_point = (point[0] - r, point[1] - r)
            right_down_point = (point[0] + r, point[1] + r)
            if vor_verts.get(point_region_id) and len(vor_verts[point_region_id]) > 0:
                polygon_vertices_tuples = [tuple(vertex) for vertex in vor_verts[point_region_id]]
                drawV.polygon(polygon_vertices_tuples, width=3, outline=outline_color)
            drawV.ellipse([left_up_point, right_down_point], fill=outline_color)

        display(imgV)
    return vor_verts_list

def major_minor_axis_lengths(polygon_coords):
    """
    Calculate the major and minor axis lengths of a polygon.
    :param polygon_coords: An array of shape (N, 2) representing the polygon vertices.
    """
    polygon_coords = np.array(polygon_coords) # Convert to numpy array if not already
    centroid = np.mean(polygon_coords, axis=0)
    centered_coords = polygon_coords - centroid
    cov_matrix = np.cov(centered_coords, rowvar=False) # Compute the covariance matrix of the centered coordinates
    eigenvalues, _ = np.linalg.eigh(cov_matrix) # Get the eigenvalues of the covariance matrix
    major_axis_length = 2 * np.sqrt(eigenvalues[1]) # Eigenvalues are the variances along the principal axes
    minor_axis_length = 2 * np.sqrt(eigenvalues[0])
    return major_axis_length, minor_axis_length

def create_instance_mask(image_width, image_height, yolo_results_data, show_test_mask = False):
    """
    Create a mask where each pixel value represents the instance class.

    :param image_shape: A tuple (height, width) representing the image shape.
    :param masks: The masks from the YOLOv8 results.
    :param classes: The classes of each instance.
    :return: A mask array where each pixel value represents the instance class. First channel is class, 2nd is confidence, 3rd is 0
    """
    boxes = yolo_results_data.boxes.cpu()
    masks = yolo_results_data.masks.cpu()
    classes_conf = [(boxes[idx].cls.item(),boxes[idx].conf.item()) for idx in range(len(boxes))]
    instance_mask = np.zeros((image_width, image_height, 3), dtype=float) # dtype=np.int32)

    for idx in range(len(boxes)):
        poly_cors = masks[idx].xy[0]
        path = mpltPath.Path(poly_cors)
        y, x = np.mgrid[:image_width, :image_height]
        points = np.vstack((x.ravel(), y.ravel())).T
        mask = path.contains_points(points)
        mask = mask.reshape((image_width, image_height))
        instance_mask[mask, 0] = classes_conf[idx][0] # Class
        instance_mask[mask, 1] = classes_conf[idx][1] # Confidence
        instance_mask[mask, 2] = idx                  # Instance ID
    if (show_test_mask):
        plt.figure()
        plt.imshow(instance_mask, cmap='gray')
        plt.title('Mask')
        plt.show()
    return instance_mask

def soft_voting_ensemble(arrays):
    image_width, image_height, _ = arrays[0].shape
    temp_dict = np.full((image_width, image_height), None, dtype=object)
    for x in range(image_width):
        for y in range(image_height):
            temp_dict[x, y] = defaultdict(float)
    for array in arrays:
        for x in range(image_width):
            for y in range(image_height):
                class_id = int(array[x, y, 0])
                confidence = array[x, y, 1]
                temp_dict[x, y][class_id] += confidence
    
    ensemble_result = np.zeros((image_width, image_height, 2), dtype=float)
    for x in range(image_width):
        for y in range(image_height):
            if temp_dict[x, y]:
                class_confidences = temp_dict[x, y]
                max_class = max(class_confidences, key=class_confidences.get)
                max_confidence = class_confidences[max_class]
                ensemble_result[x, y, 0] = max_class
                ensemble_result[x, y, 1] = max_confidence
    return ensemble_result

def create_transcript_dict(transcript_info, micro_down_x=1, micro_down_y=1, chunk_size=200000):
    def process_chunk_old(chunk, trans_mask, ti, micro_down_x, micro_down_y):
        for index, row in chunk.iterrows():
            key = (round(row[ti.col_x] * micro_down_x), round(row[ti.col_y] * micro_down_y))
            gene = row[ti.col_gene]
            count = row[ti.col_count]

            if key not in trans_mask:
                trans_mask[key] = {}
            if gene not in trans_mask[key]:
                trans_mask[key][gene] = 0
            trans_mask[key][gene] += count

    def process_chunk_new(chunk, trans_mask, ti, micro_down_x, micro_down_y):
        chunk['key'] = list(zip(
            (chunk[ti.col_x] * micro_down_x).round().astype(int),
            (chunk[ti.col_y] * micro_down_y).round().astype(int)
        ))
        
        grouped = chunk.groupby(['key', ti.col_gene])[ti.col_count].sum().reset_index()
        
        for _, row in grouped.iterrows():
            key = row['key']
            gene = row[ti.col_gene]
            count = row[ti.col_count]

            if key not in trans_mask:
                trans_mask[key] = {}
            if gene not in trans_mask[key]:
                trans_mask[key][gene] = 0
            trans_mask[key][gene] += count

    ti = transcript_info
    trans_mask = {}
    processed_rows = 0
    chunk_idx = 0

    for chunk in pd.read_csv(ti.path, chunksize=chunk_size):
        processed_rows += len(chunk)
        chunk_idx += 1

        if chunk_idx % 2 == 1:
            start_time = time.time()
            process_chunk_old(chunk, trans_mask, ti, micro_down_x, micro_down_y)
            old_method_time = time.time() - start_time
            print(f"Chunk {chunk_idx} (old method): {old_method_time:.2f} seconds")
        else:
            start_time = time.time()
            process_chunk_new(chunk, trans_mask, ti, micro_down_x, micro_down_y)
            new_method_time = time.time() - start_time
            print(f"Chunk {chunk_idx} (new method): {new_method_time:.2f} seconds")

    return trans_mask
  
def find_mask_intensities(img_data, image_array, file_name, fraction_complete = 0,shift_x = 0, shift_y = 0, full_width = -1, full_height = -1, include_headers = True, meta_name = "NA", tile_name = "NA", max_bb_area = 99999, macro_model_list = []):
    sto = io.StringIO()
    sth = ''; d = '\t'

    def bstr_h(sth1):
        nonlocal sth
        sth += sth1

    def bstr_m(st1):
        sto.write(st1)

    def bstr_m_start():
        nonlocal sth, sto
        st = sth + '\r' + sto.getvalue()
        sto.close()
        sto = io.StringIO()
        sto.write(st)

    def get_mask(vertices):
        try:
            polygon_path = mpltPath.Path(vertices) # Create a path object from the vertices
            inside_polygon = polygon_path.contains_points(class_points)
            mask = inside_polygon.reshape(xx.shape) # Reshape the mask back to the image shape
            return mask
        except:
            return None

    width =image_array.shape[1]; height = image_array.shape[0]; channels = image_array.shape[2]
    boxes = img_data.boxes.cpu()
    img_box_centers = boxes.xywh 
    img_mask_coords = None if img_data.masks is None else img_data.masks.xy
    img_vor_coords = get_vor_boundaries(img_box_centers)

    # Now we want to see if the mask contains anything in teh macro model

    first = include_headers; masks = {}
    print(f"{fraction_complete:.1%}"," > width =",width,"height =",height,"chs =",channels,"boxes =",len(img_box_centers),"vor =",len(img_vor_coords))
    xx, yy = np.meshgrid(np.arange(width),np.arange(height)) # Create a mesh grid of coordinate values
    x_flat = xx.flatten(); y_flat = yy.flatten()
    class_points = np.vstack((x_flat, y_flat)).T # Create a list of (x, y) points from the flattened grid
    for idx in range(len(img_box_centers)):
        if (idx % 500 == 499): print("Measuring Intensities",idx)
        bbox_xywh = img_box_centers[idx]
        bbox_corners = [[bbox_xywh[0] - bbox_xywh[2], bbox_xywh[1] + bbox_xywh[3]],[bbox_xywh[0] + bbox_xywh[2], bbox_xywh[1] + bbox_xywh[3]] ,[bbox_xywh[0] + bbox_xywh[2], bbox_xywh[1] - bbox_xywh[3]], [bbox_xywh[0] - bbox_xywh[2], bbox_xywh[1] - bbox_xywh[3]]]
        vor_corners = img_vor_coords[idx] if img_vor_coords else None
        polys = { "box": bbox_corners, "poly": img_mask_coords,  **({"vor": vor_corners} if vor_corners else {}) }
        masks = {key: get_mask(value) for key, value in polys.items() if value}

        cx = bbox_xywh[0].item() + shift_x; cy = bbox_xywh[1].item() + shift_y; cw = bbox_xywh[2].item(); ch = bbox_xywh[3].item()
        #'FileName' + d +  #Took this out 7/22 takes up a lot of space 
        #file_name + d + 
        if (first): bstr_h('MetaName' + d + 'TileName' + d + 'Micro ObjectID' + d + 'Micro Class'              + d + 'Micro Confidence'          + d + 'cx'    + d + 'cy'    + d)
        bstr_m(             meta_name  + d +  tile_name + d + str(idx)   + d + str(int(boxes[idx].cls.item())) + d + str(boxes[idx].conf.item()) + d + str(cx) + d + str(cy) + d)  #I just added the +d at the end on 6/18/2024

        bestConf = -1; bestClass = -1; bestLabel = "" #For Ensemble
        soft_voting = None; labelList = None
        for ma in macro_model_list:
            if (ma.type == "macro"):
                if soft_voting is None: soft_voting = {}
                ry = int(ma.dim_x * cx / full_width); rx = int(ma.dim_y * cy / full_height)
                name = ma.name[:10]
                mac_cls, mac_conf, mac_ins = int(ma.instance_mask[rx,ry,0]), ma.instance_mask[rx,ry,1], ma.instance_mask[rx,ry,2]
                if mac_cls not in soft_voting: soft_voting[mac_cls] = 0
                soft_voting[mac_cls] += mac_conf
                if labelList is None: labelList = ma.model.names
                if (mac_conf > bestConf): 
                    bestConf = mac_conf; bestClass = mac_cls; bestLabel = ma.model.names[bestClass]
                if (first): bstr_h(name + " Class" + d + name + " Confidence" + d + name + " ID" + d)
                bstr_m(          str(     mac_cls) + d +        str(mac_conf) + d + str(mac_ins) + d)
            elif (ma.type == "transcripts"):
                half_cw = int(cw/2); half_ch = int(ch/2); assembled_gene_dict = {}
                for dx in range(-half_cw, half_cw):
                    for dy in range(-half_ch, half_ch):
                        if ma.downsample_match_micro_Down:
                            rx = round(full_width * (cx + dx) / full_width); ry = round(full_height * (cy + dy) / full_height)
                        else:
                            rx = round(ma.full_width * (cx + dx) / full_width); ry = round(ma.full_height * (cy + dy) / full_height)
                        key = (rx, ry)
                        if key in ma.transcript_dict:
                            gene_dict = ma.transcript_dict[key]
                            for gene, count in gene_dict.items():
                                if gene not in assembled_gene_dict: assembled_gene_dict[gene] = 0
                                assembled_gene_dict[gene] += count
                if (first): bstr_h("Gene Dict"  + d)
                bstr_m(str(assembled_gene_dict) + d)
        if soft_voting:
            sv_key = max(soft_voting, key=soft_voting.get)
            if (first): bstr_h("HV Ensemble Class" + d + "HV Ensemble Confidence" + d + "HV Ensemble Label" + d + "SV Ensemble Class" + d + "SV Ensemble Confidence" + d + "SV Ensemble Label" + d) 
            bstr_m(         str(int(bestClass)) + d +    str(bestConf)      + d + bestLabel                 + d + str(int(sv_key)) + d +    str(soft_voting[sv_key])      + d + labelList[sv_key] + d)

        for c in range(channels): # Look at each mask for each channel
            cs = str(c)
            for key in masks:
                mask = masks[key]
                if mask is not None and mask.any():
                    selected_pixels = image_array[:, :, c][mask]
                    area = len(selected_pixels)
                else: area = "NaN"
                #TODO: Add in Major Minor (maj, min) = major_minor_axis_lengths(?,?) # Probably only for the polygon masks
                if (first and c==0): bstr_h(key + ' AreaP' + d)
                if (c==0): bstr_m(               str(area) + d)

                if mask is not None and mask.any():
                    sum = np.sum(selected_pixels)
                    avg = np.average(selected_pixels)
                    std = np.std(selected_pixels)
                else: sum = avg = std = "NaN"
                if (first): bstr_h(key + ' Total Intensity wv' + cs + d + key + ' Avg Intensity wv' + cs + d + key + ' Std Intensity wv' + cs + d)
                bstr_m(                    str(sum)                 + d + str(avg)                       + d + str(std)                       + d)

        if (first): bstr_m_start(); first = False
        bstr_m('\r')
    return sto.getvalue()

def Predict_OnPartsOfImage(micro_model, original_image_name, full_image_arr_predict, full_image_arr_measure = None, save_path = None, save_imgs = None, overlap_amount = 0, fill_edges = False, include_headers = True, meta_name = "NA", testMode = False, maxdets = 6666, macro_model_list = []):
    new_w = micro_model.dim_x; new_h = micro_model.dim_y
    test_counter = 0; test_max = 6

    def get_piece(t_arr, x, y):
        piece = t_arr[y:min(y + new_h, t_arr.shape[0]), x:min(x + new_w, t_arr.shape[1])] # Calculate the dimensions of the piece
        if fill_edges: # Create a new array filled with zeros (black) of the desired final size
            filled_piece = np.zeros((new_h, new_w), dtype=t_arr.dtype)
            filled_piece[:piece.shape[0], :piece.shape[1]] = piece
            piece = filled_piece
        return piece
            
    t_arr = full_image_arr_predict; first = include_headers
    st = io.StringIO(); w, h = t_arr.shape[1], t_arr.shape[0]
    w_interval = new_w - overlap_amount; h_interval = new_h - overlap_amount
    tPath = os.path.join(save_imgs,cPredImgFldr); os.makedirs(tPath, exist_ok=True)
    total_tiles = (h+1)/(h_interval) * (w+1)/(w_interval); tile_counter = 0.0
    for y in range(0, h, h_interval):
        for x in range(0, w, w_interval):
            tile_counter += 1
            print(tile_counter,"out of",)
            piece_pred = get_piece(t_arr, x, y)
            piece_meas = get_piece(full_image_arr_measure, x, y) if (full_image_arr_measure is not None) else piece_pred
            tilename = f"{x:05},{y:05}"; print("Region:",tilename)
            predictions = micro_model.model.predict(piece_pred, show=False, max_det=maxdets, conf=micro_model.min_conf, half=True) 
            if save_imgs is not None: 
                img_array=predictions[0].plot(labels=False, boxes=True, masks=True); 
                combined_image = Image.new('RGB', (img_array.shape[1] + piece_pred.shape[1], img_array.shape[0]))
                combined_image.paste(Image.fromarray(img_array[..., ::-1]), (0, 0)); combined_image.paste(Image.fromarray(piece_pred[..., ::-1]), (img_array.shape[1], 0)); 
                combined_image.save(os.path.join(tPath, tilename + ".jpg"))
            infoToWrite = find_mask_intensities(predictions[0], piece_meas, original_image_name, tile_counter/total_tiles, x, y, w, h, first, meta_name, tilename, micro_model.max_area, macro_model_list)
            if infoToWrite:
                test_counter += 1
                st.write(infoToWrite); first = False
            if (testMode and test_counter > test_max): break
        if (testMode and test_counter > test_max): break

    strRet = st.getvalue()
    if (save_path is not None):
        with open(save_path, 'a') as file: file.write(strRet)
        st.close()
    print("Done with File")
    return strRet

def work_on_folder(micro_model, macro_model_list, SubFolder, ResultsFolder, testMode = False, IncludeHeaders = True, save_path = None, maxdet = 10000, overlap = 0):
    def prep_img(file_pred):
        img = Image.open(file_pred); img_array = np.array(img); # This code can handle 8 and 16-bit TIFFs . . not sure about RGB
        max_intensity = np.max(img_array); img_8bit = (255.0 * img_array / max_intensity).astype('uint8')
        img = Image.fromarray(img_8bit).convert('RGB'); 
        return img

    down_x = micro_model.down_x if micro_model else 1; down_y = micro_model.down_y if micro_model else 1; st = ""; names = []
    tPath = os.path.join(ResultsFolder, cPredImgFldr); os.makedirs(tPath, exist_ok=True)
    
    # Prep for Macro predictions (if there are any requested)
    if macro_model_list: #checks both not none and has list elements
        resize_dict = {}
        for ma in macro_model_list:
            if (ma.type == "macro"):
                key = (ma.channel_contains, ma.dim_x, ma.dim_y); res_img = resize_dict.get(key)
                if res_img is None: 
                    file_pred = find_first_file(SubFolder, ma.channel_contains)
                    img = prep_img(file_pred); 
                    p_img = img.resize((ma.dim_x, ma.dim_y), Image.Resampling.BILINEAR) # We can't crop or add letterboxes, since it will disrupt the connection to the omics data
                    res_img  = np.array(p_img); resize_dict[key] = res_img
                Run_MacroModel(ma, res_img, tPath)
            elif (ma.type == "transcripts" and not testMode):
                if (ma.downsample_match_micro_Down): ma.transcript_dict = create_transcript_dict(ma, down_x, down_y)
                else: ma.transcript_dict = create_transcript_dict(ma)
        print("Making SV ensemble . . ")
        ts = soft_voting_ensemble([ma.instance_mask for ma in macro_model_list if ma.type == "macro"])
        df = pd.DataFrame([(x, y, ts[x, y, 0], ts[x, y, 1]) for x in range(ts.shape[0]) for y in range(ts.shape[1])], columns=['x', 'y', 'SV Class', 'SV Conf'])
        df.to_csv(os.path.join(tPath, "Ensemble" + " LUT.csv"), index=False)
        #We should probably make the ensemble right here instead of during the other measures
    
    # Prep the large image for micro predictions
    if micro_model:
        file_pred = find_first_file(SubFolder, micro_model.channel_contains)
        img = prep_img(file_pred); width, height = img.size
        if (down_x < 1 or down_y < 1):
            new_width = int(width * down_x); new_height = int(height * down_y)
            img = img.resize((new_width, new_height), Image.Resampling.BILINEAR) # Resize the image before micro model
            print("  Resized image from", width, height, " to", new_width, new_height)
        pred_arr_m0 = np.array(img) # Convert to array
        print(" Loaded data from image", img.width, "x", img.height," m", img.mode, " min", np.min(pred_arr_m0), " max", str(np.max(pred_arr_m0)))
        if (down_x <1 or down_y <1): img.save(os.path.join(tPath, "main resized.jpg"))

        meas_arr_m0, names = create_multichannel_array(SubFolder, down_x, down_y)
        st = Predict_OnPartsOfImage(micro_model, file_pred, pred_arr_m0, meas_arr_m0, None, ResultsFolder, overlap, False, IncludeHeaders, os.path.basename(SubFolder), testMode, maxdet, macro_model_list) #st = Predict_OnPartsOfImage(m0.model, file_pred, pred_arr_m0, meas_arr_m0, None, dim_x, dim_y, 0, False, IncludeHeaders, SubFolder, testMode, maxdet, m0.min_conf, m0.max_area) # Old Style
        if (save_path is not None): 
            with open(save_path, 'a') as file: file.write(st)
    print("Done with Files")
    return st, names

def Run_MacroModel(macro_model, resized_image, result_path, matrix_export_exclude_conf_0 = True):
    def save_polygons_to_file(output_file, polygons,  output_format='json'):
        if output_format == 'json':
            with open(output_file, 'w') as f:
                json.dump(polygons, f)
        elif output_format == 'txt':
            with open(output_file, 'w') as f:
                for polygon in polygons:
                    polygon_str = ' '.join(map(str, polygon))
                    f.write(f"{polygon_str}\n")
        else: raise ValueError(f"Unsupported output format: {output_format}")
    
    ma = macro_model; tPath = result_path
    print("  Running Macro Model", ma.name, " on resized image"); 
    name = ma.name[:10]
    ma.res = ma.model.predict(resized_image)
    ma.instance_mask = create_instance_mask(ma.dim_x, ma.dim_y, ma.res[0])
    ts = ma.instance_mask
    #Export images - - - 
    img_array=ma.res[0].plot(labels=False, boxes=False, masks=True)
    Image.fromarray(resized_image).save(os.path.join(tPath, name + " resize.jpg"))
    Image.fromarray(img_array[..., ::-1]).save(os.path.join(tPath, name + " pred.jpg"))
    #Export a sparse Matrix - - - 
    columns_1=['x', 'y', name + ' Class', name + ' Conf', name + ' Instance']
    if matrix_export_exclude_conf_0:
        df = pd.DataFrame([(x, y, ts[x, y, 0], ts[x, y, 1], ts[x, y, 2]) for x in range(ts.shape[0]) for y in range(ts.shape[1]) if ts[x, y, 1] != 0], columns=columns_1)
    else:
        df = pd.DataFrame([(x, y, ts[x, y, 0], ts[x, y, 1], ts[x, y, 2]) for x in range(ts.shape[0]) for y in range(ts.shape[1])], columns=columns_1)
    df.to_csv(os.path.join(tPath, name + " LUT.csv"), index=False)
    #Export Polygons - - - - 
    with open(os.path.join(tPath, name + " polys.json"), 'w') as f: f.write(ma.res[0].tojson())
    for i, result in enumerate(ma.res):
        polygons = []
        for mask in result.masks:
            polygon = mask.xy #.numpy().tolist(); 
            polygons.append(polygon)
    #save_polygons_to_file(os.path.join(tPath, name + " polys.json"), polygons, 'json')
    #save_polygons_to_file(os.path.join(tPath, name + " polys.txt"), polygons, 'txt')

def clear_path(mPathClear):
    if os.path.exists(mPathClear):
        for filename in os.listdir(mPathClear):
            file_path = os.path.join(mPathClear, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"The specified path does not exist: {mPathClear}")

def count_txt_files(yamlPath):
    patterns = {
        'train': r'train:\s*\.\./(.+)',
        'val': r'val:\s*\.\./(.+)',
    }
    with open(yamlPath, 'r') as file: content = file.read()
    results = {}; base_dir = os.path.dirname(yamlPath)
    for label, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            relative_path = match.group(1).strip()
            directory = os.path.join(base_dir, relative_path)
            if os.path.isdir(directory): txt_count = len([f for f in os.listdir(directory) if f.endswith('.txt')])
            else: txt_count = 0
            results[label] = txt_count
    return results

def write_meta_json(dictionary, filepath):
    base_filename = "metaFIVE"; extension = "x.json"; counter = 0
    filename = os.path.join(filepath, f"{base_filename}{counter}{extension}")
    with open(filename, 'w') as json_file:
        json.dump(dictionary, json_file, indent=4)

def yolo_save_meta(new_folder_path, NameOfRun, yamlPath, results):
    base_dir = os.path.dirname(yamlPath)

    render_files = [f for f in os.listdir(base_dir) if re.match(r'render\d+x\.json', f)]
    if render_files:
        most_recent_render = max(render_files, key=lambda f: int(re.search(r'\d+', f).group()))
        most_recent_render_path = os.path.join(base_dir, most_recent_render)
        shutil.copy(most_recent_render_path, new_folder_path)
        with open(os.path.join(new_folder_path, most_recent_render), 'r') as file:
            data = json.load(file)
            units_per_pixel = data.get("Pixel Width in Unit")
            unit = data.get("Unit")

    meta_dict = {
        "Timestamp": datetime.now().isoformat(),
        "Host Computer Name": socket.gethostname(),
        "Base Path" : base_dir,
        "Model Path" : new_folder_path,
        "Run Name" : NameOfRun,
        "Render Info Path" : most_recent_render_path,
        "Units per Pixel" : units_per_pixel,
        "Units" : unit,
        "Image Counts" : count_txt_files(yamlPath),
        "Class Names" : results.names,
    }
    write_meta_json(meta_dict, new_folder_path)

def macro_copy(macro_to_copy, macro_list_to_append, model_path):
    ma = copy.deepcopy(macro_to_copy)
    macro_list_to_append.append(ma)
    ma.model_path = model_path

def init_macro_micro_predictions(params, micro, macro_list):
    def setup_model(m):
        if m is None: return
        m.model = YOLO(m.model_path); 
        m.name = os.path.basename(os.path.dirname(os.path.dirname(m.model_path)))
        strNotes = ""
        if (not hasattr(m, 'dim_x') or m.dim_x is None): #then get from the model itself
            m.dim_x = m.model.overrides['imgsz'] #If you get an error here then please manually enter the dimensions for the model, or we can get it from the args.yaml
            strNotes += "Found dimensions from model: " + str(m.dim_x) + ". "
        if (not hasattr(m, "dim_y") or m.dim_y is None): 
            m.dim_y = m.dim_x
        if (not hasattr(m, "max_area") or m.max_area is None): 
            m.max_area = 30000 if m.type == "micro" else 30000000
            strNotes += "Set default max_area to " + str(m.max_area) + ". "
        if (not hasattr(m, "down_x") or m.down_x is None): m.down_x = 1
        if (not hasattr(m, "down_y") or m.down_y is None): m.down_y = m.down_x
        if (not hasattr(m, "min_conf") or m.min_conf is None): 
            m.min_conf = 0.20
            strNotes += "Set default min_conf to " + str(m.min_conf) + ". "
        if strNotes != "": print(m.type, m.name, strNotes)
            
    # Setup and Save settings
    Image.MAX_IMAGE_PIXELS = None #Turn off the limit
    Prefix = f"R_{datetime.now().strftime('%Y%m%d_%H%M%S')}{params.res_append}"
    params.newFolder = os.path.join(params.m_folder,Prefix); os.makedirs(params.newFolder,True)
    meta_dicts = { "m0" : str(micro), "ms": str(macro_list)}
    meta_dicts["Folder"] = params.m_folder
    with open(os.path.join(params.newFolder,"rundata.json"), 'w') as f: json.dump(meta_dicts, f, indent=2)

    # Load models, assign metadata
    setup_model(micro)
    for m in macro_list: 
        if (m.type != "transcripts"): setup_model(m)
        else: m.transcript_dict = {}
        
def infer(m_folder, micro_model_path, macro_model_path, testMode=False, save_folder="", micro_channel_contains="C3", 
          macro_channel_contains="C3", micro_min_conf=0.38, macro_min_conf=0.20):
    # Spinal Cord from Dodd and Feiderling

    params = types.SimpleNamespace(); 
    params.m_folder = rf"{m_folder}" # Needs to be in one more subfolder after that
    params.res_append = rf"{save_folder}"  #This just changes the name of the save folder, can be empty
    params.testMode = testMode
    m0 = None; ms = []

    # - - - - Micro Level
    m0 = types.SimpleNamespace(); m0.type = "micro"
    m0.model_path = rf"{micro_model_path}" 
    m0.channel_contains = micro_channel_contains 
    m0.min_conf = micro_min_conf

    # - - - - - Macro Levels - - - - -
    ma = types.SimpleNamespace();  
    ms.append(ma); ma.type = "macro";
    ma.model_path = rf"{macro_model_path}"
    ma.channel_contains = macro_channel_contains
    ma.min_conf = macro_min_conf
    
    init_macro_micro_predictions(params, m0, ms)

    first_level_subfolders = next(os.walk(params.m_folder))[1]  # Get first level of folders only
    First = True; stio = io.StringIO(); namedict = {}
    for subfolder in first_level_subfolders:
        if (subfolder.startswith("R_20") and len(subfolder)>12): continue # this is a run folder
        print(subfolder,"------------------------------------------------------------------")
        subfolder_path = os.path.join(params.m_folder, subfolder)
        st, names = work_on_folder(m0, ms, subfolder_path, params.newFolder, params.testMode, First)
        stio.write(st); namedict[subfolder] = names; First = False
        if (params.testMode): break

    if m0 is not None:
        # Save out the name information
        save_path = os.path.join(params.newFolder, "ChannelNames.txt")
        rows = [f"{subfolder}\t{idx}\t{name}" for subfolder, names in namedict.items() for idx, name in enumerate(names)]
        with open(save_path, 'w') as txtfile:
            txtfile.write("Subfolder\tIndex\tName\n"); txtfile.write("\n".join(rows))

        # Save out the main data
        save_path = os.path.join(params.newFolder, "PerInstance.txt"); strRet = stio.getvalue(); stio.close()
        with open(save_path, 'a') as file: file.write(strRet)

    print("Done with Folder")