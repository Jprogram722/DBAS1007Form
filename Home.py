# This form will be for the DBAS1007 final project

import streamlit as st
from createDB import connectDB, insertIntoDB


def setToNone(inputDict: dict) -> dict:
    for key in inputDict.keys():
        if (inputDict[key] == ''):
            return None


def main():
    try:
        conn, c = connectDB(
            st.secrets["DRIVER_NAME"], st.secrets["SERVER_NAME"], st.secrets["DATABASE"])
        print("Connected to database")
    except:
        raise Exception("Couldn't connect to database")

    st.set_page_config(
        page_title="Stock Info App (Home)",
    )

    st.title("Favourite Movie Form")
    st.subheader("Test")

    with st.form(key="myForm"):
        st.subheader("About You")
        colf, coll = st.columns(2)
        with colf:
            user_fname = st.text_input(
                label="Your First Name:"
            )
        with coll:
            user_lname = st.text_input(
                label="Your Last Name:"
            )
        user_age = st.number_input(
            label="Your Age:",
            step=1
        )
        user_gender = st.selectbox(
            label="Your gender:",
            options=("Male", "Female", "Other")
        )
        user_nationality = st.text_input(
            label="Your Nationality:",
        )
        st.subheader("About Your Favourite Movie")
        movie_title = st.text_input(
            label="Movie Title"
        )
        movie_genre = st.text_input(
            label="Movie Genre"
        )
        movie_year = st.number_input(
            label="Movie Release Year",
            step=1
        )
        movie_studio = st.text_input(
            label="Who Produced The Movie"
        )
        movie_location = st.text_input(
            label="Where Was The Movie Produced"
        )
        col_leadf, col_leadL = st.columns(2)

        with col_leadf:
            movie_leadf = st.text_input(
                label="Lead Actors First Name"
            )
            movie_directf = st.text_input(
                label="Directors First Name"
            )

        with col_leadL:
            movie_leadL = st.text_input(
                label="Lead Actors Last Name"
            )
            movie_directl = st.text_input(
                label="Directors Last Name"
            )

        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            movie = {
                "title": movie_title.lower(),
                "genre": movie_genre.lower(),
                "year": movie_year,
                "studio": movie_studio.lower(),
                "location": movie_location.lower(),
                "directorF": movie_directf.lower(),
                "directorL": movie_directl.lower(),
                "leadF": movie_leadf.lower(),
                "leadL": movie_leadL.lower()
            }

            user = {
                "fname": user_fname,
                "lname": user_lname,
                "age": user_age,
                "gender": user_gender,
                "nationality": user_nationality
            }

            movie = setToNone(movie)
            user = setToNone(user)

            if (movie != None and user != None):
                insertIntoDB(conn, c, movie, user)
            else:
                st.error("The form was not filled out completly")


if __name__ == "__main__":
    main()
