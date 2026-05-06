// ================= API CONFIG (DEPLOYED VERSION) =================
const API_URL = "https://clinic-system-799b.onrender.com";


// ================= REGISTER =================
window.register = function () {

    const username = document.getElementById("regUsername").value;
    const email = document.getElementById("regEmail").value;
    const password = document.getElementById("regPassword").value;
    const confirmPassword = document.getElementById("regConfirmPassword").value;
    const msg = document.getElementById("regMsg");

    if (!username || !email || !password || !confirmPassword) {
        msg.innerText = "All fields are required";
        msg.style.color = "red";
        return;
    }

    if (password !== confirmPassword) {
        msg.innerText = "Passwords do not match";
        msg.style.color = "red";
        return;
    }

    fetch(`${API_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, email, password })
    })
    .then(res => res.json())
    .then(data => {

        msg.innerText = data.message || "Response received";

        if (data.message === "User registered successfully") {
            msg.style.color = "green";

            setTimeout(() => {
                window.location.href = "login.html";
            }, 1200);

        } else {
            msg.style.color = "red";
        }
    })
    .catch(err => {
        console.error("Register error:", err);
        msg.innerText = "Server not reachable";
        msg.style.color = "red";
    });
};


// ================= LOGIN =================
window.login = function () {

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    const msg = document.getElementById("loginMsg");

    if (!email || !password) {
        msg.innerText = "All fields are required";
        msg.style.color = "red";
        return;
    }

    fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {

        if (data && data.username) {

            msg.innerText = "Login successful";
            msg.style.color = "green";

            // store session
            sessionStorage.setItem("user", JSON.stringify(data));

            setTimeout(() => {
                window.location.href = "user.dashboard.html";
            }, 1000);

        } else {
            msg.innerText = data.message || "Invalid credentials";
            msg.style.color = "red";
        }
    })
    .catch(err => {
        console.error("Login error:", err);
        msg.innerText = "Server not reachable";
        msg.style.color = "red";
    });
};


// ================= DASHBOARD LOAD =================
window.onload = function () {

    const user = JSON.parse(sessionStorage.getItem("user"));
    const usernameSpan = document.getElementById("username");

    if (user && usernameSpan) {
        usernameSpan.innerText = user.username;
    }

    const sidebar = document.getElementById("sidebar");
    if (!sidebar) return;

    let role = user ? user.role : "STUDENT";

    let buttonsHtml = `<h2 class="logo">Botho University Clinic</h2>`;

    if (role === "ADMIN") {
        buttonsHtml += `
            <button onclick="showSection('adminServices')">📋 Manage Services</button>
            <button onclick="showSection('adminUsers')">👥 Manage Users</button>
            <button onclick="logout()">🚪 Logout</button>
        `;
    } else {
        buttonsHtml += `
            <button onclick="showSection('portal')">🏠 Portal</button>
            <button onclick="showSection('services')">🏥 Services</button>
            <button onclick="showSection('location')">📍 Location</button>
            <button onclick="showSection('about')">ℹ️ About</button>
            <button onclick="showSection('support')">💬 Support</button>
            <button onclick="showSection('ai')">🤖 AI</button>
            <button onclick="showSection('announcements')">📢 Announcements</button>
            <button onclick="logout()">🚪 Logout</button>
        `;
    }

    sidebar.innerHTML = buttonsHtml;

    showSection(role === "ADMIN" ? "adminServices" : "portal");
};


// ================= SHOW SECTION =================
window.showSection = function (section) {

    const content = document.getElementById("content");
    if (!content) return;

    if (section === "portal") {
        const user = JSON.parse(sessionStorage.getItem("user"));

        content.innerHTML = `
            <h3>Welcome ${user ? user.username : ""}</h3>
            <p>Clinic Portal Dashboard</p>
        `;
    }

    else if (section === "services") {
        content.innerHTML = `
            <h3>Clinic Services</h3>
            <p>Services are loaded from backend.</p>
        `;
    }

    else if (section === "location") {
        content.innerHTML = `
            <h3>Location</h3>
            <p>Ha Pena-Pena Green City, Maseru, Lesotho</p>
        `;
    }

    else if (section === "about") {
        content.innerHTML = `
            <h3>About Clinic</h3>
            <p>Botho University Clinic provides free student healthcare.</p>
        `;
    }

    else if (section === "support") {
        content.innerHTML = `
            <h3>Support</h3>
            <p>Support system will connect to backend later.</p>
        `;
    }

    else if (section === "ai") {
        content.innerHTML = `
            <h3>AI Assistant</h3>
            <textarea id="aiInput" placeholder="Ask a question..."></textarea>
            <button onclick="askAI()">Ask</button>
            <p id="aiResponse"></p>
        `;
    }

    else if (section === "announcements") {
        content.innerHTML = `
            <h3>Announcements</h3>
            <p>No announcements yet.</p>
        `;
    }
};


// ================= AI =================
window.askAI = function () {

    const input = document.getElementById("aiInput").value;
    const response = document.getElementById("aiResponse");

    if (!input) {
        response.innerText = "Please type a question";
        return;
    }

    response.innerText = "AI: " + input + " (backend AI not connected yet)";
};


// ================= LOGOUT =================
window.logout = function () {
    sessionStorage.removeItem("user");
    window.location.href = "login.html";
};
