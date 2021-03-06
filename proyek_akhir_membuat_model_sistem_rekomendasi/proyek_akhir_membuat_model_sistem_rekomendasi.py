# -*- coding: utf-8 -*-
"""Proyek Akhir : Membuat Model Sistem Rekomendasi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aqaUJ-UXFfp0bDk8q4dID4Z72FiR44za

Nama : Devaldi Caliesta Octadiani \
Email : devaldicaliesta20@gmail.com \
Alamat Domisili : Kabupaten Bantul, Daerah Istimewa Yogyakarta, 55187

**Data Understanding**
"""

import pandas as pd

books = pd.read_csv('books.csv')
books_tags = pd.read_csv('book_tags.csv')
ratings = pd.read_csv('ratings.csv')
tags = pd.read_csv('tags.csv')

print('books: ', books.shape)
print('books_tags: ', books_tags.shape)
print('ratings: ', ratings.shape)
print('tags: ', tags.shape)

books.info()

books_tags.info()

ratings.info()

tags.info()

books = books.drop(columns=['id', 'best_book_id', 'work_id', 'isbn', 'isbn13', 'title','work_ratings_count',
                                   'work_text_reviews_count', 'ratings_1', 'ratings_2', 'ratings_3', 'ratings_4', 'ratings_5', 
                                    'image_url','small_image_url'])

books.head()

books.isnull().sum()

books = books.dropna()
books.isnull().sum()

ratings = ratings.sort_values("user_id")
ratings.drop_duplicates(subset =["user_id","book_id"], keep = False, inplace = True) 
books.drop_duplicates(subset='original_title',keep=False,inplace=True)
books_tags.drop_duplicates(subset='tag_id',keep=False,inplace=True)
tags.drop_duplicates(subset=['tag_id','tag_name'],keep=False,inplace=True)

books_new = books[['original_title','authors','average_rating']]
books_new = books_new.astype(str)

books_new['content'] = books_new['original_title'] + ' ' + books_new['authors'] + ' ' + books_new['average_rating']

books_new.head()

books_new = books_new.reset_index()
indices = pd.Series(books_new.index, index=books_new['original_title'])

indices.head()

from sklearn.feature_extraction.text import TfidfVectorizer

# Inisialisasi TfidfVectorizer
tf = TfidfVectorizer(stop_words='english')
 
# Melakukan perhitungan idf pada data authors
tf.fit(books_new['authors']) 

# Mapping array dari fitur index integer ke fitur nama
tf.get_feature_names()

# Melakukan fit lalu ditransformasikan ke bentuk matrix
tfidf_matrix = tf.fit_transform(books_new['authors']) 

# Melihat ukuran matrix tfidf
tfidf_matrix.shape

# Mengubah vektor tf-idf dalam bentuk matriks dengan fungsi todense()
tfidf_matrix.todense()

# Membuat dataframe untuk melihat tf-idf matrix
# Kolom diisi dengan author
# Baris diisi dengan judul buku
 
pd.DataFrame(
    tfidf_matrix.todense(), 
    columns=tf.get_feature_names(),
    index=books_new.original_title
).sample(22, axis=1).sample(10, axis=0)

from sklearn.metrics.pairwise import cosine_similarity
 
# Menghitung cosine similarity pada matrix tf-idf
cosine_sim = cosine_similarity(tfidf_matrix) 
cosine_sim

# Membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa judul buku
cosine_sim_df = pd.DataFrame(cosine_sim, index=books_new['original_title'], columns=books_new['original_title'])
print('Shape:', cosine_sim_df.shape)
 
# Melihat similarity matrix pada setiap judul buku
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

# Bangun array 1 dimensi dengan judul buku
titles = books_new['original_title']
indices = pd.Series(books_new.index, index=books_new['original_title'])

# Fungsi yang mendapatkan rekomendasi buku berdasarkan skor kesamaan kosinus penulis buku
def authors_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    book_indices = [i[0] for i in sim_scores]
    return titles.iloc[book_indices]

authors_recommendations('The Hunger Games')

authors_recommendations('The Fault in Our Stars')



