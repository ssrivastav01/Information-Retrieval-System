import argparse
import math
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import pickle

# Load the corpus from a JSON file
def load_corpus(json_file):
    try:
        with open('../crawler/' + json_file) as f:
            data = json.load(f)
        
        corpus = [obj['title'] for obj in data]
        urls = [obj['link'] for obj in data]

        return corpus, urls
    except Exception as e:
        print(f"Error loading corpus: {e}")
        return [], []

# Create a TF-IDF index from the corpus
def tf_idf_index(corpus):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus).toarray()
    feature_names = vectorizer.get_feature_names_out()

    tfidf_index = {}
    for i in range(len(feature_names)):
        tfidf_index[feature_names[i]] = []
        for doc in range(len(corpus)):
            if X[doc][i] > 0:
                tfidf_index[feature_names[i]].append((doc, X[doc][i]))
    
    return tfidf_index

# Convert a query to a vector using the IDF scores
def query_to_vector(query, inv_index, N):
    terms = query.split(" ")
    vector = {}
    for term in terms:
        if term not in inv_index:
            vector[term] = 0
        else:
            df = len(inv_index[term])
            idf = math.log(N / df)
            vector[term] = idf
    return vector

# Calculate the cosine similarity between a query vector and the TF-IDF index
def cos_similarity(query_vector, tfidf_index, corpus):
    scores = {}
    for i in range(len(corpus)):
        scores[i] = 0
    for term in query_vector:
        for (doc, score) in tfidf_index[term]:
            scores[doc] += score * query_vector[term]
    for doc in scores.keys():
        scores[doc] = scores[doc] / len(corpus[doc])

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# Save the URLs to a text file
def saved_urls(urls, output_file):
    with open(output_file, "w") as f:
        for url in urls:
            f.write(url + "\n")
    print('Saved urls to', output_file)

# Save the corpus to a text file
def saved_corpus(corpus, output_file):
    with open(output_file, "w") as f:
        for doc in corpus:
            f.write(doc + "\n")
    print('Saved corpus to', output_file)

# Save the index to a pickle file
def to_pickle(index, output_file):
    with open(output_file, "wb") as file:
        pickle.dump(index, file)
    print('Saved index to', output_file)

# Main function to construct the index
def main(args):
    corpus, urls = load_corpus(args.json_file)
    N = len(corpus)
    if corpus:
        index = tf_idf_index(corpus)
        to_pickle(index, args.output_file)
        saved_urls(urls, 'urls.txt')
        saved_corpus(corpus, 'corpus.txt')
    else:
        print("Corpus is empty. No index created.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inverted index construction')

    # Example command
    parser.add_argument('--json_file', type=str, default='product.json')
    parser.add_argument('--output_file', type=str, default='product.pickle')
    main(parser.parse_args())
