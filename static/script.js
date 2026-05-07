const API_URL = "http://127.0.0.1:10000";

// ================= REGISTER =================
window.register = async function () {
    const username = document.getElementById("regUsername").value;
    const email = document.getElementById("regEmail").value;
    const password = document.getElementById("regPassword").value;
    const msg = document.getElementById("regMsg");

    try {
        const res = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });

        const data = await res.json();

        if (res.ok) {
            msg.style.color = "green";
            msg.innerText = data.message;

            setTimeout(() => {
                window.location.href = "login.html";
            }, 1000);
        } else {
            msg.style.color = "red";
            msg.innerText = data.message;
        }
    } catch {
        msg.innerText = "Server not reachable";
    }
};

// ================= LOGIN =================
window.login = async function () {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    const msg = document.getElementById("loginMsg");

    try {
        const res = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (res.ok) {
            localStorage.setItem("user", JSON.stringify(data));

            msg.style.color = "green";
            msg.innerText = "Login successful";

            setTimeout(() => {
                window.location.href = "user.dashboard.html";
            }, 1000);
        } else {
            msg.style.color = "red";
            msg.innerText = data.message;
        }
    } catch {
        msg.innerText = "Server not reachable";
    }
};

// ================= DASHBOARD LOAD =================
window.onload = function () {
    const user = JSON.parse(localStorage.getItem("user"));

    if (!user) return;

    const username = document.getElementById("username");
    if (username) username.innerText = user.username;

    const sidebar = document.getElementById("sidebar");
    if (!sidebar) return;

    let html = `<h2 class="logo">Botho Clinic</h2>`;

    if (user.role === "ADMIN") {
        html += `
            <button onclick="showSection('adminServices')">Manage Services</button>
            <button onclick="showSection('adminUsers')">Users</button>
        `;
    } else {
        html += `
            <button onclick="showSection('portal')">Portal</button>
            <button onclick="showSection('services')">Services</button>
        `;
    }

    html += `<button onclick="logout()">Logout</button>`;
    sidebar.innerHTML = html;

    showSection("portal");
};

// ================= SHOW SECTION (simple version) =================
window.showSection = function (section) {
    const content = document.getElementById("content");

    if (section === "portal") {
        const user = JSON.parse(localStorage.getItem("user"));

        content.innerHTML = `
            <h3>Welcome ${user.username}</h3>
            <p>Role: ${user.role}</p>
        `;
    }

    if (section === "services") {
        content.innerHTML = `<h3>Services</h3><p>All clinic services here</p>`;
    }

    if (section === "adminUsers") {
        content.innerHTML = `<h3>Admin Users Panel</h3><p>Coming soon</p>`;
    }
};

// ================= LOGOUT =================
window.logout = function () {
    localStorage.removeItem("user");
    window.location.href = "login.html";
};
