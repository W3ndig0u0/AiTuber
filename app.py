from flask import Flask, render_template, request, jsonify
from artGeneration import AnimeArtist
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import os

app = Flask(__name__)
anime_artist = AnimeArtist()


@app.route("/process_input", methods=["POST"])
def process_input():
    user_input = request.json["user_input"]
    response = virtual_tuber.run(user_input)
    return jsonify({"response": response})


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/art")
def art():
    return render_template("art.html")


@app.route("/generate_art", methods=["POST"])
def generate_art():
    prompt = request.json["prompt"]
    num_inference_steps = int(request.json["num_inference_steps"])
    eta = float(request.json["eta"])
    guidance_scale = int(request.json["guidance_scale"])
    width = int(request.json.get("width", 512))
    height = int(request.json.get("height", 512))
    seed = int(request.json.get("seed", -1))
    batch_size = int(request.json.get("batch_size", 1))

    save_folder = "./GeneratedImg"
    initial_generation = request.json.get("initial_generation", False)

    intermediate_folder, final_save_path = anime_artist.generate_art(
        prompt,
        width,
        height,
        num_inference_steps,
        eta,
        guidance_scale,
        save_folder,
        seed,
        batch_size,
        initial_generation,
    )

    intermediate_url = f"/{intermediate_folder}/"
    final_url = f"/{final_save_path}"

    response = {
        "intermediate_url": intermediate_url,
        "final_url": final_url,
        "progress": anime_artist.progress,
        "total_steps": anime_artist.total_steps,
        "generation_complete": anime_artist.generation_complete,
        "estimated_time": anime_artist.estimated_time,
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
