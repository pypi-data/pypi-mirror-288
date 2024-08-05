# mkdoc-qcm
mkdoc qcm pluging

My apologies for that oversight. Here is the corrected JSON structure including the "indice" field for hints, along with the updated references:

### Complete Directory Structure

Ensure your project directory looks like this:
```
my_project/
├── docs/
├── mkdocs.yml
├── my_quiz_plugin/
│   ├── __init__.py
│   └── plugin.py
├── quizzes.json
├── tests/
│   ├── __init__.py
│   └── test_plugin.py
└── tox.ini

```

________________________________________________________________________________________________________________


# TODO
- [ ] write documentation 
- [ ] adjust json doc 
- [ ] adjust project Directory Structure 


### Step 1: Update the JSON Structure


Ensure the JSON file includes hints (indice) for each option:
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
                        {
                            "text": {
                                "en": "Berlin",
                                "fr": "Berlin"
                            },
                            "correct": false,
                            "indice": {
                                "en": "This is the capital of Germany.",
                                "fr": "Ceci est la capitale de l'Allemagne."
                            }
                        },
                        {
                            "text": {
                                "en": "Madrid",
                                "fr": "Madrid"
                            },
                            "correct": false,
                            "indice": {
                                "en": "This is the capital of Spain.",
                                "fr": "Ceci est la capitale de l'Espagne."
                            }
                        },
                        {
                            "text": {
                                "en": "Paris",
                                "fr": "Paris"
                            },
                            "correct": true,
                            "indice": {
                                "en": "Paris is the city of light",
                                "fr": ""
                            }
                        },
                        {
                            "text": {
                                "en": "Rome",
                                "fr": "Rome"
                            },
                            "correct": false,
                            "indice": {
                                "en": "This is the capital of Italy.",
                                "fr": "Ceci est la capitale de l'Italie."
                            }
                        }
                    ]
                },
                {
                    "type": "true-false",
                    "question": {
                        "en": "The Earth is flat.",
                        "fr": "La Terre est plate."
                    },
                    "options": [
                        {
                            "text": {
                                "en": "True",
                                "fr": "Vrai"
                            },
                            "correct": false,
                            "indice": {
                                "en": "The Earth is round.",
                                "fr": "La Terre est ronde."
                            }
                        },
                        {
                            "text": {
                                "en": "False",
                                "fr": "Faux"
                            },
                            "correct": true,
                            "indice": {
                                "en": "",
                                "fr": ""
                            }
                        }
                    ]
                },
                {
                    "type": "fill-in-the-blank",
                    "question": {
                        "en": "____ is the largest planet in our solar system.",
                        "fr": "____ est la plus grande planète de notre système solaire."
                    },
                    "answer": {
                        "en": "Jupiter",
                        "fr": "Jupiter"
                    },
                    "indice": {
                        "en": "It is a gas giant.",
                        "fr": "C'est une géante gazeuse."
                    }
                },
                {
                    "type": "multi-choice",
                    "question": {
                        "en": "Select the primary colors:",
                        "fr": "Sélectionnez les couleurs primaires :"
                    },
                    "options": [
                        {
                            "text": {
                                "en": "Red",
                                "fr": "Rouge"
                            },
                            "correct": true,
                            "indice": {
                                "en": "Red is a primary color.",
                                "fr": "Rouge est une couleur primaire."
                            }
                        },
                        {
                            "text": {
                                "en": "Blue",
                                "fr": "Bleu"
                            },
                            "correct": true,
                            "indice": {
                                "en": "Blue is a primary color.",
                                "fr": "Bleu est une couleur primaire."
                            }
                        },
                        {
                            "text": {
                                "en": "Green",
                                "fr": "Vert"
                            },
                            "correct": false,
                            "indice": {
                                "en": "Green is a secondary color.",
                                "fr": "Vert est une couleur secondaire."
                            }
                        },
                        {
                            "text": {
                                "en": "Yellow",
                                "fr": "Jaune"
                            },
                            "correct": true,
                            "indice": {
                                "en": "Yellow is a primary color.",
                                "fr": "Jaune est une couleur primaire."
                            }
                        }
                    ]
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
                        {
                            "text": {
                                "en": "Oxygen",
                                "fr": "Oxygène"
                            },
                            "correct": true,
                            "indice": {
                                "en": "",
                                "fr": ""
                            }
                        },
                        {
                            "text": {
                                "en": "Gold",
                                "fr": "Or"
                            },
                            "correct": false,
                            "indice": {
                                "en": "The symbol for gold is 'Au'.",
                                "fr": "Le symbole de l'or est 'Au'."
                            }
                        },
                        {
                            "text": {
                                "en": "Osmium",
                                "fr": "Osmium"
                            },
                            "correct": false,
                            "indice": {
                                "en": "The symbol for osmium is 'Os'.",
                                "fr": "Le symbole de l'osmium est 'Os'."
                            }
                        },
                        {
                            "text": {
                                "en": "Hydrogen",
                                "fr": "Hydrogène"
                            },
                            "correct": false,
                            "indice": {
                                "en": "The symbol for hydrogen is 'H'.",
                                "fr": "Le symbole de l'hydrogène est 'H'."
                            }
                        }
                    ]
                },
                {
                    "type": "true-false",
                    "question": {
                        "en": "Water boils at 100°C.",
                        "fr": "L'eau bout à 100°C."
                    },
                    "options": [
                        {
                            "text": {
                                "en": "True",
                                "fr": "Vrai"
                            },
                            "correct": true,
                            "indice": {
                                "en": "",
                                "fr": ""
                            }
                        },
                        {
                            "text": {
                                "en": "False",
                                "fr": "Faux"
                            },
                            "correct": false,
                            "indice": {
                                "en": "At sea level, water boils at 100°C.",
                                "fr": "Au niveau de la mer, l'eau bout à 100°C."
                            }
                        }
                    ]
                },
                {
                    "type": "fill-in-the-blank",
                    "question": {
                        "en": "The chemical formula for water is ___.",
                        "fr": "La formule chimique de l'eau est ___."
                    },
                    "answer": {
                        "en": "H2O",
                        "fr": "H2O"
                    },
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


### Step x: Update `mkdocs.yml`

Ensure the CSS and JavaScript files are referenced in your `mkdocs.yml`:
```yaml
extra_css:
  - stylesheets/extra.css
  - https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css


extra_javascript:
  - javascripts/extra.js
```

### Step y: Test the Plugin

Run MkDocs to test the updated plugin:
```bash
mkdocs serve
```

Example Markdown with Quizzes
Here’s how you can reference quizzes in your markdown files:

Example `docs/index.md`

```
# Page 1

This is a quiz about geography.

<!-- QUIZ_ID: quiz1 -->

# Page 2

This is a quiz about space.

<!-- QUIZ_ID: quiz2 -->

```


________________________________________________________________________________________________________________________


# Testing

### Step 1 : Create a `tox.ini` file 

Update `tox.ini` to include Python versions 3.7 to 3.11:

#### `tox.ini`
```ini
[tox]
envlist = py37, py38, py39, py310, py311

[testenv]
deps = 
    pytest
    mkdocs
commands = pytest tests
```

### Step 2: Running the Tests

To run the tests just use `tox` command 🚀

By following these steps, you should be able to set up a complete testing pipeline to test your MkDocs plugin across Python versions 3.7 to 3.11. If you encounter any issues or need further assistance, feel free to open an issue !


________________________________________________________________________________________________________________________

# Hint 1: Allow Multiple Quiz Formats

To support multiple quiz formats like multiple-choice, true/false, and fill-in-the-blank, we need to extend our JSON structure and adjust our plugin to handle different types of quizzes. We'll also enhance the JavaScript to process user interactions for each quiz type.

#### Step 1: Update JSON Structure

Enhance the `quizzes.json` file to include different types of quizzes:

**quizzes.json:**
```json
{
    "quizzes": {
        "quiz1": {
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
        "quiz2": {
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
        "quiz3": {
            "type": "fill-in-the-blank",
            "question": {
                "en": "____ is the capital of France.",
                "fr": "____ est la capitale de la France."
            },
            "answer": { "en": "Paris", "fr": "Paris" },
            "indice": {
                "en": "The city of lights.",
                "fr": "La ville des lumières."
            }
        }
    }
}
```

#### Step 2: Update Plugin Code

Modify the plugin to handle different quiz types:

**plugin.py:**
```python
import re
import uuid
import json
from mkdocs.plugins import BasePlugin
import os

class QuizPlugin(BasePlugin):
    config_scheme = (
        ('quiz_file', str),
        ('language', str, 'en'),
    )

    def on_config(self, config):
        quiz_file_path = self.config.get('quiz_file')
        self.language = self.config.get('language', 'en')
        if quiz_file_path and os.path.isfile(quiz_file_path):
            with open(quiz_file_path, 'r') as file:
                self.quiz_data = json.load(file)
        else:
            self.quiz_data = {'quizzes': {}}
        return config

    def on_page_markdown(self, markdown, page, config, files):
        quiz_placeholder_pattern = re.compile(r'<!-- QUIZ_ID: (\w+) -->')
        matches = quiz_placeholder_pattern.findall(markdown)

        for quiz_id in matches:
            if quiz_id in self.quiz_data['quizzes']:
                quiz_html = self.generate_quiz_html(self.quiz_data['quizzes'][quiz_id])
                markdown = markdown.replace(f'<!-- QUIZ_ID: {quiz_id} -->', quiz_html)

        return markdown

    def generate_quiz_html(self, quiz):
        quiz_id = uuid.uuid4().hex
        question = quiz['question'].get(self.language, quiz['question']['en'])
        quiz_type = quiz.get('type', 'multiple-choice')

        if quiz_type == 'multiple-choice':
            options = quiz['options']
            quiz_html = f"""
            <div class='quiz p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='quiz-{quiz_id}' data-quiz-id='{quiz_id}' data-quiz-type='{quiz_type}'>
                <p class='font-bold text-lg mb-4'>{question}</p>
                <ul class='list-none p-0'>
            """
            for i, option in enumerate(options):
                text = option['text'].get(self.language, option['text']['en'])
                indice = option['indice'].get(self.language, option['indice']['en'])
                correct = 'correct' if option['correct'] else 'incorrect'
                quiz_html += f"""
                    <li class='{correct} p-2 mb-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-100' data-quiz-id='{quiz_id}' data-option-id='{i}' data-indice='{indice}'>
                        {text}
                    </li>
                """
            quiz_html += f"""
                </ul>
                <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{quiz_id}'></div>
            </div>
            """
        elif quiz_type == 'true-false':
            options = quiz['options']
            quiz_html = f"""
            <div class='quiz p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='quiz-{quiz_id}' data-quiz-id='{quiz_id}' data-quiz-type='{quiz_type}'>
                <p class='font-bold text-lg mb-4'>{question}</p>
                <ul class='list-none p-0'>
            """
            for i, option in enumerate(options):
                text = option['text'].get(self.language, option['text']['en'])
                indice = option['indice'].get(self.language, option['indice']['en'])
                correct = 'correct' if option['correct'] else 'incorrect'
                quiz_html += f"""
                    <li class='{correct} p-2 mb-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-100' data-quiz-id='{quiz_id}' data-option-id='{i}' data-indice='{indice}'>
                        {text}
                    </li>
                """
            quiz_html += f"""
                </ul>
                <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{quiz_id}'></div>
            </div>
            """
        elif quiz_type == 'fill-in-the-blank':
            answer = quiz['answer'].get(self.language, quiz['answer']['en'])
            indice = quiz['indice'].get(self.language, quiz['indice']['en'])
            quiz_html = f"""
            <div class='quiz p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='quiz-{quiz_id}' data-quiz-id='{quiz_id}' data-quiz-type='{quiz_type}' data-answer='{answer}'>
                <p class='font-bold text-lg mb-4'>{question}</p>
                <input type='text' class='p-2 mb-2 border border-gray-200 rounded-lg' id='answer-{quiz_id}'>
                <button class='submit-answer bg-blue-500 text-white p-2 rounded-lg' data-quiz-id='{quiz_id}'>Submit</button>
                <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{quiz_id}'>{indice}</div>
            </div>
            """
        return quiz_html
```

#### Step 3: Update JavaScript for Interaction

Enhance the JavaScript to handle interactions for different quiz types:

**extra.js:**
```javascript
document.addEventListener("DOMContentLoaded", function() {
    const quizzes = document.querySelectorAll('.quiz');
    
    quizzes.forEach(quiz => {
        const quizType = quiz.getAttribute('data-quiz-type');
        if (quizType === 'multiple-choice' || quizType === 'true-false') {
            const options = quiz.querySelectorAll('li');
            const indiceDiv = quiz.querySelector('.indice');
            options.forEach(option => {
                option.addEventListener('click', () => {
                    option.parentElement.querySelectorAll('li').forEach(li => li.classList.remove('selected', 'font-bold', 'border-blue-500', 'bg-blue-100'));
                    option.classList.add('selected', 'font-bold', 'border-blue-500', 'bg-blue-100');

                    // Show indice for incorrect answers
                    if (option.classList.contains('incorrect')) {
                        indiceDiv.textContent = option.getAttribute('data-indice');
                        indiceDiv.classList.remove('hidden');
                        option.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                    } else {
                        indiceDiv.classList.add('hidden');
                        option.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                    }

                    // Check if all quizzes are answered
                    const allQuizzesAnswered = [...quizzes].every(q => q.querySelector('li.selected'));
                    if (allQuizzesAnswered

) {
                        showResults();
                    }
                });
            });
        } else if (quizType === 'fill-in-the-blank') {
            const submitButton = quiz.querySelector('.submit-answer');
            const answerInput = quiz.querySelector(`#answer-${quiz.id.split('-')[1]}`);
            const indiceDiv = quiz.querySelector('.indice');
            const correctAnswer = quiz.getAttribute('data-answer');

            submitButton.addEventListener('click', () => {
                if (answerInput.value.trim().toLowerCase() === correctAnswer.trim().toLowerCase()) {
                    answerInput.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                    indiceDiv.classList.add('hidden');
                } else {
                    answerInput.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                    indiceDiv.classList.remove('hidden');
                }
            });
        }
    });

    function showResults() {
        quizzes.forEach(quiz => {
            let score = 0;
            const selectedOption = quiz.querySelector('li.selected');
            if (selectedOption && selectedOption.classList.contains('correct')) {
                selectedOption.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                score += 1;
            } else if (selectedOption) {
                selectedOption.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
            }
            const scoreDiv = quiz.querySelector('.score');
            if (scoreDiv) {
                scoreDiv.textContent = `Your score: ${score}/${quizzes.length}`;
                scoreDiv.classList.remove('hidden');
            }
        });
    }
});
```

### Step 4: Update Tests

Enhance the tests to cover the new quiz types:

**tests/test_plugin.py:**
```python
import os
import json
import unittest
from mkdocs.config import Config
from mkdocs.structure.pages import Page
from my_quiz_plugin.plugin import QuizPlugin

class TestQuizPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = QuizPlugin()
        self.plugin.config = {
            'quiz_file': os.path.join(os.path.dirname(__file__), '..', 'quizzes.json')
        }
        self.plugin.on_config(Config())

    def test_load_quiz_data(self):
        self.assertIn('quizzes', self.plugin.quiz_data)
        self.assertIn('quiz1', self.plugin.quiz_data['quizzes'])
        self.assertIn('quiz2', self.plugin.quiz_data['quizzes'])
        self.assertIn('quiz3', self.plugin.quiz_data['quizzes'])

    def test_generate_quiz_html_multiple_choice(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('What is the capital of France?', quiz_html)
        self.assertIn('Berlin', quiz_html)
        self.assertIn('Madrid', quiz_html)
        self.assertIn('Paris', quiz_html)
        self.assertIn('Rome', quiz_html)

    def test_generate_quiz_html_true_false(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz2']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('The Earth is flat.', quiz_html)
        self.assertIn('True', quiz_html)
        self.assertIn('False', quiz_html)

    def test_generate_quiz_html_fill_in_the_blank(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz3']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('____ is the capital of France.', quiz_html)
        self.assertIn("Paris", quiz_html)

    def test_on_page_markdown(self):
        markdown = """
        # Sample Page

        <!-- QUIZ_ID: quiz1 -->
        """
        page = Page('Sample Page', None, None, None)
        updated_markdown = self.plugin.on_page_markdown(markdown, page, Config(), None)
        self.assertIn('What is the capital of France?', updated_markdown)
        self.assertIn('Berlin', updated_markdown)
        self.assertIn('Madrid', updated_markdown)
        self.assertIn('Paris', updated_markdown)
        self.assertIn('Rome', updated_markdown)

    def test_hint_functionality(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('data-indice="This is the capital of Germany."', quiz_html)
        self.assertIn('data-indice="This is the capital of Spain."', quiz_html)
        self.assertIn('data-indice="This is the capital of Italy."', quiz_html)

    def test_show_correct_answer(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('correct', quiz_html)
        self.assertIn('incorrect', quiz_html)

if __name__ == '__main__':
    unittest.main()
```

### Running the Tests

To run the tests using `tox`, execute:
```bash
tox
```

This setup allows you to support multiple quiz formats (multiple-choice, true/false, and fill-in-the-blank) and provides comprehensive testing for each format. Let me know if you need further adjustments or additional features!

________________________________________________________________________________________________________________________

# Documentation

### How to Use the Quiz Plugin with a Custom JSON File in MkDocs

This guide will help you set up and use the Quiz Plugin with a custom JSON file in your MkDocs project. Follow these steps to integrate and configure the plugin with your custom quizzes.

#### Step 1: Install MkDocs

First, ensure you have MkDocs installed. If you don't have it installed, you can do so using pip:
```bash
pip install mkdocs
```

#### Step 2: Create a New MkDocs Project

If you don't already have a MkDocs project, create one:
```bash
mkdocs new my-project
cd my-project
```

#### Step 3: Add the Plugin to Your Project

1. **Create the Plugin Directory Structure:**
   ```
   my_project/
   ├── docs/
   ├── mkdocs.yml
   └── my_quiz_plugin/
       ├── __init__.py
       └── plugin.py
   ```

2. **Create the Plugin Code:**

   Create `plugin.py` in the `my_quiz_plugin` directory with the following content:

   ```python
   import re
   import uuid
   import json
   from mkdocs.plugins import BasePlugin
   import os

   class QuizPlugin(BasePlugin):
       config_scheme = (
           ('quiz_file', str),
       )

       def on_config(self, config):
           quiz_file_path = self.config.get('quiz_file')
           if quiz_file_path and os.path.isfile(quiz_file_path):
               with open(quiz_file_path, 'r') as file:
                   self.quiz_data = json.load(file)
           else:
               self.quiz_data = {'quizzes': {}}
           return config

       def on_page_markdown(self, markdown, page, config, files):
           quiz_placeholder_pattern = re.compile(r'<!-- QUIZ_ID: (\w+) -->')
           matches = quiz_placeholder_pattern.findall(markdown)

           for quiz_id in matches:
               if quiz_id in self.quiz_data['quizzes']:
                   quiz_html = self.generate_quiz_html(self.quiz_data['quizzes'][quiz_id])
                   markdown = markdown.replace(f'<!-- QUIZ_ID: {quiz_id} -->', quiz_html)

           return markdown

       def generate_quiz_html(self, quiz):
           quiz_id = uuid.uuid4().hex
           question = quiz['question']
           options = quiz['options']

           quiz_html = f"""
           <div class='quiz p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='quiz-{quiz_id}'>
               <p class='font-bold text-lg mb-4'>{question}</p>
               <ul class='list-none p-0'>
           """
           for i, option in enumerate(options):
               correct = 'correct' if option['correct'] else 'incorrect'
               quiz_html += f"""
                   <li class='{correct} p-2 mb-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-100' data-quiz-id='{quiz_id}' data-option-id='{i}' data-indice='{option['indice']}'>
                       {option['text']}
                   </li>
               """
           quiz_html += f"""
               </ul>
               <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{quiz_id}'></div>
           </div>
           """
           return quiz_html
   ```

3. **Create a JSON File:**

   Create a JSON file with your quiz data. Save it as `quizzes.json` in the root of your project directory:

   ```json
   {
       "quizzes": {
           "quiz1": {
               "question": "What is the capital of France?",
               "options": [
                   { "text": "Berlin", "correct": false, "indice": "This is the capital of Germany." },
                   { "text": "Madrid", "correct": false, "indice": "This is the capital of Spain." },
                   { "text": "Paris", "correct": true, "indice": "" },
                   { "text": "Rome", "correct": false, "indice": "This is the capital of Italy." }
               ]
           },
           "quiz2": {
               "question": "Which planet is known as the Red Planet?",
               "options": [
                   { "text": "Earth", "correct": false, "indice": "This is our home planet." },
                   { "text": "Mars", "correct": true, "indice": "" },
                   { "text": "Jupiter", "correct": false, "indice": "This is the largest planet in our solar system." },
                   { "text": "Saturn", "correct": false, "indice": "This planet is famous for its rings." }
               ]
           }
       }
   }
   ```

4. **Update MkDocs Configuration:**

   Edit `mkdocs.yml` to register the plugin and specify the path to your custom JSON file:

   ```yaml
   site_name: My Docs

   plugins:
     - search
     - my_quiz_plugin:
         quiz_file: quizzes.json

   extra_css:
     - https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css

   extra_javascript:
     - javascripts/extra.js
   ```

5. **Create JavaScript File:**

   Create a JavaScript file (`docs/javascripts/extra.js`) to handle the quiz interactions:

   ```javascript
   document.addEventListener("DOMContentLoaded", function() {
       const quizzes = document.querySelectorAll('.quiz');
       
       quizzes.forEach(quiz => {
           const options = quiz.querySelectorAll('li');
           const indiceDiv = quiz.querySelector('.indice');
           options.forEach(option => {
               option.addEventListener('click', () => {
                   option.parentElement.querySelectorAll('li').forEach(li => li.classList.remove('selected', 'font-bold', 'border-blue-500', 'bg-blue-100'));
                   option.classList.add('selected', 'font-bold', 'border-blue-500', 'bg-blue-100');

                   // Show indice for incorrect answers
                   if (option.classList.contains('incorrect')) {
                       indiceDiv.textContent = option.getAttribute('data-indice');
                       indiceDiv.classList.remove('hidden');
                   } else {
                       indiceDiv.classList.add('hidden');
                   }

                   // Check if all quizzes are answered
                   const allQuizzesAnswered = [...quizzes].every(q => q.querySelector('li.selected'));
                   if (allQuizzesAnswered) {
                       showResults();
                   }
               });
           });
       });

       function showResults() {
           quizzes.forEach(quiz => {
               const selectedOption = quiz.querySelector('li.selected');
               if (selectedOption.classList.contains('correct')) {
                   selectedOption.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
               } else {
                   selectedOption.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
               }
           });
       }
   });
   ```

6. **Update Markdown Files:**

   Reference the quizzes in your markdown files using placeholders:

   ```markdown
   # Page 1

   This is a quiz about geography.

   <!-- QUIZ_ID: quiz1 -->

   # Page 2

   This is a quiz about space.

   <!-- QUIZ_ID: quiz2 -->
   ```

### Step 4: Test the Plugin

Run MkDocs to test the plugin with your custom JSON file:
```bash
mkdocs serve
```

### Step 5: Verify Functionality

Navigate through your documentation and interact with the quizzes. The quizzes should be styled using Tailwind CSS, and selecting an incorrect answer should display the corresponding hint (indice).

This documentation should provide clear steps on how to integrate and use the quiz plugin with a custom JSON file in MkDocs. Let me know if you need further adjustments or additional features!

Navigate through your documentation and interact with the quizzes. Selecting an incorrect answer should display the corresponding hint (indice).


________________________________________________________________________________________________________________________


Certainly! Let's integrate the feedback functionality into the MkDocs quiz plugin and add tests to verify this feature.

### Step 1: Update Plugin Code

We'll update the plugin to add elements for feedback and integrate the logic for displaying feedback after each answer.

#### Plugin Code (`my_quiz_plugin/plugin.py`)
```python
import re
import uuid
import json
from mkdocs.plugins import BasePlugin
import os

class QuizPlugin(BasePlugin):
    config_scheme = (
        ('quiz_file', str),
        ('language', str, 'en'),
    )

    def on_config(self, config):
        quiz_file_path = self.config.get('quiz_file')
        self.language = self.config.get('language', 'en')
        if quiz_file_path and os.path.isfile(quiz_file_path):
            with open(quiz_file_path, 'r') as file:
                self.quiz_data = json.load(file)
        else:
            self.quiz_data = {'quizzes': {}}
        return config

    def on_page_markdown(self, markdown, page, config, files):
        quiz_placeholder_pattern = re.compile(r'<!-- QUIZ_ID: (\w+) -->')
        matches = quiz_placeholder_pattern.findall(markdown)

        for quiz_id in matches:
            if quiz_id in self.quiz_data['quizzes']:
                quiz_html = self.generate_quiz_html(self.quiz_data['quizzes'][quiz_id])
                markdown = markdown.replace(f'<!-- QUIZ_ID: {quiz_id} -->', quiz_html)

        return markdown

    def generate_quiz_html(self, quiz):
        quiz_id = uuid.uuid4().hex
        question = quiz['question'].get(self.language, quiz['question']['en'])
        quiz_type = quiz.get('type', 'multiple-choice')

        if quiz_type == 'multiple-choice' or quiz_type == 'true-false':
            options = quiz['options']
            quiz_html = f"""
            <div class='quiz p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='quiz-{quiz_id}' data-quiz-id='{quiz_id}' data-quiz-type='{quiz_type}'>
                <p class='font-bold text-lg mb-4'>{question}</p>
                <ul class='list-none p-0'>
            """
            for i, option in enumerate(options):
                text = option['text'].get(self.language, option['text']['en'])
                indice = option['indice'].get(self.language, option['indice']['en'])
                correct = 'correct' if option['correct'] else 'incorrect'
                quiz_html += f"""
                    <li class='{correct} p-2 mb-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-100' data-quiz-id='{quiz_id}' data-option-id='{i}' data-indice='{indice}'>
                        {text}
                    </li>
                """
            quiz_html += f"""
                </ul>
                <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{quiz_id}'></div>
                <div class='feedback mt-4 p-3 rounded-lg hidden' id='feedback-{quiz_id}'></div>
            </div>
            """
        elif quiz_type == 'fill-in-the-blank':
            answer = quiz['answer'].get(self.language, quiz['answer']['en'])
            indice = quiz['indice'].get(self.language, quiz['indice']['en'])
            quiz_html = f"""
            <div class='quiz p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='quiz-{quiz_id}' data-quiz-id='{quiz_id}' data-quiz-type='{quiz_type}' data-answer='{answer}'>
                <p class='font-bold text-lg mb-4'>{question}</p>
                <input type='text' class='p-2 mb-2 border border-gray-200 rounded-lg' id='answer-{quiz_id}'>
                <button class='submit-answer bg-blue-500 text-white p-2 rounded-lg' data-quiz-id='{quiz_id}'>Submit</button>
                <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{quiz_id}'>{indice}</div>
                <div class='feedback mt-4 p-3 rounded-lg hidden' id='feedback-{quiz_id}'></div>
            </div>
            """
        return quiz_html
```

### Step 2: Update JavaScript for Interaction

Enhance the JavaScript to handle interactions and display feedback for each answer.

#### JavaScript (`docs/javascripts/extra.js`)
```javascript
document.addEventListener("DOMContentLoaded", function() {
    const quizzes = document.querySelectorAll('.quiz');

    quizzes.forEach(quiz => {
        const quizType = quiz.getAttribute('data-quiz-type');
        const feedbackDiv = quiz.querySelector('.feedback');

        if (quizType === 'multiple-choice' || quizType === 'true-false') {
            const options = quiz.querySelectorAll('li');
            const indiceDiv = quiz.querySelector('.indice');

            options.forEach(option => {
                option.addEventListener('click', () => {
                    option.parentElement.querySelectorAll('li').forEach(li => li.classList.remove('selected', 'font-bold', 'border-blue-500', 'bg-blue-100'));
                    option.classList.add('selected', 'font-bold', 'border-blue-500', 'bg-blue-100');

                    // Show feedback and indice for incorrect answers
                    if (option.classList.contains('incorrect')) {
                        indiceDiv.textContent = option.getAttribute('data-indice');
                        indiceDiv.classList.remove('hidden');
                        option.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                        feedbackDiv.textContent = "Incorrect!";
                        feedbackDiv.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                    } else {
                        indiceDiv.classList.add('hidden');
                        option.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                        feedbackDiv.textContent = "Correct!";
                        feedbackDiv.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                    }
                    feedbackDiv.classList.remove('hidden');
                });
            });
        } else if (quizType === 'fill-in-the-blank') {
            const submitButton = quiz.querySelector('.submit-answer');
            const answerInput = quiz.querySelector(`#answer-${quiz.id.split('-')[1]}`);
            const indiceDiv = quiz.querySelector('.indice');
            const correctAnswer = quiz.getAttribute('data-answer');

            submitButton.addEventListener('click', () => {
                if (answerInput.value.trim().toLowerCase() === correctAnswer.trim().toLowerCase()) {
                    answerInput.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                    indiceDiv.classList.add('hidden');
                    feedbackDiv.textContent = "Correct!";
                    feedbackDiv.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                } else {
                    answerInput.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                    indiceDiv.classList.remove('hidden');
                    feedbackDiv.textContent = "Incorrect!";
                    feedbackDiv.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                }
                feedbackDiv.classList.remove('hidden');
            });
        }
    });
});
```

### Step 3: Update Tests

Add tests to verify that feedback is correctly displayed after each answer.

#### Test Code (`tests/test_plugin.py`)
```python
import os
import json
import unittest
from mkdocs.config import Config
from mkdocs.structure.pages import Page
from my_quiz_plugin.plugin import QuizPlugin

class TestQuizPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = QuizPlugin()
        self.plugin.config = {
            'quiz_file': os.path.join(os.path.dirname(__file__), '..', 'quizzes.json')
        }
        self.plugin.on_config(Config())

    def test_load_quiz_data(self):
        self.assertIn('quizzes', self.plugin.quiz_data)
        self.assertIn('quiz1', self.plugin.quiz_data['quizzes'])
        self.assertIn('quiz2', self.plugin.quiz_data['quizzes'])
        self.assertIn('quiz3', self.plugin.quiz_data['quizzes'])

    def test_generate_quiz_html_multiple_choice(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('What is the capital of France?', quiz_html)
        self.assertIn('Berlin', quiz_html)
        self.assertIn('Madrid', quiz_html)
        self.assertIn('Paris', quiz_html)
        self.assertIn('Rome', quiz_html)
        self.assertIn('data-indice="This is the capital of Germany."', quiz_html)
        self.assertIn('data-indice="This is the capital of Spain."', quiz_html)
        self.assertIn('data-indice="This is the capital of Italy."', quiz_html)
        self.assertIn('feedback', quiz_html)

    def test_generate_quiz_html_true_false(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz2']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('The Earth is flat.', quiz_html)
        self.assertIn('True', quiz_html)
        self.assertIn('False', quiz_html)
        self.assertIn('feedback', quiz_html)

    def test_generate_quiz_html_fill_in_the_blank(self):
        quiz = self.plugin

.quiz_data['quizzes']['quiz3']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('____ is the capital of France.', quiz_html)
        self.assertIn("Paris", quiz_html)
        self.assertIn('feedback', quiz_html)

    def test_on_page_markdown(self):
        markdown = """
        # Sample Page

        <!-- QUIZ_ID: quiz1 -->
        """
        page = Page('Sample Page', None, None, None)
        updated_markdown = self.plugin.on_page_markdown(markdown, page, Config(), None)
        self.assertIn('What is the capital of France?', updated_markdown)
        self.assertIn('Berlin', updated_markdown)
        self.assertIn('Madrid', updated_markdown)
        self.assertIn('Paris', updated_markdown)
        self.assertIn('Rome', updated_markdown)

    def test_hint_functionality(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('data-indice="This is the capital of Germany."', quiz_html)
        self.assertIn('data-indice="This is the capital of Spain."', quiz_html)
        self.assertIn('data-indice="This is the capital of Italy."', quiz_html)

    def test_show_correct_answer(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('correct', quiz_html)
        self.assertIn('incorrect', quiz_html)

    def test_feedback_display(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('feedback', quiz_html)

if __name__ == '__main__':
    unittest.main()
```

### Running the Tests

To run the tests using `tox`, execute:
```bash
tox
```

### Complete Directory Structure

Ensure your project directory looks like this:
```
my_project/
├── docs/
│   └── javascripts/
│       └── extra.js
├── mkdocs.yml
├── my_quiz_plugin/
│   ├── __init__.py
│   └── plugin.py
├── quizzes.json
├── tests/
│   ├── __init__.py
│   └── test_plugin.py
└── tox.ini
```

### Example Files

#### `my_quiz_plugin/plugin.py`
```python
import re
import uuid
import json
from mkdocs.plugins import BasePlugin
import os

class QuizPlugin(BasePlugin):
    config_scheme = (
        ('quiz_file', str),
        ('language', str, 'en'),
    )

    def on_config(self, config):
        quiz_file_path = self.config.get('quiz_file')
        self.language = self.config.get('language', 'en')
        if quiz_file_path and os.path.isfile(quiz_file_path):
            with open(quiz_file_path, 'r') as file:
                self.quiz_data = json.load(file)
        else:
            self.quiz_data = {'quizzes': {}}
        return config

    def on_page_markdown(self, markdown, page, config, files):
        quiz_placeholder_pattern = re.compile(r'<!-- QUIZ_ID: (\w+) -->')
        matches = quiz_placeholder_pattern.findall(markdown)

        for quiz_id in matches:
            if quiz_id in self.quiz_data['quizzes']:
                quiz_html = self.generate_quiz_html(self.quiz_data['quizzes'][quiz_id])
                markdown = markdown.replace(f'<!-- QUIZ_ID: {quiz_id} -->', quiz_html)

        return markdown

    def generate_quiz_html(self, quiz):
        quiz_id = uuid.uuid4().hex
        question = quiz['question'].get(self.language, quiz['question']['en'])
        quiz_type = quiz.get('type', 'multiple-choice')

        if quiz_type == 'multiple-choice' or quiz_type == 'true-false':
            options = quiz['options']
            quiz_html = f"""
            <div class='quiz p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='quiz-{quiz_id}' data-quiz-id='{quiz_id}' data-quiz-type='{quiz_type}'>
                <p class='font-bold text-lg mb-4'>{question}</p>
                <ul class='list-none p-0'>
            """
            for i, option in enumerate(options):
                text = option['text'].get(self.language, option['text']['en'])
                indice = option['indice'].get(self.language, option['indice']['en'])
                correct = 'correct' if option['correct'] else 'incorrect'
                quiz_html += f"""
                    <li class='{correct} p-2 mb-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-100' data-quiz-id='{quiz_id}' data-option-id='{i}' data-indice='{indice}'>
                        {text}
                    </li>
                """
            quiz_html += f"""
                </ul>
                <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{quiz_id}'></div>
                <div class='feedback mt-4 p-3 rounded-lg hidden' id='feedback-{quiz_id}'></div>
            </div>
            """
        elif quiz_type == 'fill-in-the-blank':
            answer = quiz['answer'].get(self.language, quiz['answer']['en'])
            indice = quiz['indice'].get(self.language, quiz['indice']['en'])
            quiz_html = f"""
            <div class='quiz p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='quiz-{quiz_id}' data-quiz-id='{quiz_id}' data-quiz-type='{quiz_type}' data-answer='{answer}'>
                <p class='font-bold text-lg mb-4'>{question}</p>
                <input type='text' class='p-2 mb-2 border border-gray-200 rounded-lg' id='answer-{quiz_id}'>
                <button class='submit-answer bg-blue-500 text-white p-2 rounded-lg' data-quiz-id='{quiz_id}'>Submit</button>
                <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{quiz_id}'>{indice}</div>
                <div class='feedback mt-4 p-3 rounded-lg hidden' id='feedback-{quiz_id}'></div>
            </div>
            """
        return quiz_html
```

#### `docs/javascripts/extra.js`
```javascript
document.addEventListener("DOMContentLoaded", function() {
    const quizzes = document.querySelectorAll('.quiz');

    quizzes.forEach(quiz => {
        const quizType = quiz.getAttribute('data-quiz-type');
        const feedbackDiv = quiz.querySelector('.feedback');

        if (quizType === 'multiple-choice' || quizType === 'true-false') {
            const options = quiz.querySelectorAll('li');
            const indiceDiv = quiz.querySelector('.indice');

            options.forEach(option => {
                option.addEventListener('click', () => {
                    option.parentElement.querySelectorAll('li').forEach(li => li.classList.remove('selected', 'font-bold', 'border-blue-500', 'bg-blue-100'));
                    option.classList.add('selected', 'font-bold', 'border-blue-500', 'bg-blue-100');

                    // Show feedback and indice for incorrect answers
                    if (option.classList.contains('incorrect')) {
                        indiceDiv.textContent = option.getAttribute('data-indice');
                        indiceDiv.classList.remove('hidden');
                        option.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                        feedbackDiv.textContent = "Incorrect!";
                        feedbackDiv.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                    } else {
                        indiceDiv.classList.add('hidden');
                        option.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                        feedbackDiv.textContent = "Correct!";
                        feedbackDiv.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                    }
                    feedbackDiv.classList.remove('hidden');
                });
            });
        } else if (quizType === 'fill-in-the-blank') {
            const submitButton = quiz.querySelector('.submit-answer');
            const answerInput = quiz.querySelector(`#answer-${quiz.id.split('-')[1]}`);
            const indiceDiv = quiz.querySelector('.indice');
            const correctAnswer = quiz.getAttribute('data-answer');

            submitButton.addEventListener('click', () => {
                if (answerInput.value.trim().toLowerCase() === correctAnswer.trim().toLowerCase()) {
                    answerInput.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                    indiceDiv.classList.add('hidden');
                    feedbackDiv.textContent = "Correct!";
                    feedbackDiv.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                } else {
                    answerInput.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                    indiceDiv.classList.remove('hidden');
                    feedbackDiv.textContent = "Incorrect!";
                    feedbackDiv.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                }
                feedbackDiv.classList.remove('hidden');
            });
        }
    });
});
```

#### `tests/test_plugin.py`
```python
import os
import json
import

 unittest
from mkdocs.config import Config
from mkdocs.structure.pages import Page
from my_quiz_plugin.plugin import QuizPlugin

class TestQuizPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = QuizPlugin()
        self.plugin.config = {
            'quiz_file': os.path.join(os.path.dirname(__file__), '..', 'quizzes.json')
        }
        self.plugin.on_config(Config())

    def test_load_quiz_data(self):
        self.assertIn('quizzes', self.plugin.quiz_data)
        self.assertIn('quiz1', self.plugin.quiz_data['quizzes'])
        self.assertIn('quiz2', self.plugin.quiz_data['quizzes'])
        self.assertIn('quiz3', self.plugin.quiz_data['quizzes'])

    def test_generate_quiz_html_multiple_choice(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('What is the capital of France?', quiz_html)
        self.assertIn('Berlin', quiz_html)
        self.assertIn('Madrid', quiz_html)
        self.assertIn('Paris', quiz_html)
        self.assertIn('Rome', quiz_html)
        self.assertIn('data-indice="This is the capital of Germany."', quiz_html)
        self.assertIn('data-indice="This is the capital of Spain."', quiz_html)
        self.assertIn('data-indice="This is the capital of Italy."', quiz_html)
        self.assertIn('feedback', quiz_html)

    def test_generate_quiz_html_true_false(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz2']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('The Earth is flat.', quiz_html)
        self.assertIn('True', quiz_html)
        self.assertIn('False', quiz_html)
        self.assertIn('feedback', quiz_html)

    def test_generate_quiz_html_fill_in_the_blank(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz3']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('____ is the capital of France.', quiz_html)
        self.assertIn("Paris", quiz_html)
        self.assertIn('feedback', quiz_html)

    def test_on_page_markdown(self):
        markdown = """
        # Sample Page

        <!-- QUIZ_ID: quiz1 -->
        """
        page = Page('Sample Page', None, None, None)
        updated_markdown = self.plugin.on_page_markdown(markdown, page, Config(), None)
        self.assertIn('What is the capital of France?', updated_markdown)
        self.assertIn('Berlin', updated_markdown)
        self.assertIn('Madrid', updated_markdown)
        self.assertIn('Paris', updated_markdown)
        self.assertIn('Rome', updated_markdown)

    def test_hint_functionality(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('data-indice="This is the capital of Germany."', quiz_html)
        self.assertIn('data-indice="This is the capital of Spain."', quiz_html)
        self.assertIn('data-indice="This is the capital of Italy."', quiz_html)

    def test_show_correct_answer(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('correct', quiz_html)
        self.assertIn('incorrect', quiz_html)

    def test_feedback_display(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('feedback', quiz_html)

if __name__ == '__main__':
    unittest.main()
```

With these changes, your MkDocs quiz plugin will provide immediate feedback after each answer, enhancing the user experience. You can now run the tests to verify the functionality and ensure everything is working as expected. If you have any further questions or need additional features, feel free to ask!


______________________________________________________________________________________________________________

Certainly! Below is an example JSON file that includes multiple quizzes, each containing multiple questions. This file can be used to test your MkDocs quiz plugin.

### quizzes.json

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

### Step 4: Update Plugin Code to Handle Multiple Questions

Modify the plugin to handle quizzes with multiple questions.

#### Plugin Code (`my_quiz_plugin/plugin.py`)
```python
import re
import uuid
import json
from mkdocs.plugins import BasePlugin
import os

class QuizPlugin(BasePlugin):
    config_scheme = (
        ('quiz_file', str),
        ('language', str, 'en'),
    )

    def on_config(self, config):
        quiz_file_path = self.config.get('quiz_file')
        self.language = self.config.get('language', 'en')
        if quiz_file_path and os.path.isfile(quiz_file_path):
            with open(quiz_file_path, 'r') as file:
                self.quiz_data = json.load(file)
        else:
            self.quiz_data = {'quizzes': {}}
        return config

    def on_page_markdown(self, markdown, page, config, files):
        quiz_placeholder_pattern = re.compile(r'<!-- QUIZ_ID: (\w+) -->')
        matches = quiz_placeholder_pattern.findall(markdown)

        for quiz_id in matches:
            if quiz_id in self.quiz_data['quizzes']:
                quiz_html = self.generate_quiz_html(self.quiz_data['quizzes'][quiz_id])
                markdown = markdown.replace(f'<!-- QUIZ_ID: {quiz_id} -->', quiz_html)

        return markdown

    def generate_quiz_html(self, quiz):
        quiz_id = uuid.uuid4().hex
        questions = quiz['questions']
        quiz_html = f"<div class='quiz' id='quiz-{quiz_id}'>"

        for question in questions:
            question_id = uuid.uuid4().hex
            question_text = question['question'].get(self.language, question['question']['en'])
            quiz_type = question.get('type', 'multiple-choice')

            if quiz_type == 'multiple-choice' or quiz_type == 'true-false':
                options = question['options']
                quiz_html += f"""
                <div class='question p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='question-{question_id}' data-quiz-id='{quiz_id}' data-question-id='{question_id}' data-quiz-type='{quiz_type}'>
                    <p class='font-bold text-lg mb-4'>{question_text}</p>
                    <ul class='list-none p-0'>
                """
                for i, option in enumerate(options):
                    text = option['text'].get(self.language, option['text']['en'])
                    indice = option['indice'].get(self.language, option['indice']['en'])
                    correct = 'correct' if option['correct'] else 'incorrect'
                    quiz_html += f"""
                        <li class='{correct} p-2 mb-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-100' data-quiz-id='{quiz_id}' data-question-id='{question_id}' data-option-id='{i}' data-indice='{indice}'>
                            {text}
                        </li>
                    """
                quiz_html += f"""
                    </ul>
                    <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{question_id}'></div>
                    <div class='feedback mt-4 p-3 rounded-lg hidden' id='feedback-{question_id}'></div>
                </div>
                """
            elif quiz_type == 'fill-in-the-blank':
                answer = question['answer'].get(self.language, question['answer']['en'])
                indice = question['indice'].get(self.language, question['indice']['en'])
                quiz_html += f"""
                <div class='question p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='question-{question_id}' data-quiz-id='{quiz_id}' data-question-id='{question_id}' data-quiz-type='{quiz_type}' data-answer='{answer}'>
                    <p class='font-bold text-lg mb-4'>{question_text}</p>
                    <input type='text' class='p-2 mb-2 border border-gray-200 rounded-lg' id='answer-{question_id}'>
                    <button class='submit-answer bg-blue-500 text-white p-2 rounded-lg' data-quiz-id='{quiz_id}' data-question-id='{question_id}'>Submit</button>
                    <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text

-yellow-700 rounded-lg hidden' id='indice-{question_id}'>{indice}</div>
                    <div class='feedback mt-4 p-3 rounded-lg hidden' id='feedback-{question_id}'></div>
                </div>
                """

        quiz_html += "</div>"
        return quiz_html
```

### Step 5: Update JavaScript to Handle Multiple Questions

Ensure the JavaScript handles interactions for each question within a quiz.

#### JavaScript (`docs/javascripts/extra.js`)
```javascript
document.addEventListener("DOMContentLoaded", function() {
    const quizzes = document.querySelectorAll('.quiz');

    quizzes.forEach(quiz => {
        const questions = quiz.querySelectorAll('.question');

        questions.forEach(question => {
            const quizType = question.getAttribute('data-quiz-type');
            const feedbackDiv = question.querySelector('.feedback');

            if (quizType === 'multiple-choice' || quizType === 'true-false') {
                const options = question.querySelectorAll('li');
                const indiceDiv = question.querySelector('.indice');

                options.forEach(option => {
                    option.addEventListener('click', () => {
                        option.parentElement.querySelectorAll('li').forEach(li => li.classList.remove('selected', 'font-bold', 'border-blue-500', 'bg-blue-100'));
                        option.classList.add('selected', 'font-bold', 'border-blue-500', 'bg-blue-100');

                        // Show feedback and indice for incorrect answers
                        if (option.classList.contains('incorrect')) {
                            indiceDiv.textContent = option.getAttribute('data-indice');
                            indiceDiv.classList.remove('hidden');
                            option.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                            feedbackDiv.textContent = "Incorrect!";
                            feedbackDiv.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                        } else {
                            indiceDiv.classList.add('hidden');
                            option.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                            feedbackDiv.textContent = "Correct!";
                            feedbackDiv.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                        }
                        feedbackDiv.classList.remove('hidden');
                    });
                });
            } else if (quizType === 'fill-in-the-blank') {
                const submitButton = question.querySelector('.submit-answer');
                const answerInput = question.querySelector(`#answer-${question.id.split('-')[1]}`);
                const indiceDiv = question.querySelector('.indice');
                const correctAnswer = question.getAttribute('data-answer');

                submitButton.addEventListener('click', () => {
                    if (answerInput.value.trim().toLowerCase() === correctAnswer.trim().toLowerCase()) {
                        answerInput.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                        indiceDiv.classList.add('hidden');
                        feedbackDiv.textContent = "Correct!";
                        feedbackDiv.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                    } else {
                        answerInput.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                        indiceDiv.classList.remove('hidden');
                        feedbackDiv.textContent = "Incorrect!";
                        feedbackDiv.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                    }
                    feedbackDiv.classList.remove('hidden');
                });
            }
        });
    });
});
```

### Step 6: Update Tests to Verify Multiple Questions

Modify the tests to ensure that multiple questions within a quiz are handled correctly.

#### Test Code (`tests/test_plugin.py`)
```python
import os
import json
import unittest
from mkdocs.config import Config
from mkdocs.structure.pages import Page
from my_quiz_plugin.plugin import QuizPlugin

class TestQuizPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = QuizPlugin()
        self.plugin.config = {
            'quiz_file': os.path.join(os.path.dirname(__file__), '..', 'quizzes.json')
        }
        self.plugin.on_config(Config())

    def test_load_quiz_data(self):
        self.assertIn('quizzes', self.plugin.quiz_data)
        self.assertIn('quiz1', self.plugin.quiz_data['quizzes'])
        self.assertIn('quiz2', self.plugin.quiz_data['quizzes'])

    def test_generate_quiz_html_multiple_choice(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        self.assertIn('What is the capital of France?', quiz_html)
        self.assertIn('Berlin', quiz_html)
        self.assertIn('Madrid', quiz_html)
        self.assertIn('Paris', quiz_html)
        self.assertIn('Rome', quiz_html)
        self.assertIn('data-indice="This is the capital of Germany."', quiz_html)
        self.assertIn('data-indice="This is the capital of Spain."', quiz_html)
        self.assertIn('data-indice="This is the capital of Italy."', quiz_html)
        self.assertIn('feedback', quiz_html)

    def test_generate_quiz_html_true_false(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        question = quiz['questions'][1]
        quiz_html = self.plugin.generate_quiz_html({'questions': [question]})
        self.assertIn('The Earth is flat.', quiz_html)
        self.assertIn('True', quiz_html)
        self.assertIn('False', quiz_html)
        self.assertIn('feedback', quiz_html)

    def test_generate_quiz_html_fill_in_the_blank(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        question = quiz['questions'][2]
        quiz_html = self.plugin.generate_quiz_html({'questions': [question]})
        self.assertIn('____ is the largest planet in our solar system.', quiz_html)
        self.assertIn("Jupiter", quiz_html)
        self.assertIn('feedback', quiz_html)

    def test_on_page_markdown(self):
        markdown = """
        # Sample Page

        <!-- QUIZ_ID: quiz1 -->
        """
        page = Page('Sample Page', None, None, None)
        updated_markdown = self.plugin.on_page_markdown(markdown, page, Config(), None)
        self.assertIn('What is the capital of France?', updated_markdown)
        self.assertIn('Berlin', updated_markdown)
        self.assertIn('Madrid', updated_markdown)
        self.assertIn('Paris', updated_markdown)
        self.assertIn('Rome', updated_markdown)

    def test_hint_functionality(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        question = quiz['questions'][0]
        quiz_html = self.plugin.generate_quiz_html({'questions': [question]})
        self.assertIn('data-indice="This is the capital of Germany."', quiz_html)
        self.assertIn('data-indice="This is the capital of Spain."', quiz_html)
        self.assertIn('data-indice="This is the capital of Italy."', quiz_html)

    def test_show_correct_answer(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        question = quiz['questions'][0]
        quiz_html = self.plugin.generate_quiz_html({'questions': [question]})
        self.assertIn('correct', quiz_html)
        self.assertIn('incorrect', quiz_html)

    def test_feedback_display(self):
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        question = quiz['questions'][0]
        quiz_html = self.plugin.generate_quiz_html({'questions': [question]})
        self.assertIn('feedback', quiz_html)

if __name__ == '__main__':
    unittest.main()
```

With these changes, your MkDocs quiz plugin will support multiple questions within each quiz, providing a richer and more interactive experience for users. You can now run the tests to verify the functionality and ensure everything is working as expected. If you have any further questions or need additional features, feel free to ask!

______________________________________________________________________________________________________________


# Push to PyPi

Sure! Here are the steps to push your Python package to PyPI:

### 1. Update `setup.py` with necessary metadata

Make sure your `setup.py` contains all the necessary metadata for PyPI:

```python
from setuptools import setup, find_packages

setup(
    name='my_quiz_plugin',
    version='0.1',
    description='A MkDocs plugin to create quizzes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/my_quiz_plugin',
    packages=find_packages(),
    install_requires=[
        'mkdocs>=1.0.4',
    ],
    entry_points={
        'mkdocs.plugins': [
            'my_quiz_plugin = my_quiz_plugin.plugin:QuizPlugin'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
```

### 2. Create a `.pypirc` file (optional but recommended)

A `.pypirc` file stores your PyPI credentials, making the upload process easier. Create this file in your home directory (`~/.pypirc`):

```ini
[distutils]
index-servers =
  pypi

[pypi]
username = yourusername
password = yourpassword
```

### 3. Build your package

Use `setuptools` and `wheel` to build your package:

```bash
python setup.py sdist bdist_wheel
```

### 4. Upload your package to PyPI

Use `twine` to securely upload your package:

```bash
pip install twine
twine upload dist/*
```

If you didn't create a `.pypirc` file, you'll need to provide your username and password during the upload process.

### 5. Automate with GitHub Actions

You can also automate this process using GitHub Actions. Here is an example workflow file (`release.yml`) to automate the release on tag creation:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  build-and-publish:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.7

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install setuptools wheel twine

    - name: Build package
      run: |
        python setup.py sdist bdist_wheel

    - name: Publish package
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        twine upload dist/*
```

### 6. Add PyPI credentials to GitHub Secrets

1. Go to your GitHub repository.
2. Navigate to `Settings` > `Secrets` > `New repository secret`.
3. Add `PYPI_USERNAME` with your PyPI username.
4. Add `PYPI_PASSWORD` with your PyPI password.

### Summary

By following these steps, you will be able to push your Python package to PyPI and automate the process using GitHub Actions. This ensures that your package is uploaded to PyPI whenever you create a new tag in your repository.