import re
import uuid
import json
from mkdocs.plugins import BasePlugin
import os
import warnings
from mkdocs.config import config_options
from mkdocs.structure.files import File

warnings.filterwarnings("ignore")

class QuizPlugin(BasePlugin):

    config_scheme = (
        ('quiz_file', config_options.Type(str, default='quizzes.json')),
        ('language', config_options.Type(str, default='en')),
        ('show_refresh_button', config_options.Type(bool, default=True)),
        ('show_indice_on_answer', config_options.Type(bool, default=True)),
        ('show_score', config_options.Type(bool, default=True)),
        ('show_progress_bar', config_options.Type(bool, default=True)),  # New option for progress bar
    )

    def on_config(self, config):
        quiz_file_path = self.config.get('quiz_file')
        self.language = self.config.get('language', 'en')
        self.show_refresh_button = self.config.get('show_refresh_button', True)
        self.show_indice_on_answer = self.config.get('show_indice_on_answer', True)
        self.show_score = self.config.get('show_score', True)
        self.show_progress_bar = self.config.get('show_progress_bar', True)  # New option for progress bar
        if quiz_file_path and os.path.isfile(quiz_file_path):
            try:
                with open(quiz_file_path, 'r') as file:
                    self.quiz_data = json.load(file)
                print("JSON is valid")
            except json.JSONDecodeError as e:
                print(f"JSON is invalid: {e}")
                self.quiz_data = {'quizzes': {}}
        else:
            self.quiz_data = {'quizzes': {}}
        return config
    
    def on_files(self, files, config):
        # Add the JavaScript and CSS files to the site
        plugin_dir = os.path.dirname(__file__)
        js_file = File(os.path.join(plugin_dir, 'static', 'quiz.js'), config['docs_dir'], config['site_dir'], False)
        css_file = File(os.path.join(plugin_dir, 'static', 'quiz.css'), config['docs_dir'], config['site_dir'], False)
        files.append(js_file)
        files.append(css_file)
        return files

    def on_page_markdown(self, markdown, page, config, files):
        quiz_placeholder_pattern = re.compile(r'<!-- QUIZ_ID: (\w+) -->')
        matches = quiz_placeholder_pattern.findall(markdown)

        for quiz_id in matches:
            if quiz_id in self.quiz_data['quizzes']:
                quiz_html = self.generate_quiz_html(self.quiz_data['quizzes'][quiz_id])
                placeholder = f"<!-- QUIZ_PLACEHOLDER_{quiz_id} -->"
                markdown = markdown.replace(f'<!-- QUIZ_ID: {quiz_id} -->', placeholder)
                page.meta['quiz_placeholder'] = page.meta.get('quiz_placeholder', []) + [(placeholder, quiz_html)]
        
        return markdown
    
    def on_post_page(self, output_content, page, config):
        if 'quiz_placeholder' in page.meta:
            for placeholder, quiz_html in page.meta['quiz_placeholder']:
                output_content = output_content.replace(placeholder, quiz_html)
        # Inject the JavaScript and CSS into the page
        script_tag = '<script src="static/quiz.js"></script>'
        link_tag = '<link rel="stylesheet" href="static/quiz.css">'
        output_content = output_content.replace('</body>', f'{script_tag}</body>')
        output_content = output_content.replace('</head>', f'{link_tag}</head>')
        return output_content

    def generate_quiz_html(self, quiz):
        quiz_id = uuid.uuid4().hex
        questions = quiz.get('questions', [])
        show_refresh_button = 'true' if self.show_refresh_button else 'false'
        show_indice_on_answer = 'true' if self.show_indice_on_answer else 'false'
        show_score = 'true' if self.show_score else 'false'
        show_progress_bar = 'true' if self.show_progress_bar else 'false'
        quiz_html = f"<div class='quiz' id='quiz-{quiz_id}' data-show-refresh-button='{show_refresh_button}' data-show-indice-on-answer='{show_indice_on_answer}' data-show-score='{show_score}' data-show-progress-bar='{show_progress_bar}' data-score='0'>"

        # Add progress bar if enabled
        if self.show_progress_bar:
            quiz_html += """
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: 0%;"></div>
            </div>
            """

        for question in questions:
            question_id = uuid.uuid4().hex
            question_text = question['question'].get(self.language, question['question']['en'])
            quiz_type = question.get('type', 'multiple-choice')

            if quiz_type in ['multiple-choice', 'true-false']:
                options = question.get('options', [])
                quiz_html += f"""
                <div class='question p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='question-{question_id}' data-quiz-id='{quiz_id}' data-question-id='{question_id}' data-quiz-type='{quiz_type}'>
                    <p class='font-bold text-lg mb-4'>{question_text}"""
                if self.show_indice_on_answer:
                    quiz_html += f""" <button class='hint-button' data-indice='{options[0].get("indice", {}).get(self.language, options[0].get("indice", {}).get("en", ""))}'><i class='fa fa-lightbulb-o'></i></button>"""
                quiz_html += f"""</p><ul class='list-none p-0'>
                """
                for i, option in enumerate(options):
                    text = option['text'].get(self.language, option['text']['en'])
                    indice = option.get('indice', {}).get(self.language, option.get('indice', {}).get('en', ''))
                    correct = 'correct' if option['correct'] else 'incorrect'
                    quiz_html += f"""
                        <li class='{correct} p-2 mb-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-100' data-quiz-id='{quiz_id}' data-question-id='{question_id}' data-option-id='{i}' data-indice='{indice}'>
                            {text}
                        </li>
                    """
                quiz_html += f"""
                    </ul>
                """
                if self.show_indice_on_answer:
                    quiz_html += f"""
                    <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{question_id}'></div>
                    """
                quiz_html += f"""
                    <div class='feedback mt-4 p-3 rounded-lg hidden' id='feedback-{question_id}'></div>
                </div>
                """
            elif quiz_type == 'fill-in-the-blank':
                answer = question['answer'].get(self.language, question['answer']['en'])
                indice = question.get('indice', {}).get(self.language, question.get('indice', {}).get('en', ''))
                quiz_html += f"""
                <div class='question p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='question-{question_id}' data-quiz-id='{quiz_id}' data-question-id='{question_id}' data-quiz-type='{quiz_type}' data-answer='{answer}'>
                    <p class='font-bold text-lg mb-4'>{question_text}"""
                if self.show_indice_on_answer:
                    quiz_html += f""" <button class='hint-button' data-indice='{indice}'><i class='fa fa-lightbulb-o'></i></button>"""
                quiz_html += f"""</p>
                    <input type='text' class='p-2 mb-2 border border-gray-200 rounded-lg' id='answer-{question_id}'>
                    <button class='submit-answer bg-blue-500 text-white p-2 rounded-lg' data-quiz-id='{quiz_id}' data-question-id='{question_id}'>Submit</button>
                """
                if self.show_indice_on_answer:
                    quiz_html += f"""
                    <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{question_id}'>{indice}</div>
                    """
                quiz_html += f"""
                    <div class='feedback mt-4 p-3 rounded-lg hidden' id='feedback-{question_id}'></div>
                </div>
                """
            elif quiz_type == 'multi-choice':
                options = question.get('options', [])
                quiz_html += f"""
                <div class='question p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='question-{question_id}' data-quiz-id='{quiz_id}' data-question-id='{question_id}' data-quiz-type='{quiz_type}'>
                    <p class='font-bold text-lg mb-4'>{question_text}"""
                if self.show_indice_on_answer:
                    quiz_html += f""" <button class='hint-button' data-indice='{options[0].get("indice", {}).get(self.language, options[0].get("indice", {}).get("en", ""))}'><i class='fa fa-lightbulb-o'></i></button>"""
                quiz_html += f"""</p><ul class='list-none p-0'>
                """
                for i, option in enumerate(options):
                    text = option['text'].get(self.language, option['text']['en'])
                    indice = option.get('indice', {}).get(self.language, option.get('indice', {}).get('en', ''))
                    correct = 'correct' if option['correct'] else 'incorrect'
                    quiz_html += f"""
                        <li class='{correct} p-2 mb-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-100' data-quiz-id='{quiz_id}' data-question-id='{question_id}' data-option-id='{i}' data-indice='{indice}'>
                            <input type="checkbox" class="multi-choice-checkbox" data-option-id="{i}"> <span>{text}</span>
                        </li>
                    """
                quiz_html += f"""
                    </ul>
                """
                if self.show_indice_on_answer:
                    quiz_html += f"""
                    <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{question_id}'></div>
                    """
                quiz_html += f"""
                    <div class='feedback mt-4 p-3 rounded-lg hidden' id='feedback-{question_id}'></div>
                    <button class='submit-multi-choice bg-blue-500 text-white p-2 rounded-lg' data-quiz-id='{quiz_id}' data-question-id='{question_id}'>Submit</button>
                </div>
                """

        if self.show_refresh_button:
            quiz_html += f"""
                <button class='refresh-quiz bg-blue-500 text-white p-2 rounded-lg mt-4'>Refresh</button>
            """
        
        if self.show_score:
            quiz_html += "<div class='score mt-4 text-lg font-bold hidden'>Score: 0</div>"
        
        quiz_html += "</div>"
        return quiz_html
