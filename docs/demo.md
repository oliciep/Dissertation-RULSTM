Demo of RU-LSTM software
========================

The basics of action anticipation architecture and software will be demosntrated using RU-LSTM package as an example. The general ideas apply equally to AVT software, which is however more complex.

Main software modules
---------------------

- main.py contains the main driver functions which set up the model, data loader and evaluation module and then run the training / validation using these modules.
- dataset.py handles the loading of the main database as well as various CSV files which contain clip definitions and annotations.
- models.py sets up NN modules to run the component parts of RU-LSTM architecture and connects them together.

Main training driver
--------------------

We will dive in in more detail into how training algorithm works. First main.py main() function creates
- RU-LSTM model
- data loader
- optimiser

It then calls trainval() function which runs the simulation as follows
for each epoch it alternates between training and validation
- creates performance (loss and accuracy) meters
- in training mode enables gradient calculation
- then iterates throuhg batches of training samples and
	-- applies forward step of the model to generate predictions
	-- calculates and logs loss and other accuracy measures
	-- in training mode it further
		--- resets gradient
		--- recalulates them by calling backward() function
		--- updates weights and biases by calling optimiser step() function

Example script for running simulation: runpast.sh
-------------------------------------------------

- run pre-training, training, validation for all modalities
- run fusion training followed by validation

Example output: runexample.log
------------------------------

- output of training
- table produced by validation, which contains info that was used to create results tables and graphs

