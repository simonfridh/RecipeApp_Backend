1. Clone the repository and make sure you have python and a terminal (Powershell for example) installed on your machine.
   
3. Navigate to the project folder (RecipeApp_BackEnd/) in your terminal
   
4. Run the following command to create a .venv folder:
   ```powershell
   python -m venv .venv
   ```
   
5. Run the following command to install required dependencies
   ```powershell
   python -m pip install -r requirements.txt
   ```
   
6. Copy the existing ```.env.example``` and rename the copy to ```.env```

    * To create an API key for OpenAI visit https://platform.openai.com (using this API key is not free and you need to add balance to your account to use it)
    
    * To sign up for an API key for USDA FoodData Central visit https://fdc.nal.usda.gov/api-guide 

    * Place the keys in their respective lines in the ```.env``` file
   ```
   OPENAI_API_KEY="YOUR API KEY HERE"
   USDA_API_KEY="YOUR API KEY HERE"
   ```
   

7. You can start the application from your terminal by running this command in the project folder (RecipeApp_BackEnd/)
8. 
   Windows:
   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```
   MacOS: (the .venv files might follow a different structure on mac. If the above command does not work try this):
   ```bash
   ./.venv/bin/python -m uvicorn app.main:app --reload
   ```

9. The server api will be hosted locally on http://127.0.0.1:8000 and Documentation can be found on http://127.0.0.1:8000/docs

10. To stop the server application press CTRL + C in the terminal window
