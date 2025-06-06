# Import libraries import
import numpy as np
import open3d as o3d
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from PIL import Image
import torch
from transformers import GLPNImageProcessor, GLPNForDepthEstimation

# Getting model
feature_extractor = GLPNImageProcessor.from_pretrained("vinvino02/glpn-nyu")
model = GLPNForDepthEstimation.from_pretrained("vinvino02/glpn-nyu")

# Load and Resize Image
image = Image.open('E:\Mano\Generating 3D image Using 2D image\Data\phoenix_image.png')
new_height = 480 if image.height > 480 else image.height
new_height -= (new_height % 32)
new_width = int(image.height * image.width / image.height)
diff = new_width % 32

new_width = new_width - diff if diff < 16 else new_width + 32 - diff
new_size = (new_width, new_height)
image = image.resize(new_size)

# Preparing the image
inputs = feature_extractor(images=image, return_tensors ='pt')

# Getting the prediction for model
with torch.no_grad():
    outputs = model(**inputs)
    predicted_depth = outputs.predicted_depth

# Post-Processing

pad = 16
output = predicted_depth.squeeze().cpu().numpy()
output = output[pad:-pad, pad:-pad]
image = image.crop((pad,pad, image.width - pad, image.height - pad))

# Visualizing the prediction
fig, ax = plt.subplots(1, 2)
ax[0].imshow(image)
ax[0].tick_params(labelbottom=False, labelleft=False, bottom=False, left = False)
ax[1].imshow(output, cmap='plasma')
ax[1].tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)
plt.tight_layout()

# Preparing the depth for open3d

width, height = image.size
depth_image = (output * 255 / np.max(output)).astype('uint8')
image = np.array(image)

# rgbd image
depth_o3d = o3d.geometry.Image(depth_image)
image_o3d = o3d.geometry.Image(image)
regbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
    image_o3d, depth_o3d, convert_rgb_to_intensity = False)

# creating the camera
camera_intrinsics = o3d.camera.PinholeCameraIntrinsic(
    width, height, 500, 500, width / 2, height / 2
)

# creating the point cloud
pcd_raw = o3d.geometry.PointCloud.create_from_rgbd_image(
    regbd_image, camera_intrinsics
)

# o3d.visualization.draw_geometries([pcd_raw])

cl, ind = pcd_raw.remove_statistical_outlier(nb_neighbors=20, std_ratio=6.0)
pcd = pcd_raw.select_by_index(ind)

pcd.estimate_normals()
pcd.orient_normals_to_align_with_direction()

# o3d.visualization.draw_geometries([pcd])

# Surface reconstruction
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=10, n_threads=1)[0]

# rotate
rotation = mesh.get_rotation_matrix_from_xyz((np.pi, 0, 0))
mesh.rotate(rotation, center=(0, 0, 0))

o3d.visualization.draw_geometries([mesh], mesh_show_back_face= True)

# mesh_uniform = mesh.paint_uniform_color([0.9, 0.8, 0.9])
# mesh_uniform.compute_vertex_normals()
# o3d.visualization.draw_geometries([mesh_uniform], mesh_show_back_face=True)
