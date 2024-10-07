// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyBzSZYjkmHk9qGHfBWj2M5L888yrXFYc-I",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "tune2sheets",
    // storageBucket: "YOUR_STORAGE_BUCKET",
    // messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    // appId: "tune2sheets",
    //other configs
  };

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth };
