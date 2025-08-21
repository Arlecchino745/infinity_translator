# Infinity Translator

<div align="center">🌐 <a href="/docs/README_zh-Hans.md">简体中文</a> | <a href="/docs/README_zh-Hant.md">繁體中文</a> | <a href="/docs/README_ja.md">日本語</a> | <a href="/docs/README_fr.md">Français</a> | <a href="/docs/README_kr.md">한국어</a> | <a href="/docs/README_ru.md">Русский</a></div>

---
Infinity Translator est un logiciel qui utilise de grands modèles linguistiques pour la traduction de textes longs, avec une interface utilisateur moderne et esthétique. Il peut segmenter et prétraiter de manière appropriée de grands documents et les traduire en plusieurs langues.

![image](https://github.com/Arlecchino745/infinity_translator/blob/main/docs/img/screenshot2.png)
![image](https://github.com/Arlecchino745/infinity_translator/blob/main/docs/img/screenshot.png)

## Fonctionnalités ✨

- Prend en charge la traduction de documents volumineux sans limite de longueur 📄
- Prétraite les documents Markdown pour optimiser l'apparence visuelle des traductions 🎨
- Affiche la progression de la traduction en temps réel et enregistre automatiquement les résultats de la traduction ⏱️

## Démarrage rapide!

**AVIS : Malheureusement, en raison de certains problèmes techniques, cette version ne prend en charge que les travaux de traduction utilisant Google Gemini 2.0 Flash via OpenRouter. Ce problème sera priorisé dans les versions ultérieures.**

1. Téléchargez la dernière version depuis la page [Releases](https://github.com/Arlecchino745/infinity_translator/releases).
2. Extrayez le fichier zip téléchargé.
3. Ouvrez le dossier _internal, copiez .env.example et renommez-le en .env, puis remplissez la clé API.
4. Exécutez `infinity_translator.exe` pour démarrer l'application.

## Démarrer à partir du code source (dev)

1. Clonez le projet et basculez vers le dossier du projet :
```bash
# Clonez le code du projet depuis GitHub vers votre machine locale
git clone https://github.com/Arlecchino745/infinity_translator.git
# Basculez vers le répertoire du projet
cd infinity_translator
```

2. Installez les dépendances : Veuillez faire attention à sélectionner la version appropriée de Python. Le projet est connu pour fonctionner normalement sous Python 3.12.
```bash
# Créez un environnement virtuel nommé .venv
python -m venv .venv
# Activez l'environnement virtuel (pour les systèmes Windows)
.\.venv\Scripts\Activate
# Activez l'environnement virtuel (pour Linux&Mac)
source ./.venv/bin/activate
# Installez les bibliothèques de dépendances requises pour le projet
pip install -r requirements.txt
```

3. Configuration de la clé API : Reportez-vous au fichier `.env.example` dans le dossier du projet. ⚙️
   - Copiez le fichier `.env.example` vers `.env` et remplissez votre clé API.

4. (Facultatif) Créez votre configuration personnalisée dans le dossier config en suivant les commentaires dans settings.json. 🛠️
   - Si vous avez besoin d'une configuration personnalisée, veuillez vous référer au fichier `config/settings.json.example`.

5. Exécutez après avoir terminé les étapes ci-dessus :
```bash
# Démarrez l'application Web
python web_app.py
```
Ensuite, entrez `localhost:8000` ou `127.0.0.1:8000` dans la barre d'adresse de votre navigateur et confirmez. 🎉

### Configuration des paramètres de l'application (uniquement pour le démarrage à partir du code source)⚙️

Le projet contient deux fichiers de configuration :
- `config/settings.json` - Fichier de configuration par défaut, ne doit pas être modifié
- `config/settings.json.example` - Fichier de modèle de configuration pour référence

Si vous avez besoin d'une configuration personnalisée avancée (par exemple, ajouter de nouveaux modèles ou fournisseurs de services), suivez ces étapes :

1. Copiez le fichier `config/settings.json` et renommez-le en `config/settings.user.json` :
   ```bash
   # Copiez le fichier de configuration par défaut vers un fichier de configuration défini par l'utilisateur
   cp config/settings.json config/settings.user.json
   ```

2. Modifiez la configuration dans le fichier `config/settings.user.json`
   - Modifiez le fichier `settings.user.json` selon vos besoins, par exemple ajouter de nouveaux modèles ou ajuster les paramètres.

3. L'application chargera en priorité settings.user.json, donc votre configuration personnalisée ne sera pas suivie par Git
   - Cela évite que les configurations personnalisées soient validées dans le référentiel distant par Git.

## Pile technologique 💻

- Backend : FastAPI + Uvicorn
- Frontend : Vue.js + Axios
- Traduction : LangChain + OpenAI API
- Construction : PyInstaller

## Licence 📄

Le projet est sous licence MIT.

## Déclaration AIGC

Ce projet est assisté par l'IA. Veuillez contacter l'auteur en cas d'infraction involontaire.