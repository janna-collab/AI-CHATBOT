// Listen for Enter key (with Shift+Enter for newlines) in the textarea
function handleKeyPress(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }
  
  // Send user message to the backend and process response
  function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();
    if (message === "") return;
  
    // Append user message to the chat output
    appendMessage(message, "user");
    inputField.value = "";
  
    // Display the response/loading indicator
    showResponseBar();
  
    fetch("/ask/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: message })
    })
      .then(response => response.json())
      .then(data => {
        hideResponseBar();
        appendMessage(data.answer, "bot");
      })
      .catch(error => {
        hideResponseBar();
        appendMessage("Error: Unable to get a response.", "bot");
        console.error(error);
      });
  }
  
  // Append a chat bubble to the chat output area
  function appendMessage(text, sender) {
    const chatOutput = document.getElementById("chat-output");
    const bubble = document.createElement("div");
    bubble.classList.add("chat-bubble");
    bubble.classList.add(sender === "user" ? "user-bubble" : "bot-bubble");
    bubble.textContent = text;
    chatOutput.appendChild(bubble);
    chatOutput.scrollTop = chatOutput.scrollHeight;
  }
  
  // Show the loading indicator
  function showResponseBar() {
    document.getElementById("response-bar").style.display = "flex";
  }
  
  // Hide the loading indicator
  function hideResponseBar() {
    document.getElementById("response-bar").style.display = "none";
  }
  