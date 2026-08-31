import subprocess
subprocess.run(["python", "scripts/sampler.py"])
subprocess.run(["python", "scripts/renamer.py"])
print("Now run the Gradio app manually and label as many comparisons as you want.")
print("Once done, run scripts/bradley_terry_scoring.py separately.")