<!DOCTYPE html>
<html>
<head>
    <title>Daily Progress Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 400px;
            margin: 40px auto;
        }

        .progress-container {
            width: 100%;
            background: #ddd;
            border-radius: 10px;
            overflow: hidden;
            height: 25px;
            margin-bottom: 10px;
        }

        .progress-bar {
            height: 100%;
            width: 0%;
            background: #4caf50;
            text-align: center;
            color: white;
            line-height: 25px;
            transition: width 0.3s;
        }

        #resetBtn {
            margin-top: 10px;
            padding: 8px 14px;
            border: none;
            background: #e74c3c;
            color: white;
            border-radius: 6px;
            cursor: pointer;
            width: 100%;
        }

        #resetBtn:hover {
            background: #c0392b;
        }

        .controls {
            margin-top: 15px;
            display: flex;
            justify-content: space-between;
        }

        button {
            padding: 8px 14px;
            border: none;
            background: #3498db;
            color: white;
            border-radius: 6px;
            cursor: pointer;
        }

        button:hover {
            background: #2980b9;
        }
    </style>
</head>
<body>

    <h2>Daily Progress Tracker</h2>

    <!-- Progress Bar -->
    <div class="progress-container">
        <div class="progress-bar" id="progressBar">0%</div>
    </div>

    <!-- Reset Button -->
    <button id="resetBtn">Reset Today</button>

    <!-- Buttons to increase progress -->
    <div class="controls">
        <button onclick="updateProgress(10)">+10%</button>
        <button onclick="updateProgress(20)">+20%</button>
        <button onclick="updateProgress(30)">+30%</button>
    </div>

    <script>
        const progressBar = document.getElementById("progressBar");
        const today = new Date().toISOString().split("T")[0];
        const storageKey = `progress_${today}`;

        // Load today's progress
        let currentProgress = localStorage.getItem(storageKey);
        if (!currentProgress) currentProgress = 0;
        updateUI(currentProgress);

        // Update progress
        function updateProgress(value) {
            currentProgress = Math.min(100, Number(currentProgress) + value);
            localStorage.setItem(storageKey, currentProgress);
            updateUI(currentProgress);
        }

        // Update UI bar
        function updateUI(value) {
            progressBar.style.width = value + "%";
            progressBar.innerText = value + "%";
        }

        // Reset only today's data
        document.getElementById("resetBtn").addEventListener("click", function () {
            localStorage.removeItem(storageKey);
            currentProgress = 0;
            updateUI(0);
            alert("Today's progress has been reset.");
        });
    </script>

</body>
</html>
