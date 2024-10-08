// main.js
import { auth } from './src/firebase-auth.js';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";


// const signUp = async (email, password) => {
//   try {
//     await createUserWithEmailAndPassword(auth, email, password);
//     // Handle successful sign-up
//   } catch (error) {
//     // Handle Errors
//   }
// };


// Selecting elements
const signupButton = document.querySelector('.signup-btn');
const loginButton = document.querySelector('.login-btn');

// Signup function
signupButton.addEventListener('click', (e) => {
    e.preventDefault();

    const email = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;

    // Firebase auth sign-up
    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // User signed up successfully
            const user = userCredential.user;
            alert("Sign up successful. Welcome, " + user.email);
        })
        .catch((error) => {
            // Handle errors
            const errorCode = error.code;
            const errorMessage = error.message;
            alert(`Error: ${errorCode}, Message: ${errorMessage}`);
        });
});


// Login function
loginButton.addEventListener('click', (e) => {
  e.preventDefault();

  const email = document.querySelector('#username').value;
  const password = document.querySelector('#password').value;

  // Firebase auth login
  signInWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
          // User logged in successfully
          const user = userCredential.user;
          alert("Login successful. Welcome back, " + user.email);
      })
      .catch((error) => {
          // Handle errors
          const errorCode = error.code;
          const errorMessage = error.message;
          alert(`Error: ${errorCode}, Message: ${errorMessage}`);
      });
});
