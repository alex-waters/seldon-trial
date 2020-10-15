'''
This is a script with some text analysis on claims notes.
The purpose of it to test how complicated it would be to deploy this analysis using Seldon.
The code in this script is logical code, it will need refactoring to be suitable for a Seldon deployment.

In summary, the script reads in some data, searches the text for certain terms and then uses a function
to select only the words around those search terms.
It then trains a fasttext model on those text snippets and then finds word associations for an arbitrarily
written list of assets.
At the end it produces a 3d scatter plot of different words so that we can see groups of related words.
'''
import pandas as pd
import numpy
import re
import fasttext
from textblob import TextBlob
from nltk.corpus import stopwords, wordnet
from sklearn.decomposition import PCA
from plotly import graph_objects
from plotly.offline import plot

# define the search terms and read in data
QUERY_SEARCH = ['invoice for', 'receipt for', 'cost for', 'image of']
sourcedata = pd.read_csv('../DATA/multi_extract.csv')

# bit of cleaning up of unwanted text
claim_only = sourcedata.replace({'detail':{
    'Type:': '',
    'New': '',
    'Document': '',
    'Email': '',
    'Doc': '',
    'Copy Incoming': '',
    'Owner': '',
    'Desc': '',
    'Edited:': '',
    'Actioned:': '',
    'Repair invoice': '',
    'approved': '',
    'unapproved': '',
    'Referred': '',
    '[^A-Za-z\s]': '',
    'reasonable': '',
    'please': '',
    'thanks': ''
    }},
    regex=True
)


# this selects words around search terms
def word_targetter(words, window, search_words, extra_stopwords, pre=False):
    
    assert type(words) is pd.core.series.Series, 'Words must be pd.Series()'
    assert type(search_words) is list
    assert type(extra_stopwords) is list
    pre_words = '(.{2,'+str(window)+'})'
    post_words = '(.{2,'+str(window)+'})'
    if pre:
        search_term = ''
        for w in search_words:
            search_term = search_term+pre_words+w+post_words+'|'
    else:
        search_term = ''
        for w in search_words:
            search_term = search_term+w+post_words+'|'
            
    print(search_term)        # just a check, can be removed
    
    eng_stopwords = list(stopwords.words('english'))
    eng_stopwords.remove('for')
    eng_stopwords.extend(extra_stopwords)
    
    extracted = []
    for n in words.str.lower():
        blocks = re.findall(
            search_term[:-1], 
            ' '.join([x for x in n.split() if x not in eng_stopwords])
        )
        [extracted.append(x) for x in blocks if x]
    
    return set(extracted)


words_for_ft = word_targetter(
    words=claim_only['detail'].str.lower(),
    window=25,
    search_words=QUERY_SEARCH,
    extra_stopwords=['damage', 'damaged', 'payment',],
    pre=True
)

# programmatic collection of returned text snippets and transform to csv for fasttext
text_snippets = []
for i in words_for_ft:
    for j in i:
        if len(j) > 5:
            text_snippets.append(j)
pd.Series(text_snippets).to_csv('../DATA/text_snippets.csv', index=None)
# train the model on the selected text
ft_all_claim_only = fasttext.train_unsupervised(
    '../DATA/text_snippets.csv', 
    'cbow', 
    ws=10,
#     dim=3
)

# everything below this is in order to create a 3d plot to visualise groups of words
output_pca = PCA(n_components=3)
output_pca.fit(ft_all_claim_only.get_output_matrix())

# define some known assets and request their associated words from the model
assets = ['bumper', 'carseat', 'window', 'door']
selected_words = []
for a in assets:
    near_words = [x[1] for x in ft_all_claim_only.get_nearest_neighbors(a)]
    selected_words.extend(near_words)

# this is horribly written but it takes the associated words and gets them into a format for plotting
transforms = pd.DataFrame()
for w in selected_words:
    transforms = transforms.append(pd.DataFrame(
        numpy.append(
            output_pca.transform(ft_all_claim_only.get_word_vector(w).reshape(1, -1)),
            w
        )
    ).T)

# create a 3d plot of the PCA values for the words
words_fig = graph_objects.Figure(
    data=[
        graph_objects.Scatter3d(
            x=transforms[0], 
            y=transforms[1], 
            z=transforms[2], 
            mode='markers',
            marker={'size': 2},
            text=transforms[3],
        )
    ]
)

words_fig.update_layout(scene=dict(
    xaxis = dict(
         backgroundcolor='#ffffff',
         color="white",
         showbackground=True,
         zerolinecolor="white",),
    yaxis = dict(
        backgroundcolor='#ffffff',
        color="white",
        showbackground=True,
        zerolinecolor="white"),
    zaxis = dict(
        backgroundcolor='#ffffff',
        color="white",
        showbackground=True,
        zerolinecolor="white",
    )
))
plot(words_fig)     # this creates a temp file
