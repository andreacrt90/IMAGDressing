import runpod
import subprocess
import uuid
import os
import base64

def handler(event):
    try:
        # Legge input JSON
        cloth_path = event["input"].get("cloth_path")
        face_path = event["input"].get("face_path")

        if not cloth_path or not face_path:
            return {"error": "cloth_path e face_path sono richiesti."}

        # Nome unico per il file output
        output_file = f"outputs/output_{uuid.uuid4().hex}.png"
        os.makedirs("outputs", exist_ok=True)

        # Comando per lanciare lo script di inference
        cmd = [
            "python",
            "inference_IMAGdressing_ipa_controlnetpose.py",
            "--cloth_path", cloth_path,
            "--face_path", face_path,
            "--output_path", output_file,
            "--device", "cpu"  # CPU o GPU, se disponibile
        ]

        # Esecuzione comando
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return {"error": result.stderr}

        if os.path.exists(output_file):
            # Converte l'immagine in base64
            with open(output_file, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode("utf-8")
            return {"status": "success", "output_file": output_file, "image_base64": img_base64}

        return {"error": "File output non trovato."}

    except Exception as e:
        return {"error": str(e)}

# Avvia il serverless endpoint
runpod.serverless.start({"handler": handler})
