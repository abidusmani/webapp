const express = require('express');
const axios = require('axios');
const cors = require('cors');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const md5 = require('md5'); // Import the md5 library for password hashing
const session = require("express-session");
const cookieParser = require("cookie-parser");

const app = express();
const port = 4000;
// app.use(cors());
app.use(express.json());
app.use(cookieParser());
app.use(bodyParser.json());

app.use(cors({
  origin:"http://localhost:3000",
  credentials:true
}));
 
// ap.uspe(express.json());
// app.use(cookieParser());


app.use(session({
  cookieName:"AbidUSmani",
    secret: "Abid",
    saveUninitialized: true,
    resave: false,
    httpOnly: false,
    secure: true,
    ephemeral : true

}));

const { v4: uuidv4 } = require('uuid'); // Import uuid library




mongoose.connect('mongodb://127.0.0.1:27017/demo')
  .then(() => console.log('DB connected'))
  .catch((err) => console.error('Error connecting to DB:', err));

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

    const userId =md5(email);
    // Generate unique userId
    console.log(userId)
    const hashedPassword = md5(password);

    const user = new User({ userId, username, password: hashedPassword, email });

    const doc = await user.save();
    // console.log(doc);

    res.json({ message: 'User registered successfully', userId });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});



app.post('/logIn', async (req, res) => {
  try {
    const { username, password } = req.body;
    req.session.user=null;

    // Hash the password using MD5 before comparing it in the database
    const hashedPassword = md5(password);

    // Find the user in the database
    // const user = await User.findOne({ username, password: hashedPassword });

    console.log("Creds: "+username+" pwd: "+ hashedPassword)
    const user = User.findOne({ username:username, password: hashedPassword }).exec();
    user.then((data) => { 
      // console.log("123");
      req.session.user=data.userId
      // console.log(user)
      // console.log(data.email)
      // console.log(data.password)
      console.log(req.session.user)
      if (data) {
      
      res.json({ message: 'Login successful', userId: data.userId , success:1}); // Send userId along with response
    } else {
      res.status(401).json({ error: 'Invalid username or password', success:0 });
    }
  });
} catch (error) {
  console.error(error);
  res.status(500).json({ error: 'Internal server error',success:0 });
}
});

app.get('/checkSession',  (req, res) => {
  userId = req.session.user;
  // console.log("ghjk "+userId);
  // console.log(req.session.user);
  if(userId) return res.setHeader('Content-Type', 'application/json').end(userId);
  else return res.setHeader('Content-Type', 'application/json').end("Null");
});


app.get('/logOut', async (req, res) => {
    try {
       req.session.user=0;
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Internal server error' });
      }
    });


// CRUD - Read
app.get('/demo', async (req, res) => {
  try {
    const users = await resultSchema.find({userId:req.session.user});
    res.json(users);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});
// app.use(bodyParser.json());
// app.use((req, res, next) => {
//     req.user = { userId: req.header('authenticatedUserId') }; // Replace with actual user ID
//     next();
//   });

// app.post('/api/topsis-analysis', async (req, res) => {
//     try {
//         const userId = req.body.userId;
//       const { userId, matrixData, weights, is_benefit } = req.body; // Extract the data from req.body
  
//       // Send the JSON data to the Flask backend
//       const response = await axios.post('http://127.0.0.1:5000/api/topsis-analysis', {
//         matrixData,
//         weights,
//         is_benefit,
//       }, {
//         headers: {"Content-Type": "application/json"},
//       });
  
//       // Create a new document in the database to store the received data, response result, and user ID
      
  
//       // Send the response from the Flask backend to the frontend
//       res.setHeader('Content-Type', 'application/json');
//       res.end(JSON.stringify(response.data));
//       const resultData = new Result({
//         userId,
//         matrixData,
//         weights,
//         is_benefit,
//         responseResult: response.data, // Save the response result
//       });
  
//       // Save the document to the database
//       await resultData.save();
//     } catch (error) {
//       console.error(error);
//       res.status(500).json({ error: 'Internal server error' });
//     }
//   });


app.post('/api/topsis-analysis', async (req, res) => {
    try {
      // console.log("123qwe "+req.session.user);
        // if(!req.session.user){
        //     res.setHeader('Content-Type', 'application/json');
        //     res.end("Error")
        //     return
        // }
        
      const userId = req.session.user;
      console.log(userId); // Assuming user ID is sent in the request body
      const jsonData = JSON.stringify(req.body);
  
      // Send the JSON data to the Flask backend
      const response = await axios.post('http://127.0.0.1:5000/api/topsis-analysis', jsonData, {
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
      const userId = req.session.user;
        console.log(userId); // Assuming user ID is sent in the request body
        const jsonData = JSON.stringify(req.body);
    
        // Send the JSON data to the Flask backend
        const response = await axios.post('http://127.0.0.1:5000/api/topsis-analysis2', jsonData, {
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
      const userId = req.session.user;
        console.log(userId); // Assuming user ID is sent in the request body
        const jsonData = JSON.stringify(req.body);
    
        // Send the JSON data to the Flask backend
        const response = await axios.post('http://127.0.0.1:5000/api/topsis-analysis3', jsonData, {
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
      const userId = req.session.user;
        console.log(userId); // Assuming user ID is sent in the request body
        const jsonData = JSON.stringify(req.body);
    
        // Send the JSON data to the Flask backend
        const response = await axios.post('http://127.0.0.1:5000/api/topsis-analysis4', jsonData, {
          headers: { "Content-Type": "application/json" },
        });
    
        // Save the response result in the database
        const responseResult = JSON.stringify(response.data);
        const result = new Result({
          date:new Date().toUTCString(),
          userId:req.session.userId,
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
      const userId = req.session.user;
        console.log(userId); // Assuming user ID is sent in the request body
        const jsonData = JSON.stringify(req.body);
    
        // Send the JSON data to the Flask backend
        const response = await axios.post('http://127.0.0.1:5000/api/topsis-analysis5', jsonData, {
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
