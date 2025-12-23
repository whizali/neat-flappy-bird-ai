# NEAT Console Terms Glossary

## Core Metrics
- **Generation**: Evolutionary iteration/cycle number
- **Population**: Total number of neural networks being evaluated
- **Fitness**: Performance score (higher = better survival/adaptation)
- **Species**: Group of similar neural networks (prevents premature convergence)

## Fitness Statistics
- **Average fitness**: Mean performance across entire population
- **Best fitness**: Highest individual performance score
- **Stdev**: Standard deviation of fitness scores (population diversity)
- **Adjusted fitness**: Normalized fitness within species (fair competition)

## Network Architecture
- **Size (hidden_nodes, connections)**: Network complexity tuple
  - First number: Hidden neurons evolved
  - Second number: Connection links between neurons
- **Complexity**: Alternative term for network size/topology

## Species Information
- **ID**: Unique species identifier
- **Age**: Generations species has survived
- **Size**: Number of genomes in species
- **Adj fit**: Species-normalized fitness
- **Stag**: Stagnation counter (generations without improvement)

## Evolutionary Tracking
- **Genetic distance**: Similarity measure between genomes
- **Extinctions**: Species that died out
- **Innovation**: Unique mutation identifier
- **Threshold**: Success fitness requirement

## Performance
- **Generation time**: Seconds to complete one evolutionary cycle
- **Complexity**: Network structure `(input_nodes, output_nodes)`
- **Genome**: Individual neural network with genes/connections

## Genome Structure (Detailed)
- **Nodes**: Individual neurons in the neural network
  - **key**: Unique node identifier (negative = inputs, 0+ = hidden, positive = outputs)
  - **bias**: Neuron's base activation offset
  - **response**: Activation response multiplier
  - **activation**: Activation function (tanh = hyperbolic tangent)
  - **aggregation**: How inputs combine (sum = addition)

- **Connections**: Synapses linking neurons
  - **key**: Source→target node pair (e.g., (-4, 0) = input 4 → hidden 0)
  - **innovation**: Unique mutation identifier (tracks evolutionary history)
  - **weight**: Connection strength multiplier
  - **enabled**: Whether connection is active (True/False)

## Termination
- **Fitness threshold**: Minimum score required for success
- **Winner**: Best-performing genome that meets criteria
