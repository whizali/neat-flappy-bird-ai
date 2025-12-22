# NEAT Flappy Bird AI - Data Flow Diagram

## Overview
This document illustrates the complete data flow through the NEAT Flappy Bird AI system, from initialization through evolution cycles to termination.

---

## Mermaid Data Flow Diagram

```mermaid
flowchart TD
    subgraph "System Initialization"
        START([🚀 Start Training])
        LOAD_CONFIG[📄 Load Configuration<br/>config-feedforward.txt]
        LOAD_ASSETS[🖼️ Load Game Assets<br/>Images & Fonts]
        INIT_PYGAME[🎮 Initialize Pygame<br/>Display & Sound]
    end
    
    subgraph "Generation N Setup"
        GEN_START([📊 Generation N Start])
        INIT_POP[👥 Initialize Population<br/>20 Random Genomes]
        CREATE_NETS[🧠 Create Neural Networks<br/>Feedforward Architecture]
        SPAWN_BIRDS[🐦 Spawn Bird Agents<br/>Starting Position (230, 300)]
        INIT_GAME[🎯 Initialize Game State<br/>Pipes, Base, Score=0]
    end
    
    subgraph "Game Simulation Loop (30 FPS)"
        GAME_TICK[⏱️ Game Tick<br/>1/30 second]
        
        subgraph "Input Processing"
            GET_STATE[📊 Extract Game State]
            CALC_INPUTS[🔢 Calculate NN Inputs<br/>4 Normalized Values]
            INPUT1[📍 Bird Y Position<br/>bird.y / WINDOW_HEIGHT]
            INPUT2[🎯 Gap Distance<br/>(bird.y - gap_center) / range]
            INPUT3[⚡ Velocity<br/>bird.velocity / 20.0]
            INPUT4[📏 Pipe Distance<br/>(pipe.x - bird.x) / WIDTH]
        end
        
        subgraph "Neural Network Processing"
            NN_FORWARD[🧠 Forward Pass<br/>4 Inputs → 1 Output]
            ACTIVATION[📈 Tanh Activation<br/>Range: [-1, 1]]
            DECISION[❓ Decision Logic<br/>if output > 0.3]
            JUMP_ACTION[🦘 Jump Action<br/>bird.jump()]
            FALL_ACTION[⬇️ Fall Action<br/>gravity applied]
        end
        
        subgraph "Physics Update"
            UPDATE_BIRDS[🐦 Update Bird Physics<br/>Position, Velocity, Rotation]
            UPDATE_PIPES[🏗️ Update Pipe Movement<br/>Horizontal Translation]
            UPDATE_BASE[🌍 Update Base Scroll<br/>Ground Animation]
        end
        
        subgraph "Collision Detection"
            CHECK_PIPE_COLLISION[💥 Check Pipe Collisions<br/>Pixel-Perfect Detection]
            CHECK_BOUNDARY[🚧 Check Boundaries<br/>Ground & Ceiling]
            REMOVE_DEAD[💀 Remove Dead Birds<br/>Update Active Lists]
        end
        
        subgraph "Fitness Calculation"
            SURVIVAL_BONUS[⏰ Survival Bonus<br/>+0.1 per frame]
            POSITION_BONUS[🎯 Position Bonus<br/>+0.05 if centered]
            PROGRESS_BONUS[➡️ Progress Bonus<br/>+0.02 per frame]
            PIPE_REWARD[🏆 Pipe Passage<br/>+15 points]
            COLLISION_PENALTY[❌ Collision Penalty<br/>-5 points]
            BOUNDARY_PENALTY[🚫 Boundary Penalty<br/>-10 points]
            UPDATE_FITNESS[📊 Update Genome Fitness<br/>Accumulate Rewards/Penalties]
        end
        
        subgraph "Rendering"
            RENDER_GAME[🖥️ Render Game Objects<br/>Birds, Pipes, Base]
            RENDER_DEBUG[🔍 Render Debug Lines<br/>Neural Network Inputs]
            RENDER_UI[📱 Render UI Elements<br/>Score, Generation, Bird Count]
            DISPLAY_UPDATE[🖼️ Update Display<br/>pygame.display.update()]
        end
    end
    
    subgraph "Generation Evaluation"
        ALL_DEAD{💀 All Birds Dead?}
        CALC_STATS[📈 Calculate Statistics<br/>Best, Average, Std Dev]
        PRINT_STATS[📝 Print Generation Stats<br/>Console Output]
        FITNESS_CHECK{🎯 Best Fitness ≥ 300?}
        MAX_GEN_CHECK{⏰ Max Generations?}
    end
    
    subgraph "Evolution Process"
        SPECIES_FORMATION[🔬 Form Species<br/>Compatibility Grouping]
        ADJUST_FITNESS[⚖️ Adjust Fitness<br/>Species Size Penalty]
        SELECTION[🎯 Selection Process<br/>Top 25% Survive]
        ELITISM[👑 Apply Elitism<br/>Preserve 2 Best per Species]
        CROSSOVER[🧬 Genetic Crossover<br/>Combine Parent Genomes]
        MUTATION[🎲 Apply Mutations<br/>Weights, Bias, Structure]
        NEW_POPULATION[👥 Create New Population<br/>Next Generation Ready]
    end
    
    subgraph "Termination"
        SUCCESS[🏆 Training Success<br/>Winner Found!]
        TIMEOUT[⏰ Training Timeout<br/>Max Generations Reached]
        CLEANUP[🧹 Cleanup Resources<br/>pygame.quit()]
        END([🏁 End Training])
    end
    
    %% Main Flow
    START --> LOAD_CONFIG
    LOAD_CONFIG --> LOAD_ASSETS
    LOAD_ASSETS --> INIT_PYGAME
    INIT_PYGAME --> GEN_START
    
    GEN_START --> INIT_POP
    INIT_POP --> CREATE_NETS
    CREATE_NETS --> SPAWN_BIRDS
    SPAWN_BIRDS --> INIT_GAME
    INIT_GAME --> GAME_TICK
    
    %% Game Loop Flow
    GAME_TICK --> GET_STATE
    GET_STATE --> CALC_INPUTS
    CALC_INPUTS --> INPUT1
    CALC_INPUTS --> INPUT2
    CALC_INPUTS --> INPUT3
    CALC_INPUTS --> INPUT4
    
    INPUT1 --> NN_FORWARD
    INPUT2 --> NN_FORWARD
    INPUT3 --> NN_FORWARD
    INPUT4 --> NN_FORWARD
    
    NN_FORWARD --> ACTIVATION
    ACTIVATION --> DECISION
    DECISION -->|output > 0.3| JUMP_ACTION
    DECISION -->|output ≤ 0.3| FALL_ACTION
    
    JUMP_ACTION --> UPDATE_BIRDS
    FALL_ACTION --> UPDATE_BIRDS
    UPDATE_BIRDS --> UPDATE_PIPES
    UPDATE_PIPES --> UPDATE_BASE
    
    UPDATE_BASE --> CHECK_PIPE_COLLISION
    CHECK_PIPE_COLLISION --> CHECK_BOUNDARY
    CHECK_BOUNDARY --> REMOVE_DEAD
    
    REMOVE_DEAD --> SURVIVAL_BONUS
    SURVIVAL_BONUS --> POSITION_BONUS
    POSITION_BONUS --> PROGRESS_BONUS
    PROGRESS_BONUS --> PIPE_REWARD
    PIPE_REWARD --> COLLISION_PENALTY
    COLLISION_PENALTY --> BOUNDARY_PENALTY
    BOUNDARY_PENALTY --> UPDATE_FITNESS
    
    UPDATE_FITNESS --> RENDER_GAME
    RENDER_GAME --> RENDER_DEBUG
    RENDER_DEBUG --> RENDER_UI
    RENDER_UI --> DISPLAY_UPDATE
    
    DISPLAY_UPDATE --> ALL_DEAD
    ALL_DEAD -->|No| GAME_TICK
    ALL_DEAD -->|Yes| CALC_STATS
    
    %% Evolution Flow
    CALC_STATS --> PRINT_STATS
    PRINT_STATS --> FITNESS_CHECK
    FITNESS_CHECK -->|Yes| SUCCESS
    FITNESS_CHECK -->|No| MAX_GEN_CHECK
    MAX_GEN_CHECK -->|Yes| TIMEOUT
    MAX_GEN_CHECK -->|No| SPECIES_FORMATION
    
    SPECIES_FORMATION --> ADJUST_FITNESS
    ADJUST_FITNESS --> SELECTION
    SELECTION --> ELITISM
    ELITISM --> CROSSOVER
    CROSSOVER --> MUTATION
    MUTATION --> NEW_POPULATION
    NEW_POPULATION --> GEN_START
    
    %% Termination Flow
    SUCCESS --> CLEANUP
    TIMEOUT --> CLEANUP
    CLEANUP --> END
    
    %% Styling
    classDef startClass fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    classDef processClass fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    classDef decisionClass fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    classDef fitnessClass fill:#f8bbd9,stroke:#ad1457,stroke-width:2px
    classDef evolutionClass fill:#dcedc8,stroke:#558b2f,stroke-width:2px
    classDef endClass fill:#ffab91,stroke:#d84315,stroke-width:2px
    classDef inputClass fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef nnClass fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef renderClass fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    
    class START,GEN_START,INIT_POP,CREATE_NETS,SPAWN_BIRDS,INIT_GAME startClass
    class LOAD_CONFIG,LOAD_ASSETS,INIT_PYGAME,GAME_TICK,GET_STATE,UPDATE_BIRDS,UPDATE_PIPES,UPDATE_BASE,CHECK_PIPE_COLLISION,CHECK_BOUNDARY,REMOVE_DEAD,CALC_STATS,PRINT_STATS processClass
    class ALL_DEAD,FITNESS_CHECK,MAX_GEN_CHECK,DECISION decisionClass
    class SURVIVAL_BONUS,POSITION_BONUS,PROGRESS_BONUS,PIPE_REWARD,COLLISION_PENALTY,BOUNDARY_PENALTY,UPDATE_FITNESS fitnessClass
    class SPECIES_FORMATION,ADJUST_FITNESS,SELECTION,ELITISM,CROSSOVER,MUTATION,NEW_POPULATION evolutionClass
    class SUCCESS,TIMEOUT,CLEANUP,END endClass
    class CALC_INPUTS,INPUT1,INPUT2,INPUT3,INPUT4 inputClass
    class NN_FORWARD,ACTIVATION,JUMP_ACTION,FALL_ACTION nnClass
    class RENDER_GAME,RENDER_DEBUG,RENDER_UI,DISPLAY_UPDATE renderClass
```

---

## Data Flow Stages

### 1. System Initialization
```
Input Data:
├── Configuration Parameters (config-feedforward.txt)
├── Game Assets (images, fonts)
└── System Resources (pygame, display)

Processing:
├── Parse NEAT configuration
├── Load visual assets with error handling
└── Initialize rendering system

Output Data:
└── Ready system state for training
```

### 2. Generation Setup
```
Input Data:
├── NEAT configuration parameters
├── Previous generation results (if any)
└── Random seed for genome initialization

Processing:
├── Create 20 random genomes (Generation 0)
├── OR reproduce from previous generation
├── Instantiate neural networks from genomes
└── Initialize game environment

Output Data:
├── Population of 20 genomes
├── Corresponding neural networks
├── 20 bird agents at starting positions
└── Clean game state (pipes, score, etc.)
```

### 3. Game Simulation Loop
```
Input Data (per frame):
├── Current bird positions and velocities
├── Pipe positions and gap locations
├── Game state (score, time, etc.)
└── User input (debug toggles)

Processing:
├── Extract 4 normalized neural network inputs
├── Forward pass through each neural network
├── Apply jump/fall actions based on output
├── Update physics (gravity, movement, collisions)
├── Calculate fitness rewards and penalties
└── Render frame with optional debug visualization

Output Data (per frame):
├── Updated bird states (position, velocity, alive status)
├── Updated fitness scores for each genome
├── Visual frame displayed to user
├── Console output (if birds die or pass pipes)
└── Debug visualization (if enabled)
```

### 4. Neural Network Data Flow
```
Raw Game State:
├── bird.y = 350 (pixels)
├── pipe.x = 500 (pixels)
├── pipe.gap_center = 400 (pixels)
└── bird.velocity = -8.5 (pixels/frame)

Normalized Inputs:
├── Input 1: 350/800 = 0.4375 (bird Y position)
├── Input 2: (350-400)/(400) = -0.125 (gap distance)
├── Input 3: -8.5/20.0 = -0.425 (velocity)
└── Input 4: (500-230)/600 = 0.45 (pipe distance)

Network Processing:
├── Weighted sum: Σ(wi × xi) + bias
├── Activation: tanh(weighted_sum)
└── Output: value in range [-1, 1]

Decision Logic:
├── if output > 0.3: bird.jump()
└── else: apply gravity (fall)
```

### 5. Fitness Calculation Data Flow
```
Continuous Rewards (per frame):
├── Survival: +0.1 points
├── Center Position: +0.05 points (if |bird.y - 400| < 100)
└── Progress: +0.02 points

Event-Based Rewards:
├── Pipe Passage: +15 points (when bird.x > pipe.x + pipe.width)
└── Score Increment: +1 to game score

Event-Based Penalties:
├── Pipe Collision: -5 points + bird death
└── Boundary Hit: -10 points + bird death

Fitness Accumulation:
├── genome.fitness += reward_points
├── genome.fitness -= penalty_points
└── Final fitness = sum of all frame rewards/penalties
```

### 6. Evolution Process Data Flow
```
Input Data:
├── 20 genomes with final fitness scores
├── Species compatibility matrix
└── Evolution parameters from config

Species Formation:
├── Calculate genetic distance between genomes
├── Group similar genomes (compatibility < 3.5)
├── Adjust fitness based on species size
└── Track species age and stagnation

Selection Process:
├── Rank genomes by adjusted fitness
├── Select top 25% as breeding candidates
├── Apply elitism (preserve 2 best per species)
└── Remove bottom 75% from population

Reproduction:
├── Crossover between high-fitness parents
├── Apply mutations to offspring
│   ├── Weight mutations (60% probability)
│   ├── Bias mutations (40% probability)
│   └── Structural mutations (5-20% probability)
└── Create new population of 20 genomes

Output Data:
└── New generation ready for evaluation
```

### 7. Termination Data Flow
```
Success Condition:
├── Check: max(genome.fitness) ≥ 300
├── If true: declare winner, save best genome
└── If false: continue evolution

Timeout Condition:
├── Check: current_generation ≥ max_generations
├── If true: end training (no winner)
└── If false: continue evolution

Cleanup Process:
├── Close pygame display
├── Release system resources
├── Print final statistics
└── Return best genome (if found)
```

---

## Text-Based Data Flow Summary

```
NEAT Flappy Bird AI - Complete Data Flow

START
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ INITIALIZATION PHASE                                        │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│ │Config File  │  │Game Assets  │  │Pygame Init  │          │
│ │Parameters   │→ │Images/Fonts │→ │Display/Sound│          │
│ └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ GENERATION N SETUP                                          │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│ │Population   │  │Neural       │  │Game State   │          │
│ │20 Genomes   │→ │Networks     │→ │Birds/Pipes  │          │
│ └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ GAME SIMULATION LOOP (30 FPS)                              │
│                                                             │
│ Game State → Neural Inputs → Network → Decision → Physics  │
│     ↓              ↓           ↓         ↓         ↓       │
│ ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────│
│ │Bird: x,y│  │Input 1: │  │Forward  │  │Jump or  │  │Grav-│
│ │Pipe: x,h│  │Y pos    │  │Pass     │  │Fall     │  │ity, │
│ │Velocity │  │Input 2: │  │tanh()   │  │Action   │  │Move │
│ │Score    │  │Gap dist │  │Output   │  │Execute  │  │ment │
│ └─────────┘  │Input 3: │  └─────────┘  └─────────┘  └─────│
│              │Velocity │                                   │
│              │Input 4: │                                   │
│              │Pipe dist│                                   │
│              └─────────┘                                   │
│                   ↓                                        │
│ Collision Check → Fitness Update → Render → All Dead?     │
│       ↓                ↓             ↓          ↓          │
│ ┌─────────┐    ┌─────────────┐  ┌─────────┐  ┌─────────┐   │
│ │Pipe Hit │    │Rewards:     │  │Visual   │  │Check    │   │
│ │Boundary │    │+0.1 survive │  │Display  │  │Living   │   │
│ │Detection│    │+0.05 center │  │Debug    │  │Birds    │   │
│ └─────────┘    │+0.02 progress│  │Lines    │  └─────────┘   │
│                │+15 pipe pass │  │UI Stats │               │
│                │Penalties:    │  └─────────┘               │
│                │-5 collision  │                            │
│                │-10 boundary  │                            │
│                └─────────────┘                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ EVOLUTION PROCESS                                           │
│                                                             │
│ Fitness Evaluation → Species Formation → Selection         │
│         ↓                    ↓                ↓             │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│ │Calculate    │    │Group by     │    │Top 25%      │      │
│ │Statistics   │    │Compatibility│    │Survive      │      │
│ │Best/Avg/Std │    │Threshold    │    │Elitism      │      │
│ └─────────────┘    │3.5          │    │Applied      │      │
│                    └─────────────┘    └─────────────┘      │
│                                              ↓             │
│ New Generation ← Mutation ← Crossover ← Reproduction       │
│       ↓              ↓          ↓            ↓             │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────│
│ │20 New       │ │Weight 60%   │ │Genetic      │ │Parent   │
│ │Genomes      │ │Bias 40%     │ │Combination  │ │Selection│
│ │Ready        │ │Structure 5% │ │High Fitness │ │Breeding │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────│
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
                ┌─────────────────┐
                │ Termination     │
                │ Check           │
                │ Fitness ≥ 300?  │
                │ Max Generations?│
                └─────────┬───────┘
                          │
                ┌─────────┴─────────┐
                │ No                │ Yes
                ▼                   ▼
        ┌───────────────┐   ┌───────────────┐
        │ Continue      │   │ End Training  │
        │ Next Gen      │   │ Cleanup       │
        └───────────────┘   │ Results       │
                            └───────────────┘
                                    │
                                    ▼
                                  END
```

This comprehensive data flow diagram shows how information moves through the system from initialization to termination, highlighting the cyclical nature of the evolutionary learning process and the real-time feedback between the game simulation and neural network decision making.
