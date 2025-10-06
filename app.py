from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

class UltraSimpleStickmanAnimator:
    def __init__(self):
        self.poses = {
            "neutral": self._create_neutral_svg,
            "punch_right": self._create_punch_right_svg,
            "punch_left": self._create_punch_left_svg,
            "kick_right": self._create_kick_right_svg,
            "victory": self._create_victory_svg
        }
    
    def _create_neutral_svg(self, frame_num):
        return f'''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <rect width="400" height="400" fill="white"/>
            <!-- Head -->
            <circle cx="200" cy="100" r="20" fill="none" stroke="blue" stroke-width="3"/>
            <!-- Body -->
            <line x1="200" y1="120" x2="200" y2="220" stroke="blue" stroke-width="3"/>
            <!-- Arms -->
            <line x1="200" y1="150" x2="150" y2="180" stroke="blue" stroke-width="3"/>
            <line x1="200" y1="150" x2="250" y2="180" stroke="blue" stroke-width="3"/>
            <!-- Legs -->
            <line x1="200" y1="220" x2="170" y2="300" stroke="blue" stroke-width="3"/>
            <line x1="200" y1="220" x2="230" y2="300" stroke="blue" stroke-width="3"/>
        </svg>
        '''
    
    def _create_punch_right_svg(self, frame_num):
        punch_offset = min(frame_num * 5, 30)
        return f'''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <rect width="400" height="400" fill="white"/>
            <!-- Head -->
            <circle cx="200" cy="100" r="20" fill="none" stroke="red" stroke-width="3"/>
            <!-- Body -->
            <line x1="200" y1="120" x2="200" y2="220" stroke="red" stroke-width="3"/>
            <!-- Arms -->
            <line x1="200" y1="150" x2="130" y2="170" stroke="red" stroke-width="3"/>
            <line x1="200" y1="150" x2="{250 + punch_offset}" y2="140" stroke="red" stroke-width="3"/>
            <!-- Legs -->
            <line x1="200" y1="220" x2="170" y2="300" stroke="red" stroke-width="3"/>
            <line x1="200" y1="220" x2="230" y2="300" stroke="red" stroke-width="3"/>
        </svg>
        '''
    
    def _create_punch_left_svg(self, frame_num):
        punch_offset = min(frame_num * 5, 30)
        return f'''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <rect width="400" height="400" fill="white"/>
            <!-- Head -->
            <circle cx="200" cy="100" r="20" fill="none" stroke="orange" stroke-width="3"/>
            <!-- Body -->
            <line x1="200" y1="120" x2="200" y2="220" stroke="orange" stroke-width="3"/>
            <!-- Arms -->
            <line x1="200" y1="150" x2="{150 - punch_offset}" y2="140" stroke="orange" stroke-width="3"/>
            <line x1="200" y1="150" x2="270" y2="170" stroke="orange" stroke-width="3"/>
            <!-- Legs -->
            <line x1="200" y1="220" x2="170" y2="300" stroke="orange" stroke-width="3"/>
            <line x1="200" y1="220" x2="230" y2="300" stroke="orange" stroke-width="3"/>
        </svg>
        '''
    
    def _create_kick_right_svg(self, frame_num):
        kick_offset = min(frame_num * 8, 50)
        return f'''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <rect width="400" height="400" fill="white"/>
            <!-- Head -->
            <circle cx="200" cy="100" r="20" fill="none" stroke="green" stroke-width="3"/>
            <!-- Body -->
            <line x1="200" y1="120" x2="200" y2="220" stroke="green" stroke-width="3"/>
            <!-- Arms -->
            <line x1="200" y1="150" x2="170" y2="140" stroke="green" stroke-width="3"/>
            <line x1="200" y1="150" x2="230" y2="140" stroke="green" stroke-width="3"/>
            <!-- Legs -->
            <line x1="200" y1="220" x2="180" y2="300" stroke="green" stroke-width="3"/>
            <line x1="200" y1="220" x2="{230 + kick_offset}" y2="{250 - kick_offset}" stroke="green" stroke-width="3"/>
        </svg>
        '''
    
    def _create_victory_svg(self, frame_num):
        arm_wave = math.sin(frame_num * 0.5) * 10
        return f'''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <rect width="400" height="400" fill="white"/>
            <!-- Head -->
            <circle cx="200" cy="100" r="20" fill="none" stroke="purple" stroke-width="3"/>
            <!-- Body -->
            <line x1="200" y1="120" x2="200" y2="220" stroke="purple" stroke-width="3"/>
            <!-- Arms -->
            <line x1="200" y1="150" x2="150" y2="{80 + arm_wave}" stroke="purple" stroke-width="3"/>
            <line x1="200" y1="150" x2="250" y2="{80 - arm_wave}" stroke="purple" stroke-width="3"/>
            <!-- Legs -->
            <line x1="200" y1="220" x2="170" y2="300" stroke="purple" stroke-width="3"/>
            <line x1="200" y1="220" x2="230" y2="300" stroke="purple" stroke-width="3"/>
        </svg>
        '''
    
    def create_animation(self, sequence):
        frames = []
        for move in sequence:
            for frame_num in range(move["frames"]):
                svg_content = self.poses[move["pose"]](frame_num)
                frames.append(svg_content)
        return frames

class FightChoreographer:
    def interpret_prompt(self, prompt):
        prompt = prompt.lower()
        sequence = [{"pose": "neutral", "frames": 10}]
        
        if "punch" in prompt:
            if "right" in prompt:
                sequence.extend([{"pose": "punch_right", "frames": 8}])
            if "left" in prompt:
                sequence.extend([{"pose": "punch_left", "frames": 8}])
        
        if "kick" in prompt:
            sequence.extend([{"pose": "kick_right", "frames": 10}])
        
        sequence.append({"pose": "victory", "frames": 12})
        return sequence

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_animation():
    try:
        fight_description = request.form['fight_description']
        
        animator = UltraSimpleStickmanAnimator()
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
