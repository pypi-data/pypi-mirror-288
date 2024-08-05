from setuptools import setup, find_packages
import os 

# Read the contents of the README file
def read_readme():
    with open(os.path.join(os.path.dirname(__file__), 'DOC_README.md'), encoding='utf-8') as f:
        return f.read()
   
long_description = """
# Mkdocs Quizz 

## Installation 

```
pip install my_quiz_plugin
```

### Add extra js/css

Go to your `docs/` folder and create : 

- `javascripts/extra.js` file here : 
- `stylesheets/extra.css` file here : 

Then add to `mkdocs.yml` file this lines :  

```yaml
plugins:
  - my_quiz_plugin:
      quiz_file: quizzes.json
      language: en

extra_css:
  - stylesheets/extra.css
  - https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css

extra_javascript:
  - javascripts/extra.js
```

### Create a `quizzes.json` file 

Ensure your `quizzes` JSON file is structured like this :

```json
{
    "quizzes": {
        "quiz1": {
            "questions": [
                {
                    "type": "multiple-choice",
                    "question": {
                        "en": "What is the capital of France?",
                        "fr": "Quelle est la capitale de la France?"
                    },
                    "options": [
                        { "text": { "en": "Berlin", "fr": "Berlin" }, "correct": false, "indice": { "en": "This is the capital of Germany.", "fr": "Ceci est la capitale de l'Allemagne." }},
                        { "text": { "en": "Madrid", "fr": "Madrid" }, "correct": false, "indice": { "en": "This is the capital of Spain.", "fr": "Ceci est la capitale de l'Espagne." }},
                        { "text": { "en": "Paris", "fr": "Paris" }, "correct": true, "indice": { "en": "", "fr": "" }},
                        { "text": { "en": "Rome", "fr": "Rome" }, "correct": false, "indice": { "en": "This is the capital of Italy.", "fr": "Ceci est la capitale de l'Italie." }}
                    ]
                },
                {
                    "type": "true-false",
                    "question": {
                        "en": "The Earth is flat.",
                        "fr": "La Terre est plate."
                    },
                    "options": [
                        { "text": { "en": "True", "fr": "Vrai" }, "correct": false, "indice": { "en": "The Earth is round.", "fr": "La Terre est ronde." }},
                        { "text": { "en": "False", "fr": "Faux" }, "correct": true, "indice": { "en": "", "fr": "" }}
                    ]
                },
                {
                    "type": "fill-in-the-blank",
                    "question": {
                        "en": "____ is the largest planet in our solar system.",
                        "fr": "____ est la plus grande planète de notre système solaire."
                    },
                    "answer": { "en": "Jupiter", "fr": "Jupiter" },
                    "indice": {
                        "en": "It is a gas giant.",
                        "fr": "C'est une géante gazeuse."
                    }
                }
            ]
        },
        "quiz2": {
            "questions": [
                {
                    "type": "multiple-choice",
                    "question": {
                        "en": "Which element has the chemical symbol 'O'?",
                        "fr": "Quel élément a le symbole chimique 'O'?"
                    },
                    "options": [
                        { "text": { "en": "Oxygen", "fr": "Oxygène" }, "correct": true, "indice": { "en": "", "fr": "" }},
                        { "text": { "en": "Gold", "fr": "Or" }, "correct": false, "indice": { "en": "The symbol for gold is 'Au'.", "fr": "Le symbole de l'or est 'Au'." }},
                        { "text": { "en": "Osmium", "fr": "Osmium" }, "correct": false, "indice": { "en": "The symbol for osmium is 'Os'.", "fr": "Le symbole de l'osmium est 'Os'." }},
                        { "text": { "en": "Hydrogen", "fr": "Hydrogène" }, "correct": false, "indice": { "en": "The symbol for hydrogen is 'H'.", "fr": "Le symbole de l'hydrogène est 'H'." }}
                    ]
                },
                {
                    "type": "true-false",
                    "question": {
                        "en": "Water boils at 100°C.",
                        "fr": "L'eau bout à 100°C."
                    },
                    "options": [
                        { "text": { "en": "True", "fr": "Vrai" }, "correct": true, "indice": { "en": "", "fr": "" }},
                        { "text": { "en": "False", "fr": "Faux" }, "correct": false, "indice": { "en": "At sea level, water boils at 100°C.", "fr": "Au niveau de la mer, l'eau bout à 100°C." }}
                    ]
                },
                {
                    "type": "fill-in-the-blank",
                    "question": {
                        "en": "The chemical formula for water is ___.",
                        "fr": "La formule chimique de l'eau est ___."
                    },
                    "answer": { "en": "H2O", "fr": "H2O" },
                    "indice": {
                        "en": "It consists of two hydrogen atoms and one oxygen atom.",
                        "fr": "Elle se compose de deux atomes d'hydrogène et d'un atome d'oxygène."
                    }
                }
            ]
        }
    }
}

```

### Run the mkdocs server 

```
mkdocs serve
``` 
"""

setup(
    name='my_quiz_plugin',
    version='1.0.1',
    description='A MkDocs plugin to create quizzes',
    author_email='your.email@example.com',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'mkdocs>=1.0.4',
        'beautifulsoup4>=4.11.1',
        'lxml>=4.9.1',
        'pytest>=7.4.4'
    ],
    entry_points={
        'mkdocs.plugins': [
            'my_quiz_plugin = my_quiz_plugin.plugin:QuizPlugin'
        ]
    },
    keywords='mkdocs plugin quizz',
    license='MIT',
    project_urls={
        'Bug Reports': 'https://github.com/bdllard/my_quiz_plugin/issues',
        'Source': 'https://github.com/bdallard/my_quiz_plugin',
    },

)

