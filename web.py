from flask import Flask, request
import requests
import os
import base64
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="vi">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>𝐌𝐞𝐠𝐚𝐩𝐢𝐱𝐞𝐥 | 金英</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        :root {
            --glow-color: #ffffff;
            --dark-bg: #0a0a0a;
            --active-glow-shadow: 0 0 40px rgba(255, 255, 255, 1), 0 0 80px rgba(255, 255, 255, 0.8);
        }

        body {
            margin: 0;
            padding: 20px;
            /* Ảnh nền: Đã đổi sang đường dẫn RAW */
            background: url('https://raw.githubusercontent.com/vuonghuyhung23012007-lang/Megapixel/main/att.m_H4jrZt90BGHAMIv3BDN7TILHa3tAQ2HR1I5PkHjHY.jpg.jpeg') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            position: relative;
        }

        /* Lớp phủ tối nhẹ để làm nổi chữ */
        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.2); /* Rất nhạt để thấy rõ nền */
            z-index: -1;
        }

        #snow-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }

        /* --- CẤU TRÚC MENU MỚI (Sửa lỗi vệt sáng) --- */
        .floating-menu {
            position: relative;
            max-width: 400px;
            width: 100%;
            z-index: 10;
            margin: auto;
            background: transparent; /* Trong suốt hoàn toàn */
            border-radius: 20px;
            /* Không dùng overflow: hidden ở đây để glow lan ra ngoài được */
        }

        /* Container chứa hiệu ứng viền chạy (Masking Technique) */
        .border-animation-box {
            position: absolute;
            inset: 0; /* Phủ kín menu */
            border-radius: 20px;
            padding: 3px; /* Độ dày của viền sáng */
            pointer-events: none; /* Để click xuyên qua */
            
            /* MẶT NẠ CẮT RỖNG GIỮA: Đây là phần quan trọng nhất để sửa lỗi */
            -webkit-mask: 
                linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor; /* Chỉ giữ lại phần không giao nhau (tức là phần viền) */
            mask-composite: exclude;
        }

        /* Hiệu ứng xoay bên trong lớp mặt nạ */
        .border-animation-box::before {
            content: "";
            position: absolute;
            inset: -50%; /* Làm to hơn box để khi xoay vẫn phủ kín góc */
            background: conic-gradient(
                from 0deg, 
                transparent 0deg, 
                transparent 270deg, 
                var(--glow-color) 300deg, 
                var(--glow-color) 360deg
            );
            animation: rotate-border 4s linear infinite;
        }

        /* Lớp Glow mờ ảo cho viền */
        .border-glow {
            position: absolute;
            inset: 0;
            border-radius: 20px;
            padding: 3px; 
            pointer-events: none;
            -webkit-mask: 
                linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            filter: blur(10px); /* Làm mờ để tạo glow */
            opacity: 0.8;
            z-index: -1;
        }
        
        .border-glow::before {
            content: "";
            position: absolute;
            inset: -50%;
            background: conic-gradient(
                from 0deg, 
                transparent 0deg, 
                transparent 270deg, 
                var(--glow-color) 300deg, 
                var(--glow-color) 360deg
            );
            animation: rotate-border 4s linear infinite;
        }

        @keyframes rotate-border {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .menu-content-wrapper {
            position: relative;
            z-index: 2;
            padding: 30px;
            /* Không đặt màu nền ở đây để đảm bảo trong suốt */
        }

        .menu-title {
            color: #fff;
            font-size: 30px;
            font-weight: 900;
            margin-bottom: 5px;
            text-align: center;
            text-shadow: 
                0 0 5px #fff,
                0 0 10px var(--glow-color),
                0 0 20px var(--glow-color);
            letter-spacing: 2px;
        }

        .menu-subtitle {
            color: #e0e0e0;
            font-size: 14px;
            text-align: center;
            margin-bottom: 25px;
            text-shadow: 0 0 5px rgba(0,0,0,0.5);
            font-weight: bold;
        }

        .button-container {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        /* --- BUTTONS TRONG SUỐT HOÀN TOÀN --- */
        .action-link {
            display: flex;
            align-items: center;
            justify-content: center;
            /* Trong suốt hoàn toàn */
            background: transparent; 
            color: #fff;
            text-decoration: none;
            /* Viền mỏng màu trắng mờ */
            border: 1px solid rgba(255, 255, 255, 0.3); 
            padding: 15px 30px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 12px;
            transition: all 0.3s ease; 
            position: relative;
            overflow: hidden;
            letter-spacing: 1px;
            /* Đổ bóng nhẹ chữ để dễ đọc trên nền ảnh */
            text-shadow: 0 1px 3px rgba(0,0,0,0.8);
        }

        .action-link:hover {
            /* Khi hover chỉ sáng viền và nền hơi sáng nhẹ */
            background: rgba(255, 255, 255, 0.1); 
            border-color: var(--glow-color); 
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }

        .action-link:active {
            transform: scale(0.98); 
            background: rgba(255, 255, 255, 0.2);
        }

        .action-link i {
            margin-right: 10px;
            font-size: 20px;
        }

        /* --- MODAL --- */
        .app-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            text-align: center;
            z-index: 9999;
            backdrop-filter: blur(5px);
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.5s;
        }

        .app-modal.visible {
            opacity: 1;
            pointer-events: all;
        }

        .modal-content {
            background: rgba(0, 0, 0, 0.8);
            padding: 40px;
            border-radius: 15px;
            border: 1px solid var(--glow-color);
            box-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
            z-index: 10000;
        }

        .modal-content button {
            margin-top: 20px;
            background: var(--glow-color);
            color: #000;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
            border-radius: 8px;
            transition: background 0.3s;
            margin: 10px;
        }

        .modal-content button:hover {
            background: #ddd;
            box-shadow: 0 0 15px var(--glow-color);
        }

        /* --- CHAT BOX --- */
        #chat-modal {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 90%;
            max-width: 350px;
            height: 80vh;
            max-height: 500px;
            background: rgba(0, 0, 0, 0.9);
            border-radius: 15px;
            border: 1px solid var(--glow-color);
            box-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
            z-index: 9998;
            padding: 15px;
            flex-direction: column;
        }

        #chat-modal.active {
            display: flex;
        }

        #chat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.3);
        }

        #chat-header h3 {
            color: #fff;
            margin: 0;
            text-shadow: 0 0 5px var(--glow-color);
        }

        #close-chat {
            background: none;
            border: none;
            color: #fff;
            font-size: 20px;
            cursor: pointer;
            transition: color 0.3s;
        }
        #close-chat:hover {
            color: var(--glow-color);
        }

        #chat-messages {
            flex-grow: 1;
            overflow-y: auto;
            padding: 10px 0;
            margin-bottom: 10px;
        }

        .chat-row {
            display: flex;
            margin-bottom: 15px;
            align-items: flex-end;
        }

        .chat-avatar {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background-color: #333;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 14px;
            flex-shrink: 0;
            margin: 0 5px;
        }

        .user-row {
            justify-content: flex-end;
            margin-left: auto;
        }

        .ai-row {
            justify-content: flex-start;
            margin-right: auto;
        }

        .ai-row .chat-avatar {
            background-color: var(--glow-color);
            color: #0a0a0a;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
            order: 1;
        }
        
        .user-row .chat-avatar {
            background-color: #007bff; 
            order: 2; 
        }

        .chat-message {
            padding: 10px 12px;
            border-radius: 18px;
            max-width: calc(100% - 40px);
            word-wrap: break-word;
            line-height: 1.4;
        }

        .user-row .chat-message {
            background-color: #007bff; 
            color: #fff;
            border-bottom-right-radius: 4px;
            order: 1;
        }

        .ai-row .chat-message {
            background-color: rgba(255, 255, 255, 0.1);
            color: #fff;
            border: 1px solid #444;
            border-bottom-left-radius: 4px;
            order: 2;
        }

        #chat-input-container {
            display: flex;
            margin-top: 5px;
        }

        #chat-input {
            flex-grow: 1;
            padding: 10px;
            border-radius: 8px 0 0 8px;
            border: 1px solid var(--glow-color);
            background: rgba(0, 0, 0, 0.5);
            color: #fff;
            outline: none;
        }

        #send-chat {
            padding: 10px 15px;
            background: var(--glow-color);
            color: #000;
            border: none;
            border-radius: 0 8px 8px 0;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
        }
        #send-chat:hover {
             background: #ddd;
        }
        #send-chat:active {
            background: #fff;
            box-shadow: 0 0 10px var(--glow-color);
            transform: scale(0.98);
        }
</style>
  </head>
  <body onload="initPage()">

    <canvas id="snow-canvas"></canvas>

    <div id="music-modal" class="app-modal">
	  <div class="modal-content">
		<h2>Chào mừng đến với trang!</h2>
		<p>Trang này có tính năng phát nhạc nền. Bạn có muốn nghe nhạc không?</p>
		<button onclick="confirmMusic(true)">Đồng ý Phát Nhạc</button>
		<button onclick="confirmMusic(false)">Không, cảm ơn</button>
	  </div>
    </div>

    <div id="chat-modal">
	  <div id="chat-header">
		<h3>Gemini 2.5 Pro</h3>
		<button id="close-chat" onclick="closeChatModal()">×</button>
	  </div>
	  <div id="chat-messages">
		<div class="chat-row ai-row">
		  <div class="chat-avatar"><i class="fas fa-robot"></i></div>
		  <div class="chat-message">Chào bạn! Tôi là AI Chatbot, tôi có thể trả lời các câu hỏi của bạn.</div>
		</div>
	  </div>
	  <div id="chat-input-container">
		<input type="text" id="chat-input" placeholder="Nhập câu hỏi của bạn...">
		<button id="send-chat" onclick="sendChatMessage()">Gửi</button>
	  </div>
    </div>

    <div class="floating-menu">
	  <!-- Layer Glow cho viền -->
	  <div class="border-glow"></div>
	  <!-- Layer Viền chính (được cắt rỗng ruột) -->
	  <div class="border-animation-box"></div>

	  <div class="menu-content-wrapper">
		<h1 class="menu-title">𝐌𝐞𝐠𝐚𝐩𝐢𝐱𝐞𝐥 | 金英</h1>
		<p class="menu-subtitle">𝐌𝐚𝐝𝐞 𝐁𝐲 𝐌𝐞𝐠𝐚𝐩𝐢𝐱e𝐥 </p>
		<div class="button-container">
		  <a href="https://www.facebook.com/vuonghung.232007" target="_blank" class="action-link">
			<i class="fab fa-facebook-f"></i>
			<span class="link-text">FACEBOOK</span>
		  </a>

		  <a href="https://www.tiktok.com/@vuonghung_23" target="_blank" class="action-link">
			<i class="fab fa-tiktok"></i>
			<span class="link-text">TIKTOK</span>
		  </a>

		  <a href="https://t.me/MegapixelCheater" target="_blank" class="action-link">
			<i class="fab fa-telegram-plane"></i>
			<span class="link-text">TELEGRAM</span>
		  </a>

		  <a href="#" class="action-link chat-button-main" onclick="openChatModal(); return false;">
			<i class="fas fa-comment-dots"></i>
			<span class="link-text">CHAT VỚI AI</span>
		  </a>
		</div>
	  </div>
    </div>

    <audio id="background-music" loop></audio>

<script>
        const music = document.getElementById('background-music');
        const chatModal = document.getElementById('chat-modal');
        const chatInput = document.getElementById('chat-input');
        const chatMessages = document.getElementById('chat-messages');
        const sendButton = document.getElementById('send-chat');

        const MUSIC_CONSENT_KEY = 'musicConsent_v8'; 
        
        // Đã thay đổi URL nhạc sang đường dẫn RAW của GitHub để có thể phát được
        const musicUrls = [
            'https://raw.githubusercontent.com/vuonghuyhung23012007-lang/Megapixel/main/Megapixel%20Remix%202.mp3',
            'https://raw.githubusercontent.com/vuonghuyhung23012007-lang/Megapixel/main/Megapixel%20Remix.mp3'
        ];

        let chatHistory = [{
            role: "model", 
            parts: [{ text: "Chào bạn! Tôi là AI Chatbot, tôi có thể trả lời các câu hỏi của bạn." }]
        }];
        
        const API_KEY = ""; // Bỏ trống vì Canvas sẽ tự cung cấp API Key
        const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${API_KEY}`;
        
        let isTyping = false; 
        
        function openAppModal(id) {
            document.getElementById(id).classList.add('visible');
        }

        function closeAppModal(id) {
            document.getElementById(id).classList.remove('visible');
        }

        function initPage() {
            startSnowEffect();

            const musicConsent = localStorage.getItem(MUSIC_CONSENT_KEY);
            if (!musicConsent) {
                openAppModal('music-modal');
            } else if (musicConsent === 'granted') {
                playMusic();
            }
        }

        function confirmMusic(isAgreed) {
            if (isAgreed) {
                localStorage.setItem(MUSIC_CONSENT_KEY, 'granted');
                playMusic(); 
            } else {
                localStorage.setItem(MUSIC_CONSENT_KEY, 'denied');
            }
            closeAppModal('music-modal');
        }

        function playMusic() {
            try {
                if (!music.src || music.src === "") {
                    const randomIndex = Math.floor(Math.random() * musicUrls.length);
                    music.src = musicUrls[randomIndex];
                }
                
                music.volume = 0.5;
                const playPromise = music.play();

                if (playPromise !== undefined) {
                    playPromise.then(_ => {
                        console.log("Nhạc đang phát.");
                    })
                    .catch(error => {
                        console.error("Không thể phát nhạc (chặn tự động phát):", error);
                    });
                }
            } catch (e) {
                console.error("Lỗi khi bắt đầu nhạc:", e);
            }
        }

        // --- LOGIC TUYẾT RƠI ---
        function startSnowEffect() {
            const canvas = document.getElementById('snow-canvas');
            const ctx = canvas.getContext('2d');

            let width = window.innerWidth;
            let height = window.innerHeight;
            canvas.width = width;
            canvas.height = height;

            const snowflakes = [];
            const maxSnowflakes = 80; 

            class Snowflake {
                constructor() {
                    this.reset();
                }

                reset() {
                    this.x = Math.random() * width;
                    this.y = Math.random() * -height;
                    this.vx = Math.random() * 1 - 0.5;
                    this.vy = Math.random() * 1.5 + 0.5; 
                    this.size = Math.random() * 10 + 10; 
                    this.opacity = Math.random() * 0.5 + 0.5;
                    this.rotation = Math.random() * 360;
                    this.rotationSpeed = Math.random() * 2 - 1;
                }

                update() {
                    this.x += this.vx;
                    this.y += this.vy;
                    this.rotation += this.rotationSpeed;

                    if (this.y > height || this.x > width || this.x < -50) {
                        this.reset();
                    }
                }

                draw() {
                    ctx.save();
                    ctx.translate(this.x, this.y);
                    ctx.rotate(this.rotation * Math.PI / 180);
                    
                    ctx.shadowBlur = 15; 
                    ctx.shadowColor = "rgba(255, 255, 255, 0.8)"; 
                    
                    ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`;
                    ctx.font = `${this.size}px Arial`;
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText("❄", 0, 0); 
                    
                    ctx.restore();
                }
            }

            for (let i = 0; i < maxSnowflakes; i++) {
                snowflakes.push(new Snowflake());
            }

            function animate() {
                ctx.clearRect(0, 0, width, height);
                for (let snowflake of snowflakes) {
                    snowflake.update();
                    snowflake.draw();
                }
                requestAnimationFrame(animate);
            }

            animate();

            window.addEventListener('resize', () => {
                width = window.innerWidth;
                height = window.innerHeight;
                canvas.width = width;
                canvas.height = height;
            });
        }

        // --- LOGIC CHAT BOT ---

        function openChatModal() {
            chatModal.classList.add('active');
            chatInput.focus();
        }

        function closeChatModal() {
            chatModal.classList.remove('active');
        }
        
        function setChatState(typing) {
            isTyping = typing;
            sendButton.disabled = typing;
            chatInput.disabled = typing;
        }

        function displayMessage(text, isUser) {
            const chatRow = document.createElement('div');
            chatRow.className = `chat-row ${isUser ? 'user-row' : 'ai-row'}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'chat-avatar';
            avatar.innerHTML = isUser ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
            
            const msg = document.createElement('div');
            msg.className = 'chat-message';
            msg.textContent = text;
            
            if (isUser) {
                chatRow.appendChild(msg);
                chatRow.appendChild(avatar);
            } else {
                chatRow.appendChild(avatar);
                chatRow.appendChild(msg);
            }

            chatMessages.appendChild(chatRow);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            return msg;
        }
        
        function typeWriterEffect(element, text, speed = 25) {
            let i = 0;
            element.textContent = '';
            
            return new Promise(resolve => {
                function type() {
                    if (i < text.length) {
                        element.textContent += text.charAt(i);
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                        i++;
                        setTimeout(type, speed);
                    } else {
                        resolve();
                    }
                }
                type();
            });
        }

        async function fetchAIResponse(userQuery) {
            chatHistory.push({ role: "user", parts: [{ text: userQuery }] });

            const payload = {
                contents: chatHistory,
                tools: [{ "google_search": {} }], 
                systemInstruction: {
                    parts: [{ text: "Bạn là một trợ lý ảo thân thiện, hỗ trợ người dùng bằng tiếng Việt. Hãy trả lời ngắn gọn, chính xác và có ích. Bạn được lập trình bởi Megapixel | 金英." }]
                },
            };

            setChatState(true);
            const aiMessageElement = displayMessage('', false);

            let attempts = 0;
            const maxAttempts = 3;
            let delay = 1000;

            while (attempts < maxAttempts) {
                try {
                    const response = await fetch(API_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const result = await response.json();
                    
                    const candidate = result.candidates?.[0];
                    if (candidate && candidate.content?.parts?.[0]?.text) {
                        const aiText = candidate.content.parts[0].text;
                        
                        await typeWriterEffect(aiMessageElement, aiText);
                        
                        chatHistory.push({ role: "model", parts: [{ text: aiText }] });
                        return aiText;
                    } else {
                        return "Rất tiếc, tôi không thể tạo ra câu trả lời lúc này. Vui lòng thử lại.";
                    }

                } catch (error) {
                    console.error(`Lần thử ${attempts + 1} thất bại:`, error);
                    attempts++;
                    if (attempts < maxAttempts) {
                        await new Promise(resolve => setTimeout(resolve, delay));
                        delay *= 2;
                    }
                }
            }
            return "Đã xảy ra lỗi hệ thống, vui lòng thử lại sau.";
        }


        async function sendChatMessage() {
            if (isTyping) return;
            
            const message = chatInput.value.trim();
            if (message === "") return;

            displayMessage(message, true);
            
            chatInput.value = '';
            
            const aiResponse = await fetchAIResponse(message);
            
            if (aiResponse.startsWith("Rất tiếc") || aiResponse.startsWith("Đã xảy ra lỗi")) {
                const errorElement = chatMessages.lastElementChild.querySelector('.chat-message');
                errorElement.textContent = aiResponse;
            }

            setChatState(false);
            chatInput.focus();
        }

        chatInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter' && !isTyping) {
                sendChatMessage();
            }
        });
        
</script>
  </body>
</html>
'''
if __name__ == '__main__':
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port = port, debug = False)
    


