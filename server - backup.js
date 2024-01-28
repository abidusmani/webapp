const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
const port = 4000;

app.use(cors());
app.use(express.json()); // Add this middleware to parse JSON data from the request body

app.get('/', async (req, res) => {
  res.send("Hello, world");
});

app.post('/api/topsis-analysis', async (req, res) => {
  try {
    const jsonData =JSON.stringify(req.body); // The JSON data is now available in the 'req.body' object
    console.log(jsonData)
    // console.log(req.body)

    // Send the JSON data to the Flask backend
    const response = await axios.post('http://127.0.0.1:5000/api/topsis-analysis', jsonData,{
      headers:{"Content-Type":"application/json"
    }
    })
    .then(response2 =>{
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify(response2.data));
      // console.log(response2)
    });
    
    // Set the response headers
    

    // Send the response from the Flask backend to the frontend
    // console.log(response.data) 
   
    // console.log(response.data) 
    return
  } catch (error) {
    // console.error(error)
    // res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
