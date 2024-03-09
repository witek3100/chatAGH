const inputBox = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-container")
 inputBox.addEventListener("keyup", (event) => {
   if (event.key === "Enter") {
     ask()
   }
 });
sendButton.addEventListener("click", ask);
 function ask(event) {
   event.preventDefault();

   const formData = new FormData(chatForm);

   sendButton.disabled = true;
   sendButton.style.backgroundColor = "#555"

   $.ajax({
     url: "123123",
     type: "POST",
     data: formData,
     processData: false,
     contentType: false,
     success: function(chat) {
       updateChat(chat)
       sendButton.disabled = false;
       sendButton.style.backgroundColor = "#4CAF50";
       },
     error: function(jqXHR, textStatus, errorMessage) {
       console.error("Error submitting form:", errorMessage);
       alert(errorMessage)
       sendButton.disabled = false;
       sendButton.style.backgroundColor = "#4CAF50";
     }
   });
 }
 function updateChat(chat) {
   const newMessage = document.createElement("div")
    newMessage.classList.add("message")
    newMessage.textContent = chat['answer']
    chatBox.appendChild(newMessage)
 }