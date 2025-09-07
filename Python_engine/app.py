from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from ingestion import load_trainsets
from rules_engine import score_trainset

app = Flask(__name__)
app.secret_key = "super-secret-key"

# Dummy users
USERS = {"admin": "admin", "kmrl": "metro2025"}

@app.route("/api/ranked")
def api_ranked():
    trainsets = load_trainsets()
    scored = []
    for t in trainsets:
        score, reasons = score_trainset(t)
        scored.append({"id": t["id"], "score": score, "reasons": reasons})
    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)
    return jsonify(ranked)

@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    data = request.json
    sim_score, sim_reasons = score_trainset(data)
    return jsonify({"id": data.get("id"), "score": sim_score, "reasons": sim_reasons})

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    trainsets = load_trainsets()
    scored = []
    for t in trainsets:
        score, reasons = score_trainset(t)
        scored.append({"id": t["id"], "score": score, "reasons": reasons})
    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)

    return render_template("dashboard.html", trainsets=ranked, user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
    
@app.route("/simulate", methods=["POST"])
def simulate():
    if "user" not in session:
        return redirect(url_for("login"))

    trainsets = load_trainsets()
    scored = []
    for t in trainsets:
        score, reasons = score_trainset(t)
        scored.append({"id": t["id"], "score": score, "reasons": reasons})
    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)

    # Get simulation input
    trainset_id = request.form["trainset_id"]
    sim_data = {
        "id": trainset_id,
        "fitness": request.form["fitness"],
        "jobcard": request.form["jobcard"],
        "branding": request.form["branding"]
    }
    sim_score, sim_reasons = score_trainset(sim_data)
    simulation = {"id": trainset_id, "score": sim_score, "reasons": sim_reasons}

    return render_template("dashboard.html", trainsets=ranked, user=session["user"], simulation=simulation)

if __name__ == "__main__":
    app.run(debug=True)