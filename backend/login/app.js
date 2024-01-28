// import React, { useState } from 'react';
// import axios from 'axios';

// const App = () => {
//   const [username, setUsername] = useState('');
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');

//   const handleSignUp = async () => {
//     try {
//       const response = await axios.post('/api/users/', {
//         username,
//         email,
//         password,
//       });
//       console.log('User created:', response.data);
//     } catch (error) {
//       console.error('Error signing up:', error);
//     }
//   };

//   return (
//     <div>
//       <h1>Signup Page</h1>
//       <input
//         type="text"
//         placeholder="Username"
//         value={username}
//         onChange={(e) => setUsername(e.target.value)}
//       />
//       <input
//         type="email"
//         placeholder="Email"
//         value={email}
//         onChange={(e) => setEmail(e.target.value)}
//       />
//       <input
//         type="password"
//         placeholder="Password"
//         value={password}
//         onChange={(e) => setPassword(e.target.value)}
//       />
//       <button onClick={handleSignUp}>Sign Up</button>
//     </div>
//   );
// };

// export default App;
