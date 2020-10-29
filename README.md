# A Seldon ready model

#### This repo contains the files needed to take a particular model and build an image that can be deployed to Seldon as a Custom Model. 

## Below is a reference to what is in this repo.

### .s2i/environment
Some config that Seldon requires.

### __pycache__
Probably shouldn't be in the repo!

### model/
This contains the models to be used and built into the image.

### NoteCluster.py
This is a class that receives data, runs three models and outputs a prediction. It's where the data science happens!

### local_cont_test.py
After having got the container running locally, this script will test the app.

It sends some demo data (`notes`) to the app on port 5001 and then prints the response.

A much better test that this can be written I'm sure!

### requirements.txt
Python package requirements for the Seldon custom model

### s2i_build.sh
This file has the commands needed to build the image using the Seldon s2i builder image.
The builder image is taken from https://hub.docker.com/r/seldonio/seldon-core-s2i-python3/tags/ and the doc page is https://docs.seldon.io/projects/seldon-core/en/latest/reference/images.html

Do not run this shell script! It's just for reference.

### test_class.py
This just tests the class in NoteCluster.py

This testing should be done by the data scientist themself because if the class is not good, it obviosuly can't move on to the image build stage.
