import logging
import pickle

logging.basicConfig(level=logging.INFO)

class NoteCluster(object):


    def __init__(self):
        logging.info('INIT: Loading in the Fasttext model')
        # self.km_500 = pickle.load(open('model/km_500.p', 'rb'))
        # self.tfidf = pickle.load(open('model/tfidf.p', 'rb'))
        # self.svd = pickle.load(open('model/svd_reduc.p', 'rb'))

    def thing(self, some_data):
        explained = [int(x)*1.5 for x in some_data]

        return explained

    def predict(self, notes, meta=[]):

        logging.info(f'PREDICT: Metadata: {meta}')
        logging.info(f'PREDICT: Requests recieved: {len(notes)}')

        output = self.thing(notes)

        return output
