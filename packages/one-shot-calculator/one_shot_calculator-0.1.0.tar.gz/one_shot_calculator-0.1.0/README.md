# One-Shot Calculator

There's a saying in some RPGs: the best debuff for your enemies is *dead*.

In edition 3.5 of Dungeons and Dragons, it is possible to make a character that does vastly more damage than you will ever need. Once you can reliably one-shot the kinds of monsters you're likely to face, you can focus the rest of your character's resources on doing other things, like not dying.

Thus, `one_shot_calculator`. This is Python package to calculate your chances of one-shotting monsters of a particular challenge rating. It can print out a histogram of your chances for one-shotting monsters, and has various other functions you can use to calculate various other useful things.

## Install

If you aren't used to using Python, the easiest way to use `one_shot_calculator` is to start from [this Google Colab notebook](https://colab.research.google.com/drive/1yWaMMJ_s-MK-ApQlY2LmhExGpLlOYQRE?usp=sharing). Just open up the notebook, try out the examples, then try modifying the code to do what you want to do.

If you are familiar with Python, you can instead install with:

```
pip install one-shot-calculator
```

## Usage

The package contains three modules and a CSV file full of monsters.

The CSV is derived from [an Excel sheet created by Giant in the Playground Forum user ezkajii](https://forums.giantitp.com/showthread.php?402179). It contains nearly all monsters published by Wizards of the Coast for D&D 3.0 and D&D 3.5.

`process_csv.py` contains functions for processing the CSV file so it can be used in the other modules.

`discrete_dists.py` contains general functions for manipulating discrete probability distributions with integer outcomes.

`one_shot_calculator_3p5.py` contains functions for manipulating probability distributions that describe your chance of one-shotting opponents in D&D 3.5. This includes distributions for damage dealt by attacks and for saving throws. You build a distribution describing your chance of one-shotting opponents, then use the function `one_shot_histogram` to make a histogram of your chance of one-shotting opponents.

## Future Extensions

That's up to you! Here are some things I could do if people are interested:

- More user-friendliness: I could set this up so you can do some rudimentary things without programming, possibly with some sort of web interface.

- More editions: I could do this for a different edition of D&D, Pathfinder, or some other appropriate RPG. In order to do that I need a CSV full of monsters for that edition. I have one for AD&D, so I might do that next.

- More examples: I'd love to include a super-high-optimization build in the examples in the Colab notebook. If someone can walk me through a standard opener for the Mailman or Cindy or the like I can add that as an example.

- More sensitivity: In order for the one-shot histograms to be fully accurate they need to take into account immunities. I could add some code to process_csv to add columns for common types of immunities so you can condition on them in your one-shot distributions.

- More versatility: If you're skeptical about one-shotting things, there is a more "normal" concept, average damage per round (DPR). It would be easy to add a DPR calculator. I could also give you an overall one-shot percentage with a given encoutner table, or even try to make a setup to answer more complicated questions like whether you can kill a monster before it kills you.

- More efficiency: This code is quite slow! It could probably be a lot faster.

- More fun stuff: Want code for specific spells? Anarchic Initiate Chaotic Surges? Other specialized things?


## Acknowledgements

This project would not be possible without ezkajii's laboriously compiled [Monster Compendium](https://forums.giantitp.com/showthread.php?402179).