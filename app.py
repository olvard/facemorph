from nicegui import ui
from utils import align_face, face_morph
import PIL.Image
import io
import numpy as np
import asyncio

def main():
	# Set the global background color to black and text color to white
	ui.add_head_html('<style>body { background-color: black; color: white; }</style>')

	# Header with proper centering
	ui.label('Face Morphing Tool').classes('text-3xl font-bold mb-8').style('text-align: center; margin-top: 20px; margin: auto;')

	# Main container for the two columns (controls on left, images on right)
	with ui.element('div').classes('flex').style('width: 70%; height: 100%; margin: auto;'):	
		
		# Left column: Controls and sliders
		with ui.column().style('width: 50%; align-items: center; padding: 20px; justify-content: flex-start;'):
			
			# Face 1 upload container
			with ui.element('div').style('width: 100%; margin-bottom: 30px;'):
				# Upload button for Face 1
				ui.upload(on_upload=lambda file: handle_face1_upload(file), auto_upload=True).props('label="Choose Face 1"').style('font-size: 24px; width: 100%; height: 50px;')

				async def handle_face1_upload(file):
					image_data = file.content.read()
				
					pil_image = PIL.Image.open(io.BytesIO(image_data))
					face1 = align_face(pil_image)
					
					# set img to PIL image source for face1_aligned_image
					face1_aligned_image.set_source(face1)
					await asyncio.sleep(0.5)
					face1_aligned_image.update()
					
			# Face 2 upload container
			with ui.element('div').style('width: 100%; margin-bottom: 40px; margin-top: 30px;'):
				# Upload button for Face 2
				ui.upload(on_upload=lambda file: handle_face2_upload(file), auto_upload=True).props('label="Choose Face 2"').style('font-size: 24px; width: 100%; height: 50px;')

				async def handle_face2_upload(file):
					image_data = file.content.read()
					pil_image = PIL.Image.open(io.BytesIO(image_data))
					face2 = align_face(pil_image)
					# set img to PIL image source for face1_aligned_image
					
					face2_aligned_image.set_source(face2)
					await asyncio.sleep(0.5)
					face2_aligned_image.update()


			# Display slider value as label
			slider_label = ui.label(f'Steps').style('font-size: 24px; margin-top: 10px;')
			# Slider for morph steps
			steps_slider = ui.slider(min=1, max=200, value=5).style('width: 100%; margin: 20px 0')  # Increased slider width

			def update_label():
				slider_label.set_text(f'Steps: {steps_slider.value}')

			# Bind the slider change event to update the label
			steps_slider.on('change', update_label)

			# Morph faces function
			async def morph_faces():


				# Show loading effect
				loading_label = ui.label('Morphing in progress...').style('font-size: 24px; color: yellow; margin-top: 20px;')
				await asyncio.sleep(0.1)  # Allow UI to update

				# Perform the face morphing
				morphed_image = face_morph(face1_aligned_image.source, face2_aligned_image.source, steps_slider.value)

				# Hide loading effect
				loading_label.set_text('Morphing complete!')
				await asyncio.sleep(1)  # Show completion message briefly
				loading_label.set_text('')
				
				morph_result.set_source(morphed_image)
				await asyncio.sleep(0.5)
				morph_result.update()

			# Add morph slider label
			morph_slider_label = ui.label(f'Morph Level: ').style('font-size: 24px; margin-top: 10px;')

			# Slider for morph transition, also larger
			morph_slider = ui.slider(min=0, max=10, value=0).style('width: 100%; margin: 20px 0; ')  # Increased slider width
		

			def update_morph_label():
				morph_slider_label.set_text(f'Morph Level: {morph_slider.value}')

			# Bind the morph slider change event to update the label
			morph_slider.on('change', update_morph_label)

		

		# Right column: Display images
		with ui.column().style('width: 50%; align-items: center; justify-content: flex-start;'):
			# Row to display cropped images of both faces
			with ui.row().style('justify-content: center; margin-top: 20px;'):
				# Placeholder for the cropped image for Face 1
				face1_aligned_image = ui.image().style('width: 200px; height: 200px; margin: 10px; object-fit: cover; border: 2px solid white;')

				# Placeholder for the cropped image for Face 2
				face2_aligned_image = ui.image().style('width: 200px; height: 200px; margin: 10px; object-fit: cover; border: 2px solid white;')

			# Display morph result below
			morph_result = ui.image().style('width: 400px; height: 400px; margin: 10px; object-fit: cover; border: 2px solid white;')  # Reserve space for the morph result

						# Button to morph faces
			ui.button('MORPH', on_click=morph_faces).style('font-size: 24px; margin: 20px 0;')  # Larger button text

	
	# Start the NiceGUI app
	ui.run()

if __name__ in {"__main__", "__mp_main__"}:
	main()
