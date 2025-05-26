### How do we measure affinity?

We have 1️⃣ create a normalized list of keywords per author (based on the keywords of the works in which they participate) to 2️⃣ create embeddings using a Transformer language model ([MiniLM](https://huggingface.co/microsoft/MiniLM-L12-H384-uncased)). Next, 3️⃣ we have computed a similarity matrix between authors using the cosine similarity between authors' embeddings. Finally, 4️⃣ we have set the similarity of each author with itself and with its co-authors to zero and normalized the matrix.
