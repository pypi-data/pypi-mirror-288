import os
import sys
import unittest
from bs4 import BeautifulSoup
from mkdocs.config import Config, config_options
from mkdocs.structure.pages import Page
from mkdocs.structure.files import File

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from my_quiz_plugin.plugin import QuizPlugin

class TestQuizPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = QuizPlugin()
        self.mock_schema = (
            ('site_name', config_options.Type(str, default='My Docs')),
            ('site_url', config_options.Type(str, default='')),
            ('repo_url', config_options.Type(str, default='')),
            ('site_author', config_options.Type(str, default='')),
            ('site_description', config_options.Type(str, default='')),
        )
        self.config = Config(self.mock_schema)

    def load_plugin_config(self, show_indice_on_answer, show_score, show_progress_bar):
        self.plugin.config = {
            'quiz_file': os.path.join(os.path.dirname(__file__), '..', 'quizzes.json'),
            'language': 'en',
            'show_indice_on_answer': show_indice_on_answer,
            'show_score': show_score,
            'show_progress_bar': show_progress_bar
        }
        self.config.load_dict(self.plugin.config)
        self.plugin.on_config(self.config)

    def test_load_quiz_data(self):
        self.load_plugin_config(True, True, True)
        self.assertIn('quizzes', self.plugin.quiz_data)
        self.assertIn('quiz1', self.plugin.quiz_data['quizzes'])
        self.assertIn('quiz2', self.plugin.quiz_data['quizzes'])

    def test_generate_quiz_html(self):
        self.load_plugin_config(True, True, True)
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
    
        soup = BeautifulSoup(quiz_html, 'html.parser')
        
        # Find the question text without considering the HTML tags
        self.assertTrue(soup.find_all(string=lambda text: 'What is the capital of France?' in text))

        # Check the presence of options in the quiz
        options = [li.get_text(strip=True) for li in soup.find_all('li')]
        self.assertIn('Berlin', options)
        self.assertIn('Madrid', options)
        self.assertIn('Paris', options)
        self.assertIn('Rome', options)

        # Check the presence of indices
        indices = [li['data-indice'] for li in soup.find_all('li')]
        self.assertIn('This is the capital of Germany.', indices)
        self.assertIn('This is the capital of Spain.', indices)
        self.assertIn('Paris is the city of light', indices)
        self.assertIn('This is the capital of Italy.', indices)

    def test_on_page_markdown(self):
        self.load_plugin_config(True, True, True)
        markdown = """
        # Sample Page

        <!-- QUIZ_ID: quiz1 -->
        """
        file = File('sample_page.md', 'docs', 'site', False)
        page = Page('Sample Page', file, self.config)
    
        # Mock quiz data
        self.plugin.quiz_data = {
            'quizzes': {
                'quiz1': {
                    'questions': [
                        {
                            'question': {
                                'en': 'What is the capital of France?'
                            },
                            'type': 'multiple-choice',
                            'options': [
                                {'text': {'en': 'Berlin'}, 'correct': False, 'indice': {'en': 'This is the capital of Germany.'}},
                                {'text': {'en': 'Madrid'}, 'correct': False, 'indice': {'en': 'This is the capital of Spain.'}},
                                {'text': {'en': 'Paris'}, 'correct': True, 'indice': {'en': 'Paris is the city of light'}},
                                {'text': {'en': 'Rome'}, 'correct': False, 'indice': {'en': 'This is the capital of Italy.'}}
                            ]
                        }
                    ]
                }
            }
        }
    
        updated_markdown = self.plugin.on_page_markdown(markdown, page, self.config, None)
    
        # Replace placeholders with actual content for the test
        for placeholder, quiz_html in page.meta['quiz_placeholder']:
            updated_markdown = updated_markdown.replace(placeholder, quiz_html)
    
        soup = BeautifulSoup(updated_markdown, 'html.parser')
    
        # Find the question text without considering the HTML tags
        self.assertTrue(soup.find_all(string=lambda text: 'What is the capital of France?' in text))

        # Check the presence of options in the quiz
        options = [li.get_text(strip=True) for li in soup.find_all('li')]
        self.assertIn('Berlin', options)
        self.assertIn('Madrid', options)
        self.assertIn('Paris', options)
        self.assertIn('Rome', options)

    def test_hint_functionality(self):
        self.load_plugin_config(True, True, True)
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)

        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Check the presence of indices
        indices = [li['data-indice'] for li in soup.find_all('li')]
        self.assertIn('This is the capital of Germany.', indices)
        self.assertIn('This is the capital of Spain.', indices)
        self.assertIn('Paris is the city of light', indices)
        self.assertIn('This is the capital of Italy.', indices)

    def test_show_correct_answer(self):
        self.load_plugin_config(True, True, True)
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)

        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Check for the presence of correct and incorrect classes
        self.assertTrue(soup.find(class_='correct'))
        self.assertTrue(soup.find(class_='incorrect'))

    def test_show_indice_on_answer_true(self):
        self.load_plugin_config(True, True, True)
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        soup = BeautifulSoup(quiz_html, 'html.parser')
        
        # Check for the presence of the hint button
        hint_button = soup.find('button', class_='hint-button')
        self.assertIsNotNone(hint_button)

    def test_show_indice_on_answer_false(self):
        self.load_plugin_config(False, True, True)
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        soup = BeautifulSoup(quiz_html, 'html.parser')
        
        # Check for the absence of the hint button
        hint_button = soup.find('button', class_='hint-button')
        self.assertIsNone(hint_button)
    
    def test_multi_choice_question(self):
        self.load_plugin_config(True, True, True)
        quiz = {
            "questions": [
                {
                    "type": "multi-choice",
                    "question": {
                        "en": "Select all prime numbers.",
                        "fr": "Sélectionnez tous les nombres premiers."
                    },
                    "options": [
                        {
                            "text": {
                                "en": "2",
                                "fr": "2"
                            },
                            "correct": True,
                            "indice": {
                                "en": "2 is a prime number.",
                                "fr": "2 est un nombre premier."
                            }
                        },
                        {
                            "text": {
                                "en": "3",
                                "fr": "3"
                            },
                            "correct": True,
                            "indice": {
                                "en": "3 is a prime number.",
                                "fr": "3 est un nombre premier."
                            }
                        },
                        {
                            "text": {
                                "en": "4",
                                "fr": "4"
                            },
                            "correct": False,
                            "indice": {
                                "en": "4 is not a prime number.",
                                "fr": "4 n'est pas un nombre premier."
                            }
                        },
                        {
                            "text": {
                                "en": "5",
                                "fr": "5"
                            },
                            "correct": True,
                            "indice": {
                                "en": "5 is a prime number.",
                                "fr": "5 est un nombre premier."
                            }
                        }
                    ]
                }
            ]
        }
        quiz_html = self.plugin.generate_quiz_html(quiz)
    
        soup = BeautifulSoup(quiz_html, 'html.parser')
        
        # Find the question text without considering the HTML tags
        self.assertTrue(soup.find_all(string=lambda text: 'Select all prime numbers.' in text))

        # Check the presence of checkboxes in the multi-choice quiz
        checkboxes = [input_ for input_ in soup.find_all('input', {'type': 'checkbox'})]
        self.assertEqual(len(checkboxes), 4)

    def test_score_computation(self):
        self.load_plugin_config(True, True, True)
        quiz = {
            "questions": [
                {
                    "type": "multiple-choice",
                    "question": {
                        "en": "What is 2 + 2?",
                        "fr": "Qu'est-ce que 2 + 2?"
                    },
                    "options": [
                        {
                            "text": {
                                "en": "3",
                                "fr": "3"
                            },
                            "correct": False,
                            "indice": {
                                "en": "This is incorrect.",
                                "fr": "Ceci est incorrect."
                            }
                        },
                        {
                            "text": {
                                "en": "4",
                                "fr": "4"
                            },
                            "correct": True,
                            "indice": {
                                "en": "This is correct.",
                                "fr": "Ceci est correct."
                            }
                        }
                    ]
                },
                {
                    "type": "fill-in-the-blank",
                    "question": {
                        "en": "The capital of France is ___.",
                        "fr": "La capitale de la France est ___."
                    },
                    "answer": {
                        "en": "Paris",
                        "fr": "Paris"
                    },
                    "indice": {
                        "en": "It is known as the city of light.",
                        "fr": "Elle est connue comme la ville lumière."
                    }
                }
            ]
        }
        quiz_html = self.plugin.generate_quiz_html(quiz)
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Ensure the score div is present and initially hidden
        score_div = soup.find('div', class_='score')
        self.assertIsNotNone(score_div)
        self.assertIn('hidden', score_div['class'])

    def test_score_hidden_when_disabled(self):
        self.load_plugin_config(True, False, True)
        quiz = {
            "questions": [
                {
                    "type": "multiple-choice",
                    "question": {
                        "en": "What is 2 + 2?",
                        "fr": "Qu'est-ce que 2 + 2?"
                    },
                    "options": [
                        {
                            "text": {
                                "en": "3",
                                "fr": "3"
                            },
                            "correct": False,
                            "indice": {
                                "en": "This is incorrect.",
                                "fr": "Ceci est incorrect."
                            }
                        },
                        {
                            "text": {
                                "en": "4",
                                "fr": "4"
                            },
                            "correct": True,
                            "indice": {
                                "en": "This is correct.",
                                "fr": "Ceci est correct."
                            }
                        }
                    ]
                }
            ]
        }
        quiz_html = self.plugin.generate_quiz_html(quiz)
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Ensure the score div is not present
        score_div = soup.find('div', class_='score')
        self.assertIsNone(score_div)

    def test_progress_bar_enabled(self):
        self.load_plugin_config(True, True, True)
        quiz = {
            "questions": [
                {
                    "type": "multiple-choice",
                    "question": {
                        "en": "What is 2 + 2?",
                        "fr": "Qu'est-ce que 2 + 2?"
                    },
                    "options": [
                        {
                            "text": {
                                "en": "3",
                                "fr": "3"
                            },
                            "correct": False,
                            "indice": {
                                "en": "This is incorrect.",
                                "fr": "Ceci est incorrect."
                            }
                        },
                        {
                            "text": {
                                "en": "4",
                                "fr": "4"
                            },
                            "correct": True,
                            "indice": {
                                "en": "This is correct.",
                                "fr": "Ceci est correct."
                            }
                        }
                    ]
                }
            ]
        }
        quiz_html = self.plugin.generate_quiz_html(quiz)
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Ensure the progress bar is present
        progress_bar = soup.find('div', class_='progress-bar')
        self.assertIsNotNone(progress_bar)

    def test_progress_bar_disabled(self):
        self.load_plugin_config(True, True, False)
        quiz = {
            "questions": [
                {
                    "type": "multiple-choice",
                    "question": {
                        "en": "What is 2 + 2?",
                        "fr": "Qu'est-ce que 2 + 2?"
                    },
                    "options": [
                        {
                            "text": {
                                "en": "3",
                                "fr": "3"
                            },
                            "correct": False,
                            "indice": {
                                "en": "This is incorrect.",
                                "fr": "Ceci est incorrect."
                            }
                        },
                        {
                            "text": {
                                "en": "4",
                                "fr": "4"
                            },
                            "correct": True,
                            "indice": {
                                "en": "This is correct.",
                                "fr": "Ceci est correct."
                            }
                        }
                    ]
                }
            ]
        }
        quiz_html = self.plugin.generate_quiz_html(quiz)
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Ensure the progress bar is not present
        progress_bar = soup.find('div', class_='progress-bar')
        self.assertIsNone(progress_bar)

if __name__ == '__main__':
    unittest.main()
