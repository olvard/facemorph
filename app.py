from nicegui import ui
from utils import align_face, face_morph
import PIL.Image
import io
import numpy as np
import asyncio

morphed_image = None

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
				ui.upload(on_upload=lambda file: handle_face2_upload(file), auto_upload=True).props('label="Choose Face 2"').style('font-size: 24px; width: 100%; height: 50px;')

				async def handle_face2_upload(file):
					image_data = file.content.read()
					pil_image = PIL.Image.open(io.BytesIO(image_data))
					face2 = align_face(pil_image)
					# set img to PIL image source for face1_aligned_image
					
					face2_aligned_image.set_source(face2)
					await asyncio.sleep(0.5)
					face2_aligned_image.update()

			with ui.element('div').classes('flex flex-col-reverse').style('width: 100%; align-items: center;'):
				steps_slider = ui.slider(min=1, max=200, value=5).style('width: 100%; margin: 20px 0')  # Increased slider width
				slider_label = ui.label(f'Steps: {steps_slider.value}').style('font-size: 24px; margin-top: 10px;')
				
				def update_label():
					slider_label.set_text(f'Steps: {steps_slider.value}')

				steps_slider.on('change', update_label)

			# Morph faces function
			async def morph_faces():

				loading_label = ui.label('Morphing in progress...').style('font-size: 24px; color: yellow; margin-top: 20px;')
				await asyncio.sleep(0.1)  # Allow UI to update

				morphed_image = face_morph(face1_aligned_image.source, face2_aligned_image.source, steps_slider.value)

				loading_label.set_text('Morphing complete!')
				await asyncio.sleep(1)  # Show completion message briefly
				loading_label.set_text('')
				
				morph_result.set_source(morphed_image[5])
				await asyncio.sleep(0.5)
				morph_result.update()

				# append face1 to first position of morphed_image and face2 to last position
				morphed_image.insert(0, face1_aligned_image.source)
				morphed_image.append(face2_aligned_image.source)

				morph_slider_label = ui.label(f'Morph Level: ').style('font-size: 24px; margin-top: 10px;')

				morph_slider = ui.slider(min=0, max=len(morphed_image)-1, value=5).style('width: 100%; margin: 20px 0; ')  # Increased slider width

				def update_morph_label():
					morph_slider_label.set_text(f'Morph Level: {morph_slider.value}')
					morph_result.set_source(morphed_image[morph_slider.value])
					morph_result.update()

				morph_slider.on('change', update_morph_label)

		# Right column: Display images
		with ui.column().style('width: 50%; align-items: center; justify-content: flex-start;'):
			with ui.row().style('justify-content: center; margin-top: 20px;'):
				face1_aligned_image = ui.image().style('width: 200px; height: 200px; margin: 10px; object-fit: cover; border: 2px solid white;')
				face2_aligned_image = ui.image().style('width: 200px; height: 200px; margin: 10px; object-fit: cover; border: 2px solid white;')

			# Display morph result below
			morph_result = ui.image().style('width: 400px; height: 400px; margin: 10px; object-fit: cover; border: 2px solid white;')  # Reserve space for the morph result

			ui.button('MORPH', on_click=morph_faces).style('font-size: 24px; margin: 20px 0;')  # Larger button text

	ui.run()

if __name__ in {"__main__", "__mp_main__"}:
	main()
