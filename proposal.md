# NEAT Flappy Bird: AI-Powered Game Learning System

## Introduction

Artificial Intelligence has revolutionized the gaming industry by enabling machines to learn and adapt to complex environments through evolutionary algorithms. NEAT (NeuroEvolution of Augmenting Topologies) represents a sophisticated approach to evolving neural networks that can master challenging tasks without explicit programming. This project implements NEAT to train artificial intelligence agents to play the classic Flappy Bird game, demonstrating the power of evolutionary computation in solving reinforcement learning problems.

The Flappy Bird game presents a perfect challenge for machine learning algorithms due to its simple mechanics but deceptive difficulty. Players must time precise jumps to navigate through pipe obstacles, requiring both spatial awareness and timing precision. By applying NEAT, this project creates a population of neural networks that evolve over generations, with each network learning to control a virtual bird through trial and error. The system evaluates fitness based on survival time and distance traveled, allowing successful strategies to propagate while unsuccessful ones are eliminated.

## Objective of Project

The main objectives of our project are as follows:

**Objective 1** - Implement NEAT (NeuroEvolution of Augmenting Topologies) algorithm to evolve neural networks capable of playing Flappy Bird autonomously, demonstrating the application of evolutionary computation in game AI.

**Objective 2** - Develop a robust game environment using Pygame framework with accurate collision detection and physics simulation to provide a realistic training ground for AI agents.

**Objective 3** - Create visualization tools to analyze the evolutionary process, including fitness progression graphs and neural network topology diagrams to understand how AI strategies develop over generations.

**Objective 4** - Optimize the NEAT configuration parameters including population size, mutation rates, and speciation settings to achieve efficient learning convergence and high-performance gameplay.

**Objective 5** - Implement a persistence system to save and load trained neural networks, allowing the preservation of successful AI models and enabling further analysis or deployment.

## Abstract View

The NEAT Flappy Bird system operates through an evolutionary learning cycle where artificial neural networks compete to master the game. Each generation begins with a population of 50 neural networks, each controlling a virtual bird in the game environment. The neural networks receive three key inputs: the bird's vertical position, the horizontal distance to the next pipe, and the vertical position of the pipe gap.

As the game progresses, each neural network makes real-time decisions about when to flap (jump) based on these inputs, with the output being a binary decision threshold. Networks that survive longer and travel greater distances achieve higher fitness scores, ensuring their genetic material (neural structure and weights) has a greater chance of being selected for the next generation.

The NEAT algorithm introduces structural innovations through mutations, allowing networks to add new neurons and connections or modify existing ones. Successful strategies emerge through natural selection, with the system maintaining genetic diversity through speciation to prevent premature convergence. Over multiple generations, the AI evolves from random, ineffective behaviors to sophisticated timing and spatial awareness strategies that can successfully navigate the pipe obstacles.

## References

[1] Stanley, K. O., & Miikkulainen, R. (2002). Evolving neural networks through augmenting topologies. Evolutionary computation, 10(2), 99-127.

[2] Tech With Tim. (2019). NEAT-Flappy-Bird GitHub Repository. https://github.com/techwithtim/NEAT-Flappy-Bird

[3] NEAT-Python Documentation. https://neat-python.readthedocs.io/en/latest/

[4] Pygame Official Documentation. https://www.pygame.org/docs/

[5] Matplotlib Visualization Library. https://matplotlib.org/stable/contents.html

