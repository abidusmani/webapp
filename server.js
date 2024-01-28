const express = require('express');
const axios = require('axios');
const cors = require('cors');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const md5 = require('md5'); // Import the md5 library for password hashing
const session = require("express-session");
const cookieParser = require("cookie-parser");
const jsonwebtoken= require ("jsonwebtoken");

const app = express();
const port = 4000;


app.use(bodyParser.json());


app.use(
  cors({
    origin: "http://localhost:3000",
    credentials: true,
    allowedHeaders: [
      "set-cookie",
      "Content-Type",
      "Access-Control-Allow-Origin",
      "Access-Control-Allow-Credentials",
    ],
  })
);

app.get("/", (req, res) => {
  res.json({ Message: "Server is up and running" });
});

app.use(express.json());
app.use(cookieParser());

app.use(session({
  secret: "Abid",
  saveUninitialized: true,
  resave: false,
  cookie: { maxAge: 1000 * 60 * 24 * 60 }, // Set the cookie expiry time to 24 hours
}));



// ... (your database connection setup and model definitions)


main().catch(err => console.log(err));
async function main(){
await mongoose.connect('mongodb://127.0.0.1:27017/demo');
   console.log('DB connected')
  }

  const userSchema = new mongoose.Schema({
    userId: String,
    username: String,
    password: String,
    email: String,
  });
  
  const User = mongoose.model('User', userSchema);
  const resultSchema = new mongoose.Schema({
      date: String,
      userId: String,
      Topsis_Method: String,
      matrixData: Array,
      weights: Array,
      is_benefit: Array,
      responseResult: Array,
    });
  const Result = mongoose.model('Result', resultSchema);

app.post('/register', async (req, res) => {
  try {
    const { username, password, email } = req.body;

    const userId = md5(email);
    // Generate unique userId
    console.log(userId)
    const hashedPassword = md5(password);
    console.log(hashedPassword);

    const user = new User({ userId, username, password: hashedPassword, email });

    const doc = await user.save();
    // console.log(doc);

    res.json({ message: 'User registered successfully', userId });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post("/login", async (req, res) => {
  const username = req.body.username;
  const password = req.body.password;
  const hashedPassword = md5(password);
  const authToken = jsonwebtoken.sign({ username, password:hashedPassword }, "DUMMYKEY");

  // now we will be setting cookies from server side only.
  // below cookie is httpOnly, its maxAge is 1 day
  // This cookie is valid to all the path in the domain
  res.cookie("authToken", authToken, {
    path: "/",
    maxAge: 24 * 60 * 60 * 1000,
    httpOnly: true,
  });
  res.sendStatus(200);
});

app.post('/logIn', async (req, res) => {
  const { username, password } = req.body;

  if (!password) {
    return res.status(400).json({ message: 'Password is required', success: 0 });
  }
  const hashedPassword = md5(password);
  // Check if the username and password match in the mock user database
  const user = await User.findOne({ username, password: hashedPassword });
  if (user) {
    req.session.user = user.userId;
    req.session.save();
    return res.status(200).json({ message: 'Login successful', success: 1 });
  } else {
    return res.status(401).json({ message: 'Invalid username or password', success: 0 });
  }
});

app.get("/autoLogin", (req, res) => {
  const cookie = req.headers.cookie;

  // if we received no cookies then user needs to login.
  if (!cookie || cookie === null) {
    return res.sendStatus(401);
  }

  return res.sendStatus(200);
});

app.get("/logout", (req, res) => {
  res.clear("authToken");
  return res.sendStatus(200);
});



// ... (other routes and listening)
app.post('/api/topsis-analysis', async (req, res) => {
  try {
    const userId = req.session.user;
    console.log(userId); // Assuming user ID is sent in the request body
    const jsonData = JSON.stringify(req.body);

    // Send the JSON data to the Flask backend
    const response = await post('http://127.0.0.1:5000/api/topsis-analysis', jsonData, {
      headers: { "Content-Type": "application/json" },
      withCredentials: true
    });

    // Save the response result in the database
    const responseResult = JSON.stringify(response.data);
    const result = new Result({
      date:new Date().toUTCString(),
      userId:req.session.userId,
      Topsis_Method:"Euclidian Method",
      matrixData: req.body.matrixData,
      weights: req.body.weights,
      is_benefit: req.body.is_benefit,
      responseResult,
    });
    await result.save();

    // Set the response headers and send the response to the frontend
    res.setHeader('Content-Type', 'application/json');
    res.end(responseResult);

  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});



app.post('/api/topsis-analysis2', async (req, res) => {
  try {
      const userId = req.user.userId;
      console.log(userId); // Assuming user ID is sent in the request body
      const jsonData = JSON.stringify(req.body);
  
      // Send the JSON data to the Flask backend
      const response = await post('http://127.0.0.1:5000/api/topsis-analysis2', jsonData, {
        headers: { "Content-Type": "application/json" },
      });
  
      // Save the response result in the database
      const responseResult = JSON.stringify(response.data);
      const result = new Result({
        date:new Date().toUTCString(),
        userId:req.session.user,
        Topsis_Method:"GRA Method",
        matrixData: req.body.matrixData,
        weights: req.body.weights,
        is_benefit: req.body.is_benefit,
        responseResult,
      });
      await result.save();
  
      // Set the response headers and send the response to the frontend
      res.setHeader('Content-Type', 'application/json');
      res.end(responseResult);
  
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });
app.post('/api/topsis-analysis3', async (req, res) => {
  try {
      const userId = req.user.userId;
      console.log(userId); // Assuming user ID is sent in the request body
      const jsonData = JSON.stringify(req.body);
  
      // Send the JSON data to the Flask backend
      const response = await post('http://127.0.0.1:5000/api/topsis-analysis3', jsonData, {
        headers: { "Content-Type": "application/json" },
      });
  
      // Save the response result in the database
      const responseResult = JSON.stringify(response.data);
      const result = new Result({
        date:new Date().toUTCString(),
        userId:req.session.user,
        Topsis_Method:"VIKOR Method",
        matrixData: req.body.matrixData,
        weights: req.body.weights,
        is_benefit: req.body.is_benefit,
        responseResult,
      });
      await result.save();
  
      // Set the response headers and send the response to the frontend
      res.setHeader('Content-Type', 'application/json');
      res.end(responseResult);
  
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });

app.post('/api/topsis-analysis4', async (req, res) => {
  try {
      const userId = req.user.userId;
      console.log(userId); // Assuming user ID is sent in the request body
      const jsonData = JSON.stringify(req.body);
  
      // Send the JSON data to the Flask backend
      const response = await post('http://127.0.0.1:5000/api/topsis-analysis4', jsonData, {
        headers: { "Content-Type": "application/json" },
      });
  
      // Save the response result in the database
      const responseResult = JSON.stringify(response.data);
      const result = new Result({
        date:new Date().toUTCString(),
        userId:req.session.user,
        Topsis_Method:"Topsis Method",
        matrixData: req.body.matrixData,
        weights: req.body.weights,
        is_benefit: req.body.is_benefit,
        responseResult,
      });
      await result.save();
  
      // Set the response headers and send the response to the frontend
      res.setHeader('Content-Type', 'application/json');
      res.end(responseResult);
  
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal server error' });
    }
});
app.post('/api/topsis-analysis5', async (req, res) => {
  try {
      const userId = req.user.userId;
      console.log(userId); // Assuming user ID is sent in the request body
      const jsonData = JSON.stringify(req.body);
  
      // Send the JSON data to the Flask backend
      const response = await post('http://127.0.0.1:5000/api/topsis-analysis5', jsonData, {
        headers: { "Content-Type": "application/json" },
      });
  
      // Save the response result in the database
      const responseResult = JSON.stringify(response.data);
      const result = new Result({
          date:new Date().toUTCString(),
        userId:req.session.user,
        Topsis_Method:"SAW Score",
        matrixData: req.body.matrixData,
        weights: req.body.weights,
        is_benefit: req.body.is_benefit,
        responseResult,
      });
      await result.save();
  
      // Set the response headers and send the response to the frontend
      res.setHeader('Content-Type', 'application/json');
      res.end(responseResult);
  
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal server error' });
    }
});


app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});