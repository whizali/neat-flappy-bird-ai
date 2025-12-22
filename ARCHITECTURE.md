# NEAT Flappy Bird AI - System Architecture & Diagrams

## Table of Contents
1. [System Block Diagram](#system-block-diagram)
2. [Data Flow Diagram](#data-flow-diagram)
3. [Component Architecture](#component-architecture)
4. [Neural Network Architecture](#neural-network-architecture)
5. [NEAT Evolution Flow](#neat-evolution-flow)

---

## System Block Diagram

### Mermaid Code
```mermaid
graph TB
    subgraph "NEAT Flappy Bird AI System"
        subgraph "Input Layer"
            UI[User Interface]
            CONFIG[Config File<br/>config-feedforward.txt]
            ASSETS[Game Assets<br/>imgs/]
        end
        
        subgraph "Core Engine"
            NEAT_ENGINE[NEAT Engine<br/>Population Management]
            GAME_ENGINE[Game Engine<br/>Physics & Rendering]
            FITNESS_ENGINE[Fitness Evaluator<br/>Reward System]
        end
        
        subgraph "AI Components"
            POPULATION[Population<br/>20 Genomes]
            NETWORKS[Neural Networks<br/>Feedforward]
            SPECIES[Species Manager<br/>Compatibility Groups]
        end
        
        subgraph "Game Components"
            BIRD[Bird Agents<br/>Physics Objects]
            PIPES[Pipe System<br/>Obstacle Generation]
            COLLISION[Collision Detection<br/>Pixel Perfect]
        end
        
        subgraph "Output Layer"
            DISPLAY[Visual Display<br/>Pygame Rendering]
            DEBUG[Debug Visualization<br/>Neural Input Lines]
            CONSOLE[Console Output<br/>Generation Stats]
        end
        
        subgraph "Evolution Process"
            SELECTION[Selection<br/>Fitness-based]
            CROSSOVER[Crossover<br/>Genetic Recombination]
            MUTATION[Mutation<br/>Weight & Structure]
        end
    end
    
    %% Connections
    UI --> NEAT_ENGINE
    CONFIG --> NEAT_ENGINE
    ASSETS --> GAME_ENGINE
    
    NEAT_ENGINE --> POPULATION
    NEAT_ENGINE --> SPECIES
    POPULATION --> NETWORKS
    
    NETWORKS --> BIRD
    GAME_ENGINE --> PIPES
    GAME_ENGINE --> COLLISION
    
    BIRD --> FITNESS_ENGINE
    PIPES --> FITNESS_ENGINE
    COLLISION --> FITNESS_ENGINE
    
    FITNESS_ENGINE --> SELECTION
    SELECTION --> CROSSOVER
    CROSSOVER --> MUTATION
    MUTATION --> POPULATION
    
    GAME_ENGINE --> DISPLAY
    NETWORKS --> DEBUG
    NEAT_ENGINE --> CONSOLE
    
    %% Styling
    classDef inputClass fill:#e1f5fe
    classDef coreClass fill:#f3e5f5
    classDef aiClass fill:#e8f5e8
    classDef gameClass fill:#fff3e0
    classDef outputClass fill:#fce4ec
    classDef evolutionClass fill:#f1f8e9
    
    class UI,CONFIG,ASSETS inputClass
    class NEAT_ENGINE,GAME_ENGINE,FITNESS_ENGINE coreClass
    class POPULATION,NETWORKS,SPECIES aiClass
    class BIRD,PIPES,COLLISION gameClass
    class DISPLAY,DEBUG,CONSOLE outputClass
    class SELECTION,CROSSOVER,MUTATION evolutionClass
```

### Text-Based Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    NEAT Flappy Bird AI System                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ User Input  │    │ Config File │    │ Game Assets │         │
│  │ (Keyboard)  │    │ Parameters  │    │ (Images)    │         │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘         │
│         │                  │                  │                │
│         └──────────────────┼──────────────────┘                │
│                            │                                   │
│  ┌─────────────────────────▼─────────────────────────┐         │
│  │              NEAT Engine Core                     │         │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │         │
│  │  │ Population  │ │ Species     │ │ Fitness     │ │         │
│  │  │ Manager     │ │ Manager     │ │ Evaluator   │ │         │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ │         │
│  └─────────────────────────┬─────────────────────────┘         │
│                            │                                   │
│  ┌─────────────────────────▼─────────────────────────┐         │
│  │              Game Simulation Layer                │         │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │         │
│  │  │ Neural      │ │ Bird        │ │ Pipe        │ │         │
│  │  │ Networks    │ │ Agents      │ │ System      │ │         │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ │         │
│  └─────────────────────────┬─────────────────────────┘         │
│                            │                                   │
│  ┌─────────────────────────▼─────────────────────────┐         │
│  │              Output & Visualization               │         │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │         │
│  │  │ Game        │ │ Debug       │ │ Console     │ │         │
│  │  │ Display     │ │ Lines       │ │ Stats       │ │         │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ │         │
│  └─────────────────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Mermaid Code
```mermaid
flowchart TD
    subgraph "Generation N"
        START([Start Generation N])
        INIT_POP[Initialize Population<br/>20 Genomes]
        CREATE_NETS[Create Neural Networks<br/>from Genomes]
        SPAWN_BIRDS[Spawn Bird Agents<br/>at Starting Position]
    end
    
    subgraph "Game Simulation Loop"
        GAME_TICK[Game Tick<br/>30 FPS]
        GET_INPUTS[Extract Game State<br/>4 Normalized Inputs]
        NN_PROCESS[Neural Network<br/>Forward Pass]
        DECISION[Jump Decision<br/>Threshold > 0.3]
        UPDATE_PHYSICS[Update Bird Physics<br/>Gravity + Movement]
        CHECK_COLLISION[Collision Detection<br/>Pipes + Boundaries]
        UPDATE_FITNESS[Update Fitness<br/>Rewards + Penalties]
        RENDER[Render Frame<br/>Visual + Debug Lines]
    end
    
    subgraph "Fitness Evaluation"
        SURVIVAL[Survival Bonus<br/>+0.1 per frame]
        POSITION[Position Bonus<br/>+0.05 if centered]
        PROGRESS[Progress Bonus<br/>+0.02 per frame]
        PIPE_PASS[Pipe Passage<br/>+15 points]
        COLLISION_PEN[Collision Penalty<br/>-5 points]
        BOUNDARY_PEN[Boundary Penalty<br/>-10 points]
    end
    
    subgraph "Evolution Process"
        ALL_DEAD{All Birds Dead?}
        EVALUATE[Evaluate Generation<br/>Fitness Statistics]
        SPECIES_FORM[Form Species<br/>Compatibility Grouping]
        SELECTION[Selection Process<br/>Top 25% Survive]
        CROSSOVER[Genetic Crossover<br/>Combine Parent Genomes]
        MUTATION[Apply Mutations<br/>Weights + Structure]
        NEW_GEN[Create New Generation<br/>N+1]
    end
    
    subgraph "Termination Check"
        FITNESS_CHECK{Fitness ≥ 300?}
        MAX_GEN{Max Generations?}
        WINNER[Winner Found!]
        END_TRAINING[End Training]
    end
    
    %% Main Flow
    START --> INIT_POP
    INIT_POP --> CREATE_NETS
    CREATE_NETS --> SPAWN_BIRDS
    SPAWN_BIRDS --> GAME_TICK
    
    %% Game Loop
    GAME_TICK --> GET_INPUTS
    GET_INPUTS --> NN_PROCESS
    NN_PROCESS --> DECISION
    DECISION --> UPDATE_PHYSICS
    UPDATE_PHYSICS --> CHECK_COLLISION
    CHECK_COLLISION --> UPDATE_FITNESS
    UPDATE_FITNESS --> RENDER
    RENDER --> ALL_DEAD
    
    %% Fitness Components
    UPDATE_FITNESS --> SURVIVAL
    UPDATE_FITNESS --> POSITION
    UPDATE_FITNESS --> PROGRESS
    UPDATE_FITNESS --> PIPE_PASS
    UPDATE_FITNESS --> COLLISION_PEN
    UPDATE_FITNESS --> BOUNDARY_PEN
    
    %% Evolution Flow
    ALL_DEAD -->|Yes| EVALUATE
    ALL_DEAD -->|No| GAME_TICK
    EVALUATE --> SPECIES_FORM
    SPECIES_FORM --> SELECTION
    SELECTION --> CROSSOVER
    CROSSOVER --> MUTATION
    MUTATION --> NEW_GEN
    NEW_GEN --> FITNESS_CHECK
    
    %% Termination
    FITNESS_CHECK -->|Yes| WINNER
    FITNESS_CHECK -->|No| MAX_GEN
    MAX_GEN -->|Yes| END_TRAINING
    MAX_GEN -->|No| INIT_POP
    WINNER --> END_TRAINING
    
    %% Styling
    classDef startClass fill:#c8e6c9
    classDef processClass fill:#bbdefb
    classDef decisionClass fill:#ffcdd2
    classDef fitnessClass fill:#f8bbd9
    classDef evolutionClass fill:#dcedc8
    classDef endClass fill:#ffab91
    
    class START,INIT_POP,CREATE_NETS,SPAWN_BIRDS startClass
    class GAME_TICK,GET_INPUTS,NN_PROCESS,UPDATE_PHYSICS,CHECK_COLLISION,RENDER processClass
    class DECISION,ALL_DEAD,FITNESS_CHECK,MAX_GEN decisionClass
    class SURVIVAL,POSITION,PROGRESS,PIPE_PASS,COLLISION_PEN,BOUNDARY_PEN,UPDATE_FITNESS fitnessClass
    class EVALUATE,SPECIES_FORM,SELECTION,CROSSOVER,MUTATION,NEW_GEN evolutionClass
    class WINNER,END_TRAINING endClass
```

### Text-Based Data Flow
```
Generation N Start
        │
        ▼
┌───────────────────┐
│ Initialize        │
│ Population (20)   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Create Neural     │
│ Networks          │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐    ┌─────────────────────────────────┐
│ Spawn Birds       │    │         Game Loop               │
│ (Starting Pos)    │───▶│                                 │
└───────────────────┘    │  ┌─────────────────────────┐    │
                         │  │ 1. Extract Inputs       │    │
                         │  │    • Bird Y Position    │    │
                         │  │    • Gap Distance       │    │
                         │  │    • Velocity           │    │
                         │  │    • Pipe Distance      │    │
                         │  └─────────┬───────────────┘    │
                         │            │                    │
                         │            ▼                    │
                         │  ┌─────────────────────────┐    │
                         │  │ 2. Neural Network       │    │
                         │  │    Forward Pass         │    │
                         │  └─────────┬───────────────┘    │
                         │            │                    │
                         │            ▼                    │
                         │  ┌─────────────────────────┐    │
                         │  │ 3. Decision Making      │    │
                         │  │    if output > 0.3      │    │
                         │  │    then jump()          │    │
                         │  └─────────┬───────────────┘    │
                         │            │                    │
                         │            ▼                    │
                         │  ┌─────────────────────────┐    │
                         │  │ 4. Physics Update       │    │
                         │  │    • Apply Gravity      │    │
                         │  │    • Move Objects       │    │
                         │  │    • Check Collisions   │    │
                         │  └─────────┬───────────────┘    │
                         │            │                    │
                         │            ▼                    │
                         │  ┌─────────────────────────┐    │
                         │  │ 5. Fitness Update       │    │
                         │  │    Rewards:             │    │
                         │  │    • +0.1 survival      │    │
                         │  │    • +0.05 position     │    │
                         │  │    • +0.02 progress     │    │
                         │  │    • +15 pipe pass      │    │
                         │  │    Penalties:           │    │
                         │  │    • -5 collision       │    │
                         │  │    • -10 boundary       │    │
                         │  └─────────┬───────────────┘    │
                         │            │                    │
                         │            ▼                    │
                         │  ┌─────────────────────────┐    │
                         │  │ 6. Render Frame         │    │
                         │  │    • Game Objects       │    │
                         │  │    • Debug Lines        │    │
                         │  │    • UI Elements        │    │
                         │  └─────────┬───────────────┘    │
                         │            │                    │
                         └────────────┼────────────────────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ All Birds     │
                              │ Dead?         │
                              └───────┬───────┘
                                      │
                         ┌────────────┴────────────┐
                         │ No                      │ Yes
                         ▼                         ▼
                 ┌───────────────┐    ┌─────────────────────────┐
                 │ Continue      │    │    Evolution Process    │
                 │ Game Loop     │    │                         │
                 └───────────────┘    │ 1. Evaluate Fitness     │
                                      │ 2. Form Species         │
                                      │ 3. Selection (25%)      │
                                      │ 4. Crossover           │
                                      │ 5. Mutation            │
                                      │ 6. Create New Gen      │
                                      └─────────┬───────────────┘
                                                │
                                                ▼
                                      ┌─────────────────────────┐
                                      │ Fitness ≥ 300 or       │
                                      │ Max Generations?        │
                                      └─────────┬───────────────┘
                                                │
                                   ┌────────────┴────────────┐
                                   │ No                      │ Yes
                                   ▼                         ▼
                           ┌───────────────┐        ┌───────────────┐
                           │ Start Next    │        │ Training      │
                           │ Generation    │        │ Complete      │
                           └───────────────┘        └───────────────┘
```

---

## Component Architecture

### Mermaid Code
```mermaid
classDiagram
    class NEATEngine {
        +Population population
        +Config config
        +int current_generation
        +run(config_path)
        +evaluate_generation()
        +create_next_generation()
    }
    
    class Population {
        +List~Genome~ genomes
        +SpeciesSet species
        +int size
        +create_networks()
        +evaluate_fitness()
        +reproduce()
    }
    
    class Genome {
        +Dict connections
        +Dict nodes
        +float fitness
        +int species_id
        +mutate()
        +crossover(other)
    }
    
    class NeuralNetwork {
        +List~Node~ input_nodes
        +List~Node~ output_nodes
        +List~Connection~ connections
        +activate(inputs)
        +forward_pass()
    }
    
    class GameEngine {
        +List~Bird~ birds
        +List~Pipe~ pipes
        +Base base
        +int score
        +update_physics()
        +check_collisions()
        +render_frame()
    }
    
    class Bird {
        +float x, y
        +float velocity
        +float rotation
        +bool alive
        +jump()
        +move()
        +get_mask()
    }
    
    class Pipe {
        +float x
        +int height
        +int GAP
        +bool passed
        +move()
        +collide(bird)
        +draw()
    }
    
    class FitnessEvaluator {
        +float survival_bonus
        +float position_bonus
        +float progress_bonus
        +float pipe_reward
        +float collision_penalty
        +calculate_fitness(bird, events)
    }
    
    class DebugVisualizer {
        +bool show_lines
        +draw_input_lines(bird, pipes)
        +draw_network_state()
        +toggle_debug()
    }
    
    %% Relationships
    NEATEngine --> Population
    Population --> Genome
    Genome --> NeuralNetwork
    NEATEngine --> GameEngine
    GameEngine --> Bird
    GameEngine --> Pipe
    GameEngine --> FitnessEvaluator
    GameEngine --> DebugVisualizer
    NeuralNetwork --> Bird : controls
    Bird --> FitnessEvaluator : evaluated_by
```

### Text-Based Component Structure
```
NEAT Flappy Bird AI Components
├── Core Engine Layer
│   ├── NEATEngine
│   │   ├── Population Management
│   │   ├── Generation Control
│   │   └── Evolution Orchestration
│   │
│   ├── GameEngine
│   │   ├── Physics Simulation
│   │   ├── Collision Detection
│   │   └── Rendering Pipeline
│   │
│   └── FitnessEvaluator
│       ├── Reward Calculation
│       ├── Penalty Assessment
│       └── Performance Metrics
│
├── AI Components Layer
│   ├── Population
│   │   ├── Genome Collection (20)
│   │   ├── Species Management
│   │   └── Reproduction Control
│   │
│   ├── Genome
│   │   ├── Connection Genes
│   │   ├── Node Genes
│   │   └── Mutation Operations
│   │
│   └── NeuralNetwork
│       ├── Input Layer (4 nodes)
│       ├── Hidden Layer (0+ nodes)
│       └── Output Layer (1 node)
│
├── Game Objects Layer
│   ├── Bird
│   │   ├── Physics Properties
│   │   ├── Movement Control
│   │   └── Collision Bounds
│   │
│   ├── Pipe
│   │   ├── Obstacle Generation
│   │   ├── Gap Positioning
│   │   └── Movement Logic
│   │
│   └── Base
│       ├── Ground Representation
│       └── Scrolling Animation
│
└── Visualization Layer
    ├── GameRenderer
    │   ├── Sprite Drawing
    │   ├── UI Elements
    │   └── Animation System
    │
    ├── DebugVisualizer
    │   ├── Neural Input Lines
    │   ├── Network State Display
    │   └── Performance Metrics
    │
    └── ConsoleOutput
        ├── Generation Statistics
        ├── Fitness Progression
        └── Training Progress
```

---

## Neural Network Architecture

### Mermaid Code
```mermaid
graph LR
    subgraph "Input Layer"
        I1[Bird Y Position<br/>Normalized 0-1]
        I2[Gap Distance<br/>Normalized -1 to 1]
        I3[Velocity<br/>Normalized -1 to 1]
        I4[Pipe Distance<br/>Normalized 0-1]
    end
    
    subgraph "Processing"
        W1[Weight 1]
        W2[Weight 2]
        W3[Weight 3]
        W4[Weight 4]
        BIAS[Bias]
        SUM[Σ Summation]
        TANH[tanh Activation]
    end
    
    subgraph "Output Layer"
        O1[Jump Decision<br/>Range -1 to 1]
        THRESH[Threshold > 0.3]
        ACTION[Jump Action]
    end
    
    %% Connections
    I1 --> W1
    I2 --> W2
    I3 --> W3
    I4 --> W4
    
    W1 --> SUM
    W2 --> SUM
    W3 --> SUM
    W4 --> SUM
    BIAS --> SUM
    
    SUM --> TANH
    TANH --> O1
    O1 --> THRESH
    THRESH --> ACTION
    
    %% Styling
    classDef inputClass fill:#e3f2fd
    classDef processClass fill:#f3e5f5
    classDef outputClass fill:#e8f5e8
    
    class I1,I2,I3,I4 inputClass
    class W1,W2,W3,W4,BIAS,SUM,TANH processClass
    class O1,THRESH,ACTION outputClass
```

### Mathematical Representation
```
Neural Network Forward Pass:

Input Vector: X = [x₁, x₂, x₃, x₄]
where:
  x₁ = bird.y / WINDOW_HEIGHT
  x₂ = (bird.y - pipe_center) / (WINDOW_HEIGHT / 2)
  x₃ = bird.velocity / 20.0
  x₄ = (pipe.x - bird.x) / WINDOW_WIDTH

Weight Vector: W = [w₁, w₂, w₃, w₄]
Bias: b

Summation: z = Σ(wᵢ × xᵢ) + b = w₁x₁ + w₂x₂ + w₃x₃ + w₄x₄ + b

Activation: output = tanh(z)

Decision: if output > 0.3 then jump() else fall()
```

---

## NEAT Evolution Flow

### Mermaid Code
```mermaid
stateDiagram-v2
    [*] --> Initialize
    Initialize --> CreatePopulation : 20 Random Genomes
    CreatePopulation --> EvaluateGeneration
    
    state EvaluateGeneration {
        [*] --> CreateNetworks
        CreateNetworks --> RunSimulation
        RunSimulation --> CalculateFitness
        CalculateFitness --> [*]
    }
    
    EvaluateGeneration --> CheckTermination
    
    state CheckTermination {
        [*] --> FitnessCheck
        FitnessCheck --> MaxGenCheck : Fitness < 300
        FitnessCheck --> Success : Fitness ≥ 300
        MaxGenCheck --> Continue : Gen < Max
        MaxGenCheck --> Timeout : Gen ≥ Max
    }
    
    CheckTermination --> Success : Winner Found
    CheckTermination --> Timeout : Max Generations
    CheckTermination --> Evolution : Continue Training
    
    state Evolution {
        [*] --> FormSpecies
        FormSpecies --> Selection
        Selection --> Crossover
        Crossover --> Mutation
        Mutation --> NewGeneration
        NewGeneration --> [*]
    }
    
    Evolution --> EvaluateGeneration : Next Generation
    Success --> [*]
    Timeout --> [*]
    
    note right of FormSpecies
        Group genomes by
        structural similarity
        Compatibility threshold: 3.5
    end note
    
    note right of Selection
        Top 25% survive
        Elitism: 2 best per species
    end note
    
    note right of Mutation
        Weight: 60% probability
        Structure: 5-20% probability
        Bias: 40% probability
    end note
```

### Evolution Process Details
```
NEAT Evolution Cycle:

Generation N
├── Step 1: Population Evaluation
│   ├── Create neural networks from genomes
│   ├── Run game simulation for each bird
│   ├── Calculate fitness scores
│   └── Record performance statistics
│
├── Step 2: Termination Check
│   ├── Best fitness ≥ 300? → SUCCESS
│   ├── Max generations reached? → TIMEOUT
│   └── Otherwise → Continue evolution
│
├── Step 3: Species Formation
│   ├── Calculate genome compatibility
│   ├── Group similar genomes into species
│   ├── Adjust fitness for species size
│   └── Track species age and stagnation
│
├── Step 4: Selection Process
│   ├── Rank genomes by adjusted fitness
│   ├── Select top 25% as parents
│   ├── Apply elitism (preserve 2 best per species)
│   └── Remove bottom performers
│
├── Step 5: Reproduction
│   ├── Crossover between high-fitness parents
│   ├── Fill population to target size (20)
│   ├── Maintain species proportions
│   └── Create offspring genomes
│
└── Step 6: Mutation
    ├── Weight mutations (60% probability)
    │   ├── Gaussian perturbation
    │   └── Bounded to [-5, 5] range
    ├── Structural mutations (5-20% probability)
    │   ├── Add new nodes (5%)
    │   └── Add new connections (20%)
    └── Bias mutations (40% probability)
        ├── Gaussian perturbation
        └── Bounded to [-5, 5] range

Result: Generation N+1 ready for evaluation
```

This comprehensive architecture documentation provides both visual (Mermaid) and text-based representations of the system's structure, data flow, and evolutionary processes, making it suitable for both technical documentation and presentation purposes.
