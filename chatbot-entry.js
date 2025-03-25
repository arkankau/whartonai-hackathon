import React from "react";
import ReactDOM from "react-dom/client";
import ChatbotWidget from "ChatbotWidget.js";

window.onload = function() {
  const chatbotContainer = document.getElementById("chatbot-widget");
  console.log(chatbotContainer);
  if (chatbotContainer) {
    ReactDOM.createRoot(chatbotContainer).render(<ChatbotWidget />);
    console.log("Chatbot initialized successfully.");
  } else {
    console.error("Chatbot container not found.");
  }
}