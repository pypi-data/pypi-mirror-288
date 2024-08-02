# app.codialog.com


 Flask for the backend and Create React App for building a React application

### 1. Setting Up the Python Backend

1. **Install Flask**: 
   ```sh
   python -m pip install --upgrade pip
   ```
   
   ```sh
   pip install Flask
   ```

3. **Run the Flask Application**:
   ```sh
   python backend/app.py
   ```
   Your Flask server should be up and running at `http://127.0.0.1:5000`.



### 2. Setting Up the React Frontend

1. **Install Node.js and npm**: Ensure that Node.js and npm are installed on your system. You can download it from [nodejs.org](https://nodejs.org/).

2. **Create a React Application**:
   ```sh
   npx create-react-app frontend
   ```

3. **Navigate to the `frontend` Directory and Start the Development Server**:
   ```sh
   cd frontend
   npm start
   ```

4. **Fetch Data from Flask Backend**:
   - Open the `frontend/src/App.js` file and modify it to fetch data from the backend and display it.


5. **Proxy Requests to the Backend**:
   - To avoid CORS issues during development, you can set up a proxy in your React development server. Add the following line to your `frontend/package.json` file:


### 3. Running the Application

- Start the Flask server:
  ```sh
  python python/app.py
  ```

- Start the React development server:
  ```sh
  cd frontend
  npm start
  ```

Now, open your browser and go to `http://localhost:3000`. You should see the message "Hello from Flask!" fetched from your Flask backend displayed by your React frontend.

This setup includes all the basic steps to get a Flask and React application running together. For a real-world application, there would be additional considerations such as deployment, security, environment variables, and more complex data handling.



### 4. Budowanie i uruchamianie Dockera

```sh
sudo docker-compose up --build
```
