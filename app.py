import streamlit as st
import preprocesser
import helper 
import matplotlib.pyplot as plt


st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file..")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocesser.perprocess(data)
    st.dataframe(df)

    #fetch unique users

    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages ")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total media shared")
            st.title(num_media_messages)
        with col4:
            st.header("Total number of links shared")
            st.title(num_links)

        #finding the busiest user in the group(Group level)
        if selected_user == 'Overall':
            st.title("Most bussy users")
            x,new_df = helper.most_busy_user(df)
            fig,ax = plt.subplots()
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        st.title("Most frequently use words")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis.")
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head())
            st.pyplot(fig)