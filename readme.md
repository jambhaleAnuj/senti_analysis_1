# Sentiment Analysis on movie reviews

## Steps for installing the required packages

- Download Python
-  Unzip the project file
-  Open CMD in the folder. i.e the at the location of the project folder
-  Now run  ``` pip install -r requirements.txt ```  
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