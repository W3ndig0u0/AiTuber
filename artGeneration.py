import torch
from diffusers import DiffusionPipeline
from PIL import Image
from accelerate import Accelerator
import time
import os

class AnimeArtist:
    def __init__(self):
        # Initialize any required attributes here
        self.progress = 0
        self.total_steps = 0
        self.generation_complete = False
        self.estimated_time = None
        self.generator = None

    def generate_art(self, prompt, height, width, num_inference_steps, eta, guidance_scale, save_folder, initial_generation=False):
        if initial_generation:
            self.progress = 0
        self.total_steps = num_inference_steps
        self.generation_complete = False
        self.estimated_time = None

        with torch.no_grad():
            generator = self.generator
            # generator.to("mps")
            current_image = None
            intermediate_folder = os.path.join(save_folder, 'intermediate')

            os.makedirs(intermediate_folder, exist_ok=True)

            existing_files = os.listdir(intermediate_folder)
            file_count = len(existing_files)

            # for step in range(num_inference_steps):
            # prompt_with_image = f"{prompt} {current_image}" if current_image else prompt

            generated = generator(prompt, 512, 512, num_inference_steps, eta=eta, guidance_scale=guidance_scale)
            current_image = generated.images[0]

            file_number = file_count +  1
            save_path = os.path.join(intermediate_folder, f"{file_number}.png")
            current_image.save(save_path)

            self.progress = step + 1
            time.sleep(1)

            final_file_number = file_count + num_inference_steps
            final_save_path = os.path.join(save_folder, f"{final_file_number}-final.png")
            current_image.save(final_save_path)

            self.generation_complete = True

        return intermediate_folder, final_save_path


if __name__ == '__main__':
    anime_artist = AnimeArtist()

    generator = YourGeneratorModel()
    anime_artist.generator = generator

    prompt = "Masterpiece, cute girl, fantasy, jump pose"
    num_inference_steps = 1
    eta = 0.1
    guidance_scale = 1
    save_folder = "./GeneratedImg"
    anime_artist.generate_art(prompt, num_inference_steps, eta, guidance_scale, save_folder, initial_generation=False)
