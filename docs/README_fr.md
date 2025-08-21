# Infinity Translator

Infinity Translator est un logiciel qui utilise de grands modèles linguistiques pour la traduction de textes longs, avec une interface utilisateur moderne et esthétique. Il peut segmenter et prétraiter de manière appropriée de grands documents et les traduire en plusieurs langues.
![image](https://github.com/Arlecchino745/infinity_translator/blob/main/docs/img/screenshot2.png)
![image](https://github.com/Arlecchino745/infinity_translator/blob/main/docs/img/screenshot.png)

## Fonctionnalités ✨

- Prend en charge la traduction de documents volumineux sans limite de longueur 📄
- Prétraite les documents Markdown pour optimiser l'apparence visuelle des traductions 🎨
- Affiche la progression de la traduction en temps réel et enregistre automatiquement les résultats de la traduction ⏱️

## Démarrage rapide 🚀

1. Clonez le projet et basculez vers le dossier du projet :
```bash
# Clone le code du projet depuis GitHub vers votre machine locale
git clone https://github.com/Arlecchino745/infinity_translator.git
# Bascule vers le répertoire du projet
cd infinity_translator
```

2. Installez les dépendances : Veuillez faire attention à sélectionner la version appropriée de Python. Le projet est connu pour fonctionner normalement sous Python 3.12.
```bash
# Crée un environnement virtuel nommé .venv
python -m venv .venv
# Active l'environnement virtuel (pour les systèmes Windows)
.\.venv\Scripts\Activate
# Active l'environnement virtuel (pour Linux&Mac)
source ./.venv/bin/activate
# Installe les bibliothèques de dépendances requises pour le projet
pip install -r requirements.txt
```

3. Configuration de la clé API : Reportez-vous au fichier `.env.example` dans le dossier du projet. ⚙️
   - Copiez le fichier `.env.example` vers `.env` et renseignez votre clé API.

4. (Facultatif) Créez votre configuration personnalisée dans le dossier config en suivant les commentaires dans settings.json. 🛠️
   - Si vous avez besoin d'une configuration personnalisée, veuillez vous référer au fichier `config/settings.json.example`.

5. Exécutez après avoir terminé les étapes ci-dessus :
```bash
# Démarre l'application Web
python web_app.py
```
Ensuite, entrez `localhost:8000` ou `127.0.0.1:8000` dans la barre d'adresse de votre navigateur et confirmez. 🎉

### Configuration des paramètres de l'application ⚙️

Le projet contient deux fichiers de configuration :
- `config/settings.json` - Fichier de configuration par défaut, ne doit pas être modifié
- `config/settings.json.example` - Fichier de modèle de configuration pour référence

Si vous avez besoin d'une configuration personnalisée avancée (par exemple, ajouter de nouveaux modèles ou fournisseurs de services), suivez ces étapes :

1. Copiez le fichier `config/settings.json` et renommez-le en `config/settings.user.json` :
   ```bash
   # Copie le fichier de configuration par défaut vers un fichier de configuration défini par l'utilisateur
   cp config/settings.json config/settings.user.json
   ```

2. Modifiez la configuration dans le fichier `config/settings.user.json`
   - Modifiez le fichier `settings.user.json` selon vos besoins, par exemple ajouter de nouveaux modèles ou ajuster les paramètres.

3. L'application chargera en priorité settings.user.json, donc votre configuration personnalisée ne sera pas suivie par Git
   - Cela évite que les configurations personnalisées soient validées dans le référentiel distant par Git.

## Pile technologique 💻

- Backend : FastAPI + Uvicorn
- Frontend : Vue.js + Axios
- Traduction : LangChain + OpenAI API
- Construction : PyInstaller + Outil d'emballage Flet

## Licence 📄

Le projet est sous licence MIT.

## Déclaration AIGC

Ce projet est assisté par l'IA. Veuillez contacter l'auteur en cas d'infraction involontaire.