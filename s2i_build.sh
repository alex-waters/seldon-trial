# Don't run this shell script!
# This is just an example of how to build the image for Seldon
# The name 'note-cluster' is the name for a specific case

# TO DO - have a variable for the image name taken from a config file / repo name / branch name
# TO DO - use the latest builder image from Seldon, not always 1.4.0

s2i build . seldonio/seldon-core-s2i-python3:1.4.0-dev note-cluster
docker commit
docker commit 8b4
docker tag note-cluster harbor.k8s-tools.digital.coveahosted.co.uk/galileo_engineers_test/note-cluster
docker push harbor.k8s-tools.digital.coveahosted.co.uk/galileo_engineers_test
