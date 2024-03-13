function ask(event) {
  event.preventDefault();

  const formData = new FormData(chatForm);
  updateChat(inputBox.value, "user")

  $(".loading-dots").show();

  sendButton.disabled = true;
  sendButton.style.backgroundColor = "#555"

  chatBox.scrollTop = chatBox.scrollHeight

  $.ajax({
    url: chatId,
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function(chat) {
        updateChat(chat["answer"], "bot")
        sendButton.disabled = false;
        sendButton.style.backgroundColor = "#4CAF50";
        $(".loading-dots").hide();
        chatBox.scrollTop = chatBox.scrollHeight + 100
    },
    error: function(jqXHR, textStatus, errorMessage) {
        console.error("Error submitting form:", errorMessage);
        sendButton.disabled = false;
        sendButton.style.backgroundColor = "#4CAF50";
        $(".loading-dots").hide();
    }
  });
}

function updateChat(message, agent) {
    const msg_box = document.createElement("div")
    msg_box.classList.add("message-box")

    const img = document.createElement("img")
    img.classList.add("icon")

    getImageURL(agent)
      .then(imageUrl => {
        console.log(imageUrl);
        img.src = imageUrl
      })
      .catch(error => {
        console.error(error);
      });

    msg_box.appendChild(img)

    const msg = document.createElement("div")
    msg.classList.add("message")
    msg.textContent = message
    msg_box.appendChild(msg)

    chatMessages.appendChild(msg_box)
    inputBox.value = ""
}

async function getImageURL(agent) {
    const response = await fetch(`/get_icon_url/${agent}`);
     return await response.text();
  }