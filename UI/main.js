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
// const signupButton = document.querySelector('.signup-btn');
// const loginButton = document.querySelector('.login-btn');

// // Signup function
// signupButton.addEventListener('click', (e) => {
//     e.preventDefault();

//     const email = document.querySelector('#username').value;
//     const password = document.querySelector('#password').value;

//     // Firebase auth sign-up
//     createUserWithEmailAndPassword(auth, email, password)
//         .then((userCredential) => {
//             // User signed up successfully
//             const user = userCredential.user;
//             alert("Sign up successful. Welcome, " + user.email);
//         })
//         .catch((error) => {
//             // Handle errors
//             const errorCode = error.code;
//             const errorMessage = error.message;
//             alert(`Error: ${errorCode}, Message: ${errorMessage}`);
//         });
// });


// // Login function
// loginButton.addEventListener('click', (e) => {
//   e.preventDefault();

//   const email = document.querySelector('#username').value;
//   const password = document.querySelector('#password').value;

//   // Firebase auth login
//   signInWithEmailAndPassword(auth, email, password)
//       .then((userCredential) => {
//           // User logged in successfully
//           const user = userCredential.user;
//           alert("Login successful. Welcome back, " + user.email);
//       })
//       .catch((error) => {
//           // Handle errors
//           const errorCode = error.code;
//           const errorMessage = error.message;
//           alert(`Error: ${errorCode}, Message: ${errorMessage}`);
//       });
// });



document.addEventListener('DOMContentLoaded', () => {
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const navMenu = document.querySelector('.nav-menu');

    hamburgerMenu.addEventListener('click', () => {
        hamburgerMenu.classList.toggle('active');
        navMenu.classList.toggle('show');
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const loginModal = document.getElementById('loginModal');
    const loginBtn = document.querySelector('.login-btn');
    const closeBtn = document.querySelector('.close-btn');

    loginBtn.addEventListener('click', () => {
        loginModal.style.display = 'flex';
    });

    closeBtn.addEventListener('click', () => {
        loginModal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === loginModal) {
            loginModal.style.display = 'none';
        }
    });
});
//file upload
document.getElementById('uploadForm').addEventListener('submit', async function(event){
    event.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');
    
    if(fileInput.files.length === 0){//Are files selected
        alert("No files selected.");
        return;
    }

    //Loop through each selected file and append to FormData
    for(let i = 0; i < fileInput.files.length; i++){
        const file = fileInput.files[i];
        //File size check (10MB limit)
        if(file.size > 10 * 1024 * 1024){
            console.error(`File ${file.name} is too large. Maximum size is 10MB.`);
            //alert(`File ${file.name} is too large. Maximum size is 10MB.`);
            return;
        }

        //File type check(only mpeg, MP3, WAV, and MIDI)
        const validTypes = ['audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/midi'];
        if(!validTypes.includes(file.type)){
            console.error(`File ${file.name} is not a valid audio type.`);
            //alert(`File ${file.name} is not a valid audio type.`);
            return;
        }
        formData.append("files", file); //Append each file
    }

    try{
        const response = await fetch('http://localhost:8000/upload/', {
            method: 'POST',
            body: formData
        });
        const resultElement = document.getElementById('uploadResult');
        if(response.ok){
                const data = await response.json();
                console.log('Files uploaded:', data);
                //alert(`Files uploaded successfully: ${data.filenames.join(', ')}`);
        }else{
                const errorData = await response.json();
                console.error('Upload failed:', errorData.detail);
                alert(`File upload failed: ${errorData.detail}`);
        }
    }catch(error){
        console.error('Error:', error);
        //alert('An error occurred during the upload.');
    }
});


