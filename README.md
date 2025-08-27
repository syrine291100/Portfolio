# Portfolio – Syrine Chehairi

Portfolio **Streamlit** multipage (pastel, responsive) pour présenter mes compétences, projets et expériences.

👉 **Démo** : <https://syrinechehairi-portfolio.hf.space>  
👉 **CV & Contact** : voir page *Contact* du site

---

## ✨ Fonctionnalités
- Barre de **navigation** sticky (pastel)
- Pages : **Accueil**, **Compétences**, **Projets** (descriptions), **Expériences**, **Formations**, **Contact**
- Design sobre + lisible (cartes, tags, couleurs pastels)
- Assets optionnels : `assets/photo.jpg`, `assets/CV_Syrine_Chehairi.pdf`

## 🧰 Stack
- Python 3.10+
- Streamlit
- Pillow (affichage images)

## 🚀 Lancer en local
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
