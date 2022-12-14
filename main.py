import pandas as pd
from chart import generate_charts as generate_charts
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import sys
import subprocess

app = FastAPI()   # API instance
# Introduce as parameter the file to be open as follow '/api?path=path_to_csv'
@app.get("/api")
def assign_variables(path='./datasets/data.csv'):
  # Read the CSV
  data = pd.read_csv(path)
  # Define the first row as titles
  titles = list(data.head(0))
  # Initialize head_options
  head_options = ''
  # Generate string for the selection menu
  for title in titles:
    # Add into the same string the html instruction to generate the options
    head_options += f'<option value="{title}">{title}</option>'

  # All the HTML content to be displayed
  html_content = f'''
  <html>
    <body>
      <p>CSV to Chart</p>
        <form action='/chart'>
          <label for="path">CSV File:</label><br>
          <select name="path"><br>
            <option value="{path}">{path}</option><br>
          </select><br><br>

          <label for="column1">Identifier</label><br>
          <select name="head_selection_1"><br>
            {head_options}
          </select><br><br>
          
          <label for="head_selection_2">Values:</label><br>
          <select name="head_selection_2"><br>
            {head_options}
          </select><br><br>

          <label for="type_chart">Type Chart:</label><br>
          <select name="chart_selection"><br>
            <option value="bar chart">bar chart</option><br>
            <option value="pie chart">pie chart</option><br>
          </select><br><br>

          <input type="submit" value="Submit"><br>
        </form>
    </body>
  </html>
  '''
  return HTMLResponse(content=html_content,status_code=200) # Return the html content with http signal all is good


# Funtion in charge to perform validation on the entry and
@app.get("/chart")
def return_chart(head_selection_1,head_selection_2,chart_selection,path):
  # Open and read the specified file
  data = pd.read_csv(path)
  # Variable assignation from the API or the command line
  column1 = head_selection_1 
  column2 = head_selection_2 
  type_chart = chart_selection

  value1 = list(data[column1])
  value2 = list(data[column2])
  # Call the function to generate the chart in format jpg
  chart = generate_charts(type_chart,value1,value2,column1,column2)
  print(chart)                          # Print the path to the chart file
  if __name__ == '__main__':            # Validate if the execution is trough command line or the API
    return chart                        # If its command line just return the path to the chart file
  else:
    return FileResponse(chart)          # If its API will return the entire chart file


# Function to be executed by the terminal instead of the web api
def run():
    print(len(sys.argv))
    # Validate if there isn`t a csv file as parameter
    if len(sys.argv) >= 2:
      path = sys.argv[1]          # If there is a parameter, then the name is assigned to path
    else:
      path='./datasets/data.csv'  #As default it show an example dataset
    
    print(path)

    if len(sys.argv) >= 3:
      chart_selection = str(sys.argv[2]).lower()   
    else:
      # Request to the user introduce a type of chart
      chart_selection = input(f'\n\tFile Name: {path}\n\tChoose your type of chart \n\tBar chart\tPie chart\n    =>    ').lower()



    # Validation of the entry information
    if ('bar' not in chart_selection) and ('pie' not in chart_selection):
        print(f'\n\tInvalid selection {chart_selection}')    # In case information is invalid, the funtion will start again
        run()
    if 'bar' in chart_selection:          # Validate that there is a text bar
        type_chart = 'bar'
    if 'pie' in chart_selection:          # Validate that there is a text pie
        type_chart = 'pie'

    # If there is an column selection into the command, this are introduced as parameter
    if len(sys.argv) == 5:
      head_selection_1 = sys.argv[3]
      head_selection_2 = sys.argv[4]
    else:
      #Open and read the csv
      data = pd.read_csv(path)
      # Define the first row as titles
      titles = list(data.head(0))
      # Show and request to the user the columns to be filtered
      print(f'\n\tChoose the columns to filter\n')

      n=0
      for title in titles:
        print(f'{n} : {title}')
        n+=1

      selection_1 = int(input('\nIdentifier    =>    '))
      selection_2 = int(input('\nValues        =>    '))

      if selection_1 > n or selection_1 < 0 or selection_2 > n or selection_1 < 0:
        print('Selection not valid\n')
        run()

      head_selection_1 = titles[selection_1]
      head_selection_2 = titles[selection_2]

      print(f'Identifier: {head_selection_1}')
      print(f'Values: {head_selection_2}')

    # Call the same function as the API to return the chart file
    chart_jpg = str(return_chart(head_selection_1,head_selection_2,chart_selection,path))
    # Execute a command line to open the chart 
    subprocess.run(["eog", f"{chart_jpg}"])
    
# Execution if its running from the terminal
if __name__ == '__main__':
  run()