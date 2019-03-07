# Language-Identifier

The report contains the link for the dataset and the details about the paper used for implementing this task. The list of languages used for training the model is present in `list of languages.pdf`.

To add more languages to the data for training, just append sentences of the new languages to `./data/dataset.csv`. Run `preprocess.py` in src directory to create a pickle file which contains the preprocessed input. Run `lang_identify.py` in src directory and give the file location as input of your chosen language.  
