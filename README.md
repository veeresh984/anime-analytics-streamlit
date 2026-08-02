# 🎌 Anime Analytics Dashboard

A professional **Streamlit web application** for exploring, analyzing, and visualizing **Top Anime TV Shows** using interactive dashboards, deep analytics, and AI-style insights.

This project is built with **Python, Streamlit, Pandas, and Plotly** and is ready for deployment on **Streamlit Cloud**.

---

## 🚀 Live Demo

After deployment, your app link will look like:

`https://your-app-name.streamlit.app`

---

## 📌 Features

### 📊 Executive Dashboard

* Total anime count
* Average score
* Total members
* Total studios
* Interactive KPI cards

### 🎭 Genre Analytics

* Most popular genres
* Genre frequency analysis
* Genre-wise score comparison

### ⭐ Rating Insights

* Score distribution
* Outlier detection
* Quantile analysis

### 🏢 Studio Analytics

* Top anime studios
* Studio performance comparison
* Production volume analysis

### 📖 Synopsis Explorer

* Search anime by title
* Read synopsis
* Explore genres and scores

### 🤖 AI Insights

* Automatically generated insights
* Trend observations
* Audience preference analysis

---

## 🗂️ Project Structure

```text
anime-analytics-streamlit/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
│
├── data/
│   └── anime_dataset.csv
│
├── pages/
│   ├── 01_Executive_Dashboard.py
│   ├── 02_Genre_Analytics.py
│   ├── 03_Rating_Insights.py
│   ├── 04_Studio_Analytics.py
│   ├── 05_Synopsis_Explorer.py
│   └── 06_AI_Insights.py
│
├── utils/
│   ├── data_loader.py
│   ├── charts.py
│   ├── analytics.py
│   └── insights.py
│
└── assets/
    └── banner.png
```

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/anime-analytics-streamlit.git
cd anime-analytics-streamlit
```

### 2️⃣ Create a virtual environment (recommended)

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App Locally

```bash
streamlit run app.py
```

The app will open in your browser at:

`http://localhost:8501`

---

## ☁️ Deploy on Streamlit Cloud

1. Push the project to GitHub.
2. Visit **https://streamlit.io/cloud**
3. Sign in with GitHub.
4. Click **New app**.
5. Select your repository.
6. Set **Main file path** to:

```text
app.py
```

7. Click **Deploy**.

---

## 📊 Example Analytics Included

| Analytics             | Included |
| --------------------- | -------- |
| KPI Dashboard         | ✅        |
| Interactive Filters   | ✅        |
| Genre Analysis        | ✅        |
| Studio Analysis       | ✅        |
| Rating Distribution   | ✅        |
| Popularity Analysis   | ✅        |
| Correlation Insights  | ✅        |
| Outlier Detection     | ✅        |
| Synopsis Search       | ✅        |
| AI Insights           | ✅        |
| Multi-page Navigation | ✅        |

---

## 🛠️ Technologies Used

* **Python 3.10+**
* **Streamlit**
* **Pandas**
* **NumPy**
* **Plotly**
* **Scikit-learn**
* **Matplotlib**
* **Seaborn**

---

## 📈 Sample Dashboard

The dashboard provides:

* Dark-themed modern UI
* Responsive layout
* Interactive Plotly charts
* Real-time filtering
* Executive-level insights

---

## 📚 Dataset

The dataset contains information such as:

* Anime title
* Score
* Popularity
* Members
* Genres
* Studios
* Synopsis

Place your dataset inside:

```text
data/anime_dataset.csv
```

---

## 🔧 Configuration

Create `.streamlit/config.toml`:

```toml
[theme]
base="dark"
primaryColor="#ff4b4b"
backgroundColor="#0e1117"
secondaryBackgroundColor="#1c1f26"
textColor="#ffffff"
font="sans serif"
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

## 📝 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Your Name**

* GitHub: https://github.com/YOUR_USERNAME
* LinkedIn: https://linkedin.com/in/YOUR_PROFILE

---

## ⭐ Support

If you found this project useful, please **star the repository** on GitHub ⭐

---

## 🙏 Acknowledgements

* Streamlit
* Plotly
* Pandas
* The anime data community

---

### 🎌 Built with ❤️ using Streamlit and Plotly
