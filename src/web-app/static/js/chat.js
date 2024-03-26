function ask() {
    if (sendButton.disabled === true) {
        return 0
    }

    const error_mesasge = "Podczas generowania odpowiedzi wystąpił błąd, spróbuj ponownie ... "

    sendButton.disabled = true;
    sendButton.style.backgroundColor = "#555"

    const question = inputBox.value
    inputBox.value = ""

    updateChat(question, "user_icon.png", [])

    var url = `/get_response/${chatId}/${question}`
    var eventSource = new EventSource(url);

    var message_to_stream = updateChat('', "bot_icon.png", [])

    chatBox.scrollTop = chatBox.scrollHeight + 100

    eventSource.onmessage = function () {
        $(".loading-dots").hide();
        var content = event.data;
        if (content === '<!ERROR>') {
            message_to_stream.innerHTML = "<b style='color: red'>" + error_mesasge + "</b>"
            eventSource.close()
            setTimeout(enableButton, 100)
        }
        else if (content === '<!END>') {
            eventSource.close()
            enableButton()
        } else {
            message_to_stream.innerHTML = content;
        }
        chatBox.scrollTop = chatBox.scrollHeight + 100
    };

}

function enableButton() {
    sendButton.disabled = false;
    sendButton.style.backgroundColor = "#4CAF50";
}


function updateChat(message, agent, source) {

    console.log('updateing')

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

    if (message === '') {
        const loading_dots = document.createElement("div")
        loading_dots.classList.add("loading-dots")
        loading_dots.innerText = '. . .'
        txt.appendChild(loading_dots)
    } else {
        txt.innerHTML = message
    }
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