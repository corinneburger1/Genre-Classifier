# Genre-Classifier
A genre classifier that uses machine learning techniques and Spotify song data to label songs with genres.

## Machine Learning Model
To classify songs, I use a random forest model that was trained on over a thousand songs.

## Data
To collect training data, I used thousands of songs from various Spotify playlists. Using the Spotify API, I collected over thirty attribute values for each song. Genre classifications were determined based on playlists - for example, I used a large country playlist and classified all songs in it as country. The current model is stored in a RandomForestModel.joblib under app/static/.

## Classifying Songs
Based on user queries, I use Spotify to search for possible songs and select the most closely matched song. I then collect the values for each attribute that my model was trained on. I then output a classification using the model to predict the genre based on the attribute values.

## Try It!
The app is hosted at http://corinneburger1.pythonanywhere.com/.
