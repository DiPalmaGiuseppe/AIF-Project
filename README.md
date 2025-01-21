## AIF-Project
# University of Pisa "Artificial Intelligence Fundamentals" course project.
### Giuseppe Di Palma, Daniel Thomas Wahle

## Abstract

This project focuses on the development of an advanced combat agent for the MiniHack environment, a research platform based on the roguelike game NetHack. Two distinct approaches are implemented: the first uses a first-order logic (FOL) knowledge base implemented in Prolog, while the second relies on reinforcement learning with TorchBeast. The FOL-based agent uses predefined rules and decision-making logic, while the RL agent applies a Convolutional Neural Network that trains through trial-and-error interactions in the environment. The evaluation of the agents across a series of combat scenarios shows that the FOL-based agent achieves superior performance in efficiency and success rate due to its reliance on prior knowledge. However, the RL-based agent demonstrates greater flexibility and scalability, with the potential to surpass its counterpart with extended training and parameter tuning. The results emphasize the trade-offs between knowledge-based and data-driven approaches in AI and point to hybrid methods as a way to combine the strengths of both approaches.

The fol-agent part of the project has been written in **Python 3.9**.

## FOL Setup 💻
Create a virtual environment, and install the dependecies (in fol_results directory):

```
python3 -m venv minihack

source minihack/bin/activate

pip install -r requirements.txt
```

or use the dockerfile that create a ready-to-use environment in which run the tests.

## RL Setup
For the TorchBeast we used the dockerfile proposed in the minihack repository https://github.com/facebookresearch/minihack/tree/main/docker
After that we register the environment using the file custom_skills_combat.py in torchbeast_results directory


## Contacts ✨

 - Giuseppe Di Palma - g.dipalma6@studenti.unipi.it
 - Daniel Wahle - d.wahle@studenti.unipi.it