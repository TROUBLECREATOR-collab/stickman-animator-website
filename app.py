from flask import Flask, render_template, request, jsonify
import os
import base64
import io
from PIL import Image, ImageDraw
import random

app = Flask(__name__)

class SimpleStickmanAnimator:
    def __init__(self, canvas_size=(400, 400)):
        self.canvas_size = canvas_size
        
    def create_stickman_frame(self, pose_type="neutral", frame_num=0):
        # Create a new image with white background
        img = Image.new('RGB', self.canvas_size, 'white')
        draw = ImageDraw.Draw(img)
        
        # Define poses
        if pose_type == "neutral":
            self._draw_neutral_stickman(draw, frame_num)
        elif pose_type == "punch_right":
            self._draw_punch_stickman(draw, frame_num, "right")
        elif pose_type == "punch_left":
            self._draw_punch_stickman(draw, frame_num, "left")
        elif pose_type == "kick_right":
            self._draw_kick_stickman(draw, frame_num, "right")
        elif pose_type == "victory":
            self._draw_victory_stickman(draw, frame_num)
            
        return img
    
    def _draw_neutral_stickman(self, draw, frame_num):
        # Head
        draw.ellipse([180, 50, 220, 90], outline='blue', width=3)
        
        # Body
        draw.line([200, 90, 200, 200], fill='blue', width=3)
        
        # Arms
        draw.line([200, 120, 150, 150], fill='blue', width=3)  # Left
        draw.line([200, 120, 250, 150], fill='blue', width=3)  # Right
        
        # Legs
        draw.line([200, 200, 170, 280], fill='blue', width=3)  # Left
        draw.line([200, 200, 230, 280], fill='blue', width=3)  # Right
    
    def _draw_punch_stickman(self, draw, frame_num, direction):
        # Head
        draw.ellipse([180, 50, 220, 90], outline='red', width=3)
        
        # Body
        draw.line([200, 90, 200, 200], fill='red', width=3)
        
        if direction == "right":
            # Punching right arm
            draw.line([200, 120, 280, 130], fill='red', width=3)
            # Left arm back
            draw.line([200, 120, 140, 160], fill='red', width=3)
        else:
            # Punching left arm
            draw.line([200, 120, 120, 130], fill='red', width=3)
            # Right arm back
            draw.line([200, 120, 260, 160], fill='red', width=3)
        
        # Legs
        draw.line([200, 200, 170, 280], fill='red', width=3)
        draw.line([200, 200, 230, 280], fill='red', width=3)
    
    def _draw_kick_stickman(self, draw, frame_num, direction):
        # Head
        draw.ellipse([180, 50, 220, 90], outline='green', width=3)
        
        # Body
        draw.line([200, 90, 200, 200], fill='green', width=3)
        
        # Arms for balance
        draw.line([200, 120, 160, 140], fill='green', width=3)
        draw.line([200, 120, 240, 140], fill='green', width=3)
        
        if direction == "right":
            # Standing leg
            draw.line([200, 200, 180, 280], fill='green', width=3)
            # Kicking leg
            draw.line([200, 200, 270, 220], fill='green', width=3)
        else:
            # Standing leg
            draw.line([200, 200, 220, 280], fill='green', width=3)
            # Kicking leg
            draw.line([200, 200, 130, 220], fill='green', width=3)
    
    def _draw_victory_stickman(self, draw, frame_num):
        # Head
        draw.ellipse([180, 50, 220, 90], outline='purple', width=3)
        
        # Body
        draw.line([200, 90, 200, 200], fill='purple', width=3)
        
        # Victory arms up
        draw.line([200, 120, 150, 80], fill='purple', width=3)
        draw.line([200, 120, 250, 80], fill='purple', width=3)
        
        # Legs
        draw.line([200, 200, 170, 280], fill='purple', width=3)
        draw.line([200, 200, 230, 280], fill='purple', width=3)
    
    def create_animation(self, sequence):
        frames = []
        for move in sequence:
            for frame_num in range(move["frames"]):
                frame = self.create_stickman_frame(move["pose"], frame_num)
                
                # Convert to base64 for web display
                buffered = io.BytesIO()
                frame.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                frames.append(f"data:image/png;base64,{img_str}")
        
        return frames

class FightChoreographer:
    def interpret_prompt(self, prompt):
        prompt = prompt.lower()
        sequence = [{"pose": "neutral", "frames": 8}]
        
        if "punch" in prompt:
            if "right" in prompt:
                sequence.extend([{"pose": "punch_right", "frames": 6}])
            if "left" in prompt:
                sequence.extend([{"pose": "punch_left", "frames": 6}])
        
        if "kick" in prompt:
            sequence.extend([{"pose": "kick_right", "frames": 8}])
        
        sequence.append({"pose": "victory", "frames": 10})
        return sequence

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_animation():
    try:
        fight_description = request.form['fight_description']
        
        animator = SimpleStickmanAnimator()
        choreographer = FightChoreographer()
        
        sequence = choreographer.interpret_prompt(fight_description)
        frames = animator.create_animation(sequence)
        
        return jsonify({
            'success': True,
            'frames': frames,
            'message': f'Created {len(frames)} frames animation!'
        })
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "Stickman animator is running!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
