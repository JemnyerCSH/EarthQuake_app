document.addEventListener("DOMContentLoaded", function () {
    // 地震通知
    fetch('/earthquake_notifications')
        .then(response => response.json())
        .then(data => {
            const notificationsContainer = document.getElementById("notifications");
            notificationsContainer.innerHTML = "";

            data.forEach(item => {
                const notification = document.createElement("p");
                notification.textContent = `${item.date} - ${item.message}`;
                notificationsContainer.appendChild(notification);
            });
        })
        .catch(error => {
            console.error('Error fetching earthquake notifications:', error);
            const notificationsContainer = document.getElementById("notifications");
            notificationsContainer.innerHTML = "無法獲取地震通知，請稍後再試。";
        });
});

// 加載新問題
function loadNewQuestion() {
    fetch('/load_game_question')
        .then(response => response.json())
        .then(data => {
            const questionContainer = document.getElementById("question");
            questionContainer.innerText = data.question;

            const optionsContainer = document.getElementById("optionsContainer");
            optionsContainer.innerHTML = "";  // 清除之前的選項

            // 加入新選項
            data.options.forEach(option => {
                const button = document.createElement("button");
                button.innerText = option.text;
                button.classList.add("option-button");
                button.addEventListener("click", () => checkAnswer(option.value, data.question));
                optionsContainer.appendChild(button);
            });
        })
        .catch(error => console.error('Error loading new question:', error));
}

// 開始地震模擬遊戲
document.getElementById('startSimulation').addEventListener('click', () => {
    document.getElementById('gameSection').classList.remove('hidden');
    document.getElementById('chatSection').classList.add('hidden');
    loadNewQuestion();
});

// 問地震互動機器人
document.getElementById('askTaide').addEventListener('click', () => {
    document.getElementById('gameSection').classList.add('hidden');
    document.getElementById('chatSection').classList.remove('hidden');
    const taideResponseContainer = document.getElementById('taideResponse');
    taideResponseContainer.innerText = "TAIDE: 你好，很高興為您服務！我是TAIDE，是您現在的地震互動機器人助手，請問您有什麼關於地震的問題需要問我嗎？我會盡我所能為您解惑～";
});

// 發送使用者的問題並顯示在chatbox
document.getElementById("sendInput").addEventListener("click", () => {
    const userInput = document.getElementById("userInput").value.trim();
    
    // 確保輸入框不為空
    if (userInput !== "") {
        // 顯示使用者的問題在 chatbox
        const chatbox = document.getElementById("taideResponse");
        const userMessage = document.createElement("p");
        userMessage.textContent = `你：${userInput}`;
        chatbox.appendChild(userMessage);

        // 清除輸入框
        document.getElementById("userInput").value = "";

        // 向 TAIDE 發送請求，處理流式數據
        fetch("/ask_taide", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput })
        })
        .then(response => {
            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let taideMessage = document.createElement("p");
            taideMessage.textContent = "TAIDE：";
            chatbox.appendChild(taideMessage);

            return reader.read().then(function processText({ done, value }) {
                if (done) {
                    // 滾動到 chatbox 底部
                    chatbox.scrollTop = chatbox.scrollHeight;
                    return;
                }

                // 解碼並顯示逐步的數據
                taideMessage.textContent += decoder.decode(value, { stream: true });
                return reader.read().then(processText);
            });
        })
        .catch(error => {
            console.error("Error:", error);
            // 錯誤處理
            const errorMessage = document.createElement("p");
            errorMessage.textContent = "TAIDE 無法回應，請稍後再試。";
            chatbox.appendChild(errorMessage);
        });
    }
});

// 檢查答案並加載新題目
function checkAnswer(userAnswer, questionText) {
    fetch('/check_answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userAnswer: userAnswer, question: questionText })
    })
    .then(response => response.json())
    .then(data => {
        if (data.correct) {
            alert("恭喜！您答對了！");
        } else {
            alert("錯誤！正確答案是 " + data.correctAnswer);
        }
        // 回答完題目後加載下一道隨機題目
        loadNewQuestion();
    })
    .catch(error => console.error('Error checking answer:', error));
}