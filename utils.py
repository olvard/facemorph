import sys
import os
import torch
import matplotlib.pyplot as plt
repo_path = '/Users/oliverlundin/Local Documents/github/facemorph/stylegan2-ada-pytorch'
sys.path.append(repo_path)
import projector
import torch
from PIL import Image
import numpy as np
import pickle
import torch.nn.functional as F
import face_alignment
from ffhq_align_app import image_align
import io


def align_face(input_image):

	landmarks_detector = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, device='mps', flip_input=False)

	converted = np.array(input_image)

	for i, face_landmarks in enumerate([landmarks_detector.get_landmarks_from_image(converted)[0]], start=1):

		final = image_align(input_image, face_landmarks=face_landmarks)
        
		# empty cache
		torch.mps.empty_cache()

	return final

def face_morph(face1,face2,steps):
	# Convert the PIL images to NumPy arrays
	face1_array = np.array(face1)
	face2_array = np.array(face2)

	# Convert NumPy arrays to PyTorch tensors with specified dtype
	face1_tensor = torch.tensor(face1_array, dtype=torch.float16)  # Change dtype as needed
	face2_tensor = torch.tensor(face2_array, dtype=torch.float16)

	# Set device
	if(torch.backends.mps.is_available()): # True
		print("MPS is available")
		device = torch.device("mps")


	# Load the generator model from the pickle file
	with open('ffhq_res256.pkl', 'rb') as f:
		G = pickle.load(f)['G_ema'].to(device) 

	# Match generator resolution to the input image resolution
	face1_tensor = face1_tensor.squeeze()
	face1_tensor = face1_tensor.permute(2, 0, 1)
	face1_tensor = F.interpolate(face1_tensor.unsqueeze(0), size=(G.img_resolution, G.img_resolution), mode='bilinear', align_corners=False)
	face1_tensor = face1_tensor.squeeze(0)

	face2_tensor = face2_tensor.squeeze()
	face2_tensor = face2_tensor.permute(2, 0, 1)
	face2_tensor = F.interpolate(face2_tensor.unsqueeze(0), size=(G.img_resolution, G.img_resolution), mode='bilinear', align_corners=False)
	face2_tensor = face2_tensor.squeeze(0)

	face1_tensor = face1_tensor.to(device)
	face2_tensor = face2_tensor.to(device)

	# empty cache
	torch.mps.empty_cache()

	# Project the first image
	projected_w_steps1 = projector.project(
		G,
		target=face1_tensor,  # Your target image tensor
		num_steps=steps,  # Number of optimization steps
		device = device,
		verbose=True  # Print optimization progress
	)

	# Project the second image
	projected_w_steps2 = projector.project(
		G,
		target=face2_tensor,  # Your target image tensor
		num_steps=steps,  # Number of optimization steps
		device=device,
		verbose=True  # Print optimization progress
	)

	w1 = projected_w_steps1[-1].unsqueeze(0)
	w2 = projected_w_steps2[-1].unsqueeze(0)

	num_interpolations = 10
	interpolations = torch.zeros((num_interpolations, w1.shape[1], w1.shape[2]), device=device)
	for i in range(num_interpolations):
		interpolations[i] = w1 + (w2 - w1) * i / (num_interpolations - 1)

	interpolated_images = G.synthesis(interpolations, noise_mode='const', force_fp32=True)

	interpolated_images = (interpolated_images + 1) * (255/2)

	interpolated_images = interpolated_images.permute(0, 2, 3, 1).clamp(0, 255).to(torch.uint8).cpu().numpy()

	print(type(interpolated_images[5]))

	# conver to pil image
	morphed = Image.fromarray(interpolated_images[5])

	return morphed