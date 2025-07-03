# ⚔️ WASSOps — Backend for Web App Security Scanner

> 🔐 Secure your deployments before hackers do.  
> **WASSOps** is the fast, extensible, and modular backend that powers **WASS** – your open-source Web Application Security Scanner.

![WASSOps Banner](https://img.shields.io/badge/Built%20With-FastAPI-blue?style=for-the-badge) ![Supabase](https://img.shields.io/badge/Database-Supabase-3ecf8e?style=for-the-badge) ![Docker](https://img.shields.io/badge/Containerized-Docker-blue?style=for-the-badge) ![AWS](https://img.shields.io/badge/Deployed%20on-AWS-232f3e?style=for-the-badge)

---

## 🚀 Features

- 🔍 **Automated Scanning** using [Nuclei](https://github.com/projectdiscovery/nuclei)
- 🎯 **Scan Queuing** and Job Management
- 🧠 **Score Calculation** based on real scan data
- ☁️ **Supabase Integration** for auth, storage, and DB
- 🧵 Background scanning via subprocesses
- ⚙️ Fully containerized with **Docker**
- ☁️ Deployable to **AWS EC2** or any cloud of your choice

---

## 🛠️ Tech Stack

- **Backend**: Python + FastAPI
- **Security Engine**: Nuclei
- **Database**: Supabase Postgres
- **Infra**: Docker + AWS EC2
- **Auth**: Supabase Auth (OAuth)

---

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-username/WASSOps.git
cd WASSOps
