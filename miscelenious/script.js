const themeToggle = document.getElementById('theme-toggle');
        const themeIcon = themeToggle.querySelector('i');
        const html = document.documentElement;

        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'light';
        html.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);

        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });

        function updateThemeIcon(theme) {
            themeIcon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }

        const startBtn = document.getElementById("start-btn");
        const outputDiv = document.getElementById("output");
        const statusSpan = document.getElementById("status");
        const waveVisualizer = document.getElementById("wave-visualizer");
        const buttonText = startBtn.querySelector("span");

        if ("webkitSpeechRecognition" in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = "en-US";

            startBtn.addEventListener("click", () => {
                startBtn.classList.add("listening");
                buttonText.textContent = "Listening...";
                outputDiv.textContent = "Listening...";
                statusSpan.textContent = "Listening...";
                waveVisualizer.style.display = "flex";
                recognition.start();
            });

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                outputDiv.innerHTML = `<i class="fas fa-quote-left"></i> ${transcript} <i class="fas fa-quote-right"></i>`;
            };

            recognition.onerror = (event) => {
                outputDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> Error: ${event.error}`;
                resetUI();
            };

            recognition.onend = () => {
                resetUI();
            };

            function resetUI() {
                startBtn.classList.remove("listening");
                buttonText.textContent = "Start Listening";
                statusSpan.textContent = "Ready";
                waveVisualizer.style.display = "none";
            }
        } else {
            startBtn.disabled = true;
            outputDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i> Speech recognition is not supported in your browser. Please try using Google Chrome.';
        }