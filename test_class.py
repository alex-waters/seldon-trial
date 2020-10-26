from NoteCluster import NoteCluster

doc = ['CLAIM EDITED: Policy Holder vehicle Damage', 'hello']
results = NoteCluster().predict(doc)

print(results)
