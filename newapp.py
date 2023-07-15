import streamlit as st
import pickle
from streamlit_option_menu import option_menu
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))


def index():
    st.title("ReadSage")
    st.title("Top 50 Treding Books")
    books_per_row = 3
    rows = len(popular_df) // books_per_row
    remaining_books = len(popular_df) % books_per_row

    for row in range(rows):
        cols = st.columns(books_per_row)
        for col_idx in range(books_per_row):
            i = row * books_per_row + col_idx
            cols[col_idx].image(popular_df['Image-URL-M'].values[i])
            cols[col_idx].subheader(popular_df['Book-Title'].values[i])
            cols[col_idx].write(f"Author: {popular_df['Book-Author'].values[i]}")
            cols[col_idx].write(f"Votes: {popular_df['num_ratings'].values[i]}")
            cols[col_idx].write(f"Rating: {popular_df['avg_rating'].values[i]}")

    if remaining_books > 0:
        cols = st.columns(remaining_books)
        last_row_start_idx = rows * books_per_row
        for col_idx in range(remaining_books):
            i = last_row_start_idx + col_idx
            cols[col_idx].image(popular_df['Image-URL-M'].values[i])
            cols[col_idx].subheader(popular_df['Book-Title'].values[i])
            cols[col_idx].write(f"Author: {popular_df['Book-Author'].values[i]}")
            cols[col_idx].write(f"Votes: {popular_df['num_ratings'].values[i]}")
            cols[col_idx].write(f"Rating: {popular_df['avg_rating'].values[i]}")

def recommend():
    user_input = st.text_input("Enter a book:")
    if st.button("Recommend"):
        matching_books = []

        # Find books that contain the user input in their title
        for i, book_title in enumerate(pt.index):
            if user_input.lower() in book_title.lower():
                matching_books.append(i)

        if len(matching_books) > 0:
            recommendations = []

            # Get recommendations for matching books
            for i in matching_books:
                similar_items = sorted(list(enumerate(similarity_scores[i])), key=lambda x: x[1], reverse=True)[1:5]

                for j in similar_items:
                    item = []
                    temp_df = books[books['Book-Title'] == pt.index[j[0]]]
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

                    recommendations.append(item)

            if len(recommendations) > 0:
                st.title("Recommended Books")

                for i in recommendations:
                    st.write(f"Title: {i[0]}")
                    st.write(f"Author: {i[1]}")
                    st.image(i[2])
            else:
                st.write("No recommendations found.")
        else:
            st.write("No matching books found.")

     




def main():
    # st.markdown(
    #     """
    #     <style>
    #         .navbar {
    #             display: flex;
    #             justify-content: space-between;
    #             align-items: center;
    #             background-color: #a6000e;
    #             padding: 10px;
    #             color: white;
    #         }
    #         .nav-links {
    #             display: flex;
    #             list-style-type: none;
    #             padding: 0;
    #         }
    #         .nav-links li {
    #             margin-right: 20px;
    #         }
    #         .nav-links li a {
    #             text-decoration: none;
    #             color: white;
    #         }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )

    # st.markdown(
    #     """
    #     <div class="navbar">
    #         <span class="navbar-brand">ReadSage</span>
    #         <ul class="nav-links">
    #             <li><a href="/">Home</a></li>
    #             <li><a href="/recommend">Recommend</a></li>
    #             <li><a href="#">Contact</a></li>
    #         </ul>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )

    # sidebar for navigation
    with st.sidebar:
    
        selected = option_menu('"Welcome to ReadSage! Select a page"',
                          
                          ['Trending',
                           'Recommend'],
                          icons=['trending','trending'],
                          default_index=0)

    if selected == "Trending":
        index()
    elif selected == "Recommend":
        recommend()

if __name__ == '__main__':
    main()

