# Sentiment Analysis on movie reviews

## Steps for installing the required packages

- Download Python
-  Unzip the project file
-  Open CMD in the folder. i.e the at the location of the project folder
-  Now run  ``` pip install -r requirements.txt ```  
  

<br>

- ### TO GENERATE YOUTUBE API KEY 
- https://developers.google.com/youtube/v3/getting-started
- Go to the above link and follow the instructions to get the youtube api key used to fetch the comments to get the People's reviews of movie before release
- COPY the api key and paste it in the ```.env``` file present in the project.  

<br>

-  Once all the above steps are done. Run the following command
-  ``` python app.py ```
-  Now copy the IP address displayed and paste it in the terminal
  
<br>

## Steps to use the program

- Once all the above steps are complete. You will have following window

<br>

![alt text](first_image.png)

<br>

- Now Go to the <a href="https://www.imdb.com/">IMDB site </a> and search for the movie you want the sentiment analysis for. 

- Copy the link of that page. But remember <b> Only Copy the link till the code </b>.
- For example: For Gangs of Wasseypur the link will be https://www.imdb.com/title/tt1954470

![alt text](for_link.png) 

<br>

### Now paste the link in our sentiment analysis website and click on "Analyze Sentiment"

![alt text](link_pasted.png)

## Result will be as follows:
![alt text](senti_screenshot.png)



## Solving the Bug
  ### Some times it may happen that after pasting the link and clicking on the analyse button. It may not work giving the following error.
  ![alt text](error.png) 

### In such cases. Try one the following steps
- Try 2-3 times by again pasting the link and clicking on "Analyze Sentiment" Button
- Restart the app 
- Try with another movie (Since for some movies the database may not have created. )




## Polarity distribution
The polarity distribution you're referring to is a visualization of the sentiment polarity scores of reviews. Polarity is a value that measures the sentiment of a piece of text, specifically how positive or negative the text is. Here's a breakdown of how it works:

What is Polarity?
Polarity is a measure that ranges from -1 to 1:

- +1 represents a completely positive sentiment (e.g., "I love this movie!").

- 0 represents a neutral sentiment (e.g., "The movie was okay.").

- -1 represents a completely negative sentiment (e.g., "I hated this movie!").


## Icon's on Plotly Graph
Plotly graphs come with several interactive icons and controls that make them easy to explore and manipulate. These controls, or modebar icons, are displayed at the top-right corner of the graph by default when you render a Plotly chart in a Jupyter notebook, web application, or standalone HTML page. Here's an overview of the most common icons and what they do:

### 1. Zoom (Magnifying Glass) Icon
- Icon: A magnifying glass or zoom icon.

- Function: Allows you to zoom in and out on the plot.

- Usage: Click and drag on the graph to select an area to zoom into. To zoom out, you can either click the "Zoom Out" icon or double-click the graph.

### 2. Pan (Hand) Icon
- Icon: A hand symbol.

- Function: Allows you to pan or move around the graph.

- Usage: Click and hold the hand icon, then drag the graph to explore different areas. This is useful for large datasets when you need to navigate without changing the zoom level.

### 3. Zoom In / Zoom Out (Plus and Minus) Icons
- Icons: A plus (+) and minus (-) sign.

- Function: Allows you to zoom in and out incrementally.

- Usage: Clicking the "+" sign zooms in, and clicking the "-" sign zooms out. This provides a quick way to change the zoom level without manually dragging.

### 4. Reset Axis (Home) Icon
- Icon: A house or home icon.

- Function: Resets the graph’s view to its original state (i.e., zoomed out to the default axis ranges).

- Usage: Clicking this button will return the plot to its initial zoom level or position before any panning or zooming was done.

### 5. Download Image (Camera) Icon
- Icon: A camera symbol.

- Function: Allows you to download the graph as an image.

- Usage: Click this icon to download the graph as a static image (PNG, JPEG, SVG, or PDF). This is useful for saving a snapshot of the chart for presentations or reports.



### 6. Select / Lasso / Box Select (Brush) Icons
- Icons: Lasso or box symbol.

- Function: These icons enable different selection modes, where you can interactively select subsets of data in the plot.

- Box Select: Click and drag to draw a rectangular box around the area of interest.

- Lasso Select: Click and drag to freely select an irregular region.

- Usage: These icons allow for interactive data selection, where you can select points within the plot and see them highlighted. This is especially useful when working with scatter plots.

### 7. Compare Data (Compare) Icon
- Icon: A "compare" or "overlapping rectangles" symbol (more common in more advanced plots).

- Function: Allows for comparing data in the plot or viewing multiple sets of data simultaneously.

- Usage: This is often used for comparing multiple data series by enabling or disabling them from view.

### 8. Hover Data / Tooltip Icon
- Icon: Typically represented by an "i" for information.

- Function: Displays detailed data for specific points in the graph when you hover over them.

- Usage: Hovering over data points on the graph will display tooltips with additional information about the point (e.g., values or categories). This is especially useful for interactive visualizations.

### 9. Toggle Spike Lines Icon
- Icon: Typically represented by a line with a vertical spike, or sometimes a small line graph icon with spikes.

- Function: Allows users to toggle the visibility of spike lines (also known as spike traces or hover lines) that appear when hovering over a data point. Spike lines help in visualizing the relationship between the hovered data point and the axes or grid lines of the graph.

- Usage:

  -  When activated, spike lines appear on the chart to visually connect a specific data point with the chart axes, making it easier for users to interpret the value of the point.

  - The spike lines are typically vertical (connecting the point to the y-axis) or horizontal (connecting the point to the x-axis) and may be present in both scatter plots and line charts.

  - This toggle allows users to show or hide the spike lines, depending on their preference for a clearer or less cluttered view of the chart.


### 10. Autoscale Icon
- Icon: Typically represented by a magnifying glass or two arrows forming a circle, often symbolizing automatic scaling or zooming.

- Function: Automatically adjusts the scale or zoom level of the graph to fit the data within the viewable area. The autoscale function ensures that all data points or elements of the chart are visible, without the user needing to manually adjust the zoom or axis ranges.

- Usage:

  - When enabled, autoscale dynamically adjusts the axis limits (both x and y axes) based on the data being displayed, ensuring that all data points fit within the chart without clipping or distortion.

  - This is particularly useful when the data range is changing or unknown, as it helps the graph adapt to varying data sets, making the visualization easier to interpret.




## How Keywords in positive and negative movies are calculated. How the alogrithm works. And why sometimes it gives non sensical words.

The keywords in positive and negative movie reviews are calculated based on the words that appear most frequently in the reviews, with a few processing steps to filter out non-informative or irrelevant words. Here’s a breakdown of how the algorithm works and why it might sometimes generate non-sensical words:

### Steps for Calculating Keywords:
Text Cleaning:

Before processing the reviews, stop words (common words like "the", "and", etc.) are removed using the NLTK stopwords list. This ensures that the focus remains on significant words.

Tokenization:

Each review is split into individual words (tokens) using NLTK’s word_tokenize() function. This breaks down the text into manageable units, such as words and punctuation.

Lowercasing:

All words are converted to lowercase to ensure uniformity (e.g., "Great" and "great" are treated as the same word).

Filtering Alphanumeric Words:

The algorithm filters out non-alphanumeric tokens (e.g., punctuation marks, numbers), so only meaningful words are processed.

Word Frequency Calculation:

After tokenizing and filtering the words, the algorithm calculates how often each word appears across the reviews using Counter from Python’s collections module. This gives a frequency distribution of words.

Extracting the Most Common Words:

The algorithm then extracts the 10 most frequent words (the most common ones) from the positive and negative reviews separately.

Categorizing by Sentiment:

The words that occur most often in the positive reviews are considered the "positive keywords," while those in negative reviews are considered the "negative keywords." These keywords are essentially the words that appear most frequently in the sentiment-labeled reviews.

Displaying Results:

The 10 most frequent words (or "keywords") are displayed as the final output for both positive and negative sentiment reviews.

### Why Sometimes Non-Sensical Words Are Generated:
The algorithm relies heavily on frequency counting, but this method has some limitations that can cause nonsensical words to appear as keywords. Here are the main reasons why:

Irrelevant Words in the Dataset:

If a movie review contains many repeated informal words, exclamations, or typos, these may become frequent tokens even though they don’t add value to the sentiment analysis. For instance, words like "wow" or "yay" might be flagged as positive keywords, but they are not necessarily informative.

Handling of Named Entities:

If the named entities (such as character names, places, or movie titles) are not handled correctly, they may be included in the final keyword list. For instance, a review may mention a movie title repeatedly, and the algorithm might incorrectly treat the title as a significant keyword.

Lack of Contextual Filtering:

The algorithm does not use any advanced semantic understanding or context to filter out irrelevant terms. For example, words like "love" or "great" are often frequent, but in some cases, they might be used sarcastically or in a neutral context, leading to skewed results.

Tokenization Issues:

Tokenization can sometimes cause problems when reviews contain non-standard characters, abbreviations, or combined words. For example, "can't" might get tokenized as "ca" and "n't," leading to odd frequency counts.

Absence of Fine-Grained NLP Techniques:

The algorithm doesn’t use part-of-speech tagging to better understand the role of words in sentences. As a result, frequent adjectives or verbs might appear as keywords even when they don’t contribute much to the sentiment.

Overlooking Phrase Structure:

The algorithm looks at single words rather than phrases or bigrams/trigrams, meaning that it might miss context-rich phrases that could better represent the sentiment (e.g., "highly recommend" might be more informative than just "recommend").