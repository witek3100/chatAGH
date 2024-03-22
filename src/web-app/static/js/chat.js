function ask() {
    const question = inputBox.value
    inputBox.value = ""

    updateChat(question, "user_icon.png", [])

    $(".loading-dots").show();

    sendButton.disabled = true;
    sendButton.style.backgroundColor = "#555"
    chatBox.scrollTop = chatBox.scrollHeight

    var url = `/get_response/${chatId}/${question}`
    var eventSource = new EventSource(url);
    $(".loading-dots").hide();

    var message_to_stream = updateChat('', "bot_icon.png", [])

    eventSource.onmessage = function () {
                $(".loading-dots").hide();
                 var token = event.data;
                 if (token === '<!END>') {
                     sendButton.disabled = false;
                     sendButton.style.backgroundColor = "#4CAF50";
                     chatBox.scrollTop = chatBox.scrollHeight + 100
                     eventSource.close()
                 } else {
                     message_to_stream.innerHTML += token
                 }
             };
}


function updateChat(message, agent, source) {
    const msg_box = document.createElement("div")
    msg_box.classList.add("message-box")

    const img = document.createElement("img")
    img.classList.add("icon")
    var new_class = "icon-" + agent.split('_')[0]
    img.classList.add(new_class)


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
    const txt = document.createElement("div")
    txt.classList.add("text")
    txt.innerHTML = message
    msg.appendChild(txt)

    if (source.length > 0) {
        const urls = document.createElement("div")
        urls.classList.add("urls")
        for (let i = 0; i < source.length; i++) {
            const url = document.createElement("a")
            url.href = source[i]
            url.innerText = source[i]
            urls.appendChild(url)
        }
        msg.appendChild(urls)
    }

    msg_box.appendChild(msg)
    chatMessages.appendChild(msg_box)

    return txt
}

async function getImageURL(agent) {
    const response = await fetch(`/get_asset/${agent}`);
     return await response.text();
  }