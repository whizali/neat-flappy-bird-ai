# NEAT Flappy Bird AI

A comprehensive implementation of NEAT (NeuroEvolution of Augmenting Topologies) algorithm to train AI agents to play Flappy Bird, featuring both AI training and human-playable versions.

## Features

- **🧠 Optimized Neural Network**: 4 normalized inputs with feedforward architecture
- **🎯 Advanced Fitness Function**: Multi-layered reward system for survival, positioning, and pipe passing
- **👁️ Visual Learning**: Real-time AI training with debug visualization showing neural network inputs
- **🎮 Dual Game Modes**: AI training version and polished human-playable version
- **⚙️ Robust Implementation**: Comprehensive error handling, resource management, and optimized NEAT parameters

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install pygame neat-python
   ```

2. **AI Training Mode**:
   ```bash
   python flappy_bird.py
   ```
   Watch AI birds learn through evolution!

3. **Human Player Mode**:
   ```bash
   python game.py
   ```
   Play the game yourself with smooth controls!

## Neural Network Inputs

The AI receives 4 normalized inputs (0-1 range):
1. **Bird Y Position**: Vertical position on screen
2. **Distance to Pipe Center**: How far bird is from pipe gap center
3. **Bird Velocity**: Current falling/rising speed
4. **Horizontal Distance**: Distance to next pipe

## Configuration

Key parameters in `config-feedforward.txt`:
- **Population**: 20 genomes per generation (optimized for visual observation)
- **Hidden Nodes**: 0 (direct input-to-output connections for simplicity)
- **Activation Function**: tanh (stable and bounded)
- **Mutation Rates**: Balanced (0.4-0.6) for stable evolution
- **Fitness Threshold**: 300 points to complete training

## Expected Performance

- **Generation 1-3**: Basic flight control and boundary avoidance
- **Generation 4-8**: Learning to navigate through pipe gaps
- **Generation 8-15**: Consistent pipe passing and score improvement
- **Generation 15+**: Optimized strategies and high-score achievements

## Fitness Function

The AI uses a sophisticated multi-component fitness system:

### Rewards
- **+0.1** per frame survived (encourages longevity)
- **+0.05** for staying near screen center (avoids boundaries)
- **+0.02** for forward progress (time-based advancement)
- **+15** for successfully passing through a pipe (major achievement)

### Penalties
- **-5** for colliding with pipes (immediate failure)
- **-10** for hitting ground or ceiling (boundary violations)

## File Structure

```
├── flappy_bird.py          # AI training version (NEAT)
├── game.py                 # Human-playable version
├── config-feedforward.txt  # NEAT configuration
├── high_score.json         # High score storage (auto-generated)
├── imgs/                   # Game assets
│   ├── bird1.png
│   ├── bird2.png
│   ├── bird3.png
│   ├── pipe.png
│   ├── base.png
│   └── bg.png
└── README.md
```

## Controls

### AI Training Mode (flappy_bird.py)
- **Automatic Learning**: AI trains without manual input
- **D**: Toggle debug visualization lines (shows neural network inputs)
- **ESC/Close Window**: Stop training and exit
- **Console Output**: Real-time generation statistics and fitness progress

#### Debug Visualization
When enabled (press 'D'), colored lines show neural network inputs:
- **🔴 Red Line**: Bird's Y position (horizontal across screen)
- **🟠 Orange Line**: Distance from bird to pipe gap center
- **🟡 Yellow Line**: Bird's velocity (up/down movement indicator)
- **🟢 Green Line**: Horizontal distance to next pipe
- **🔵 Blue Lines**: Pipe gap boundaries (top and bottom)

### Human Player Mode (game.py)
- **SPACE** or **UP Arrow**: Make the bird jump/fly
- **P**: Pause/Resume game
- **ESC**: Return to main menu
- **ENTER**: Start game or restart after game over

## Technical Specifications

### Neural Network Architecture
- **Input Layer**: 4 normalized neurons (bird position, gap distance, velocity, pipe distance)
- **Hidden Layer**: 0 neurons (direct feedforward for simplicity)
- **Output Layer**: 1 neuron (jump decision threshold: >0.3)
- **Activation**: tanh function for bounded outputs

### NEAT Parameters
- **Population Size**: 20 genomes per generation
- **Species Management**: Automatic speciation with compatibility threshold 3.5
- **Mutation Rates**: Weight (0.6), Bias (0.4), Structure (0.05-0.2)
- **Selection**: Top 25% survival rate with elitism (2 best per species)

## Customization

- **Fitness Function**: Modify rewards/penalties in `main()` function
- **NEAT Parameters**: Tune evolution in `config-feedforward.txt`
- **Jump Sensitivity**: Adjust threshold (currently 0.3) in neural network output
- **Visual Settings**: Toggle debug lines, adjust FPS (30), population display

---

*This implementation demonstrates the power of evolutionary algorithms in game AI, showing how neural networks can learn complex timing and decision-making through natural selection.*
