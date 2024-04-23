from flask import Flask, render_template, redirect, url_for, request
from query_processor import *
import sys
# Add the parent directory to the system path to import the indexer module
sys.path.append('../')
# Import the inverted index and loading functions from the indexer module
from indexer.inverted_index import *

app = Flask(__name__)
# Define the main route to render the search page
@app.route("/")
def main():
    return render_template('index.html')
# Define the search route to handle user queries
@app.route("/search",methods =['POST','GET'])
def search():
    # Check if the request method is POST or GET
    if request.method == 'POST':
         # Get the user query from the form data
        input = request.form['search']
        return redirect(url_for('result',search = input))
    else:
      # Get the user query from the query string
      input = request.args.get('search')
       # Redirect to the result route with the user query as a parameter
      return redirect(url_for('result',search = input))
# Define the result route to display the search results
@app.route("/result/<search>")
def result(search):
    # Load the inverted index from the pickle file
    index = load_index('../indexer/product.pickle')
    # Load the corpus and URLs from the text files
    corpus, urls = load_corpus_file('../indexer/corpus.txt'), load_urls('../indexer/urls.txt')
    results = ''
     # Set the number of top-K ranked results to display
    K = 4

    # search = spelling_correction(search)[:-1]
    query = modify_query(search, get_vocab(index))[:-1]
     # Convert the preprocessed query to a vector using the inverted index
    vector = query_to_vector(query, index, len(corpus))
     # Calculate the cosine similarity between the vector and the inverted index
    matches = cos_similarity(vector, index, corpus)
     # Print the preprocessed query and the top-K ranked results
    print(query)
    print(matches[:K])
    # Display the top-K ranked results on the search results page
    for i in range(K):
        results += urls[matches[i][0]] + '\n'
    # Render the search results page with the results and other variables
    return render_template('results.html', **locals())

  

# Run the Flask app
if __name__ == '__main__':
    app.run()