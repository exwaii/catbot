from question import Question

import json
import re
from time import sleep
from PyPDF2 import PageObject

import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def classify(page: PageObject, number: int, ext1=True) -> list[str]:
    content = page.extract_text()
    if ext1:
        with open("prompts/ext1.json", "r") as f:
            messages = json.load(f)
        messages.append(
            {
                "role": "user",
                "content": f"For question {number} in: \n\n" + content + "\n\nChoose one or more of the following categories for this question: Vectors, Polynomial, Proj Motion, Expo Growth & Decay, Rates of change, Trig, Differentiation, Integration, Probability, Graphing, Inequalities. Each part of the question should only fall under one of these categories. Subtopics from each part of the questions should not be counted. Answer with only a comma separated list."
            }
        )
    else:
        with open("prompts/ext2.json", "r") as f:
            messages = json.load(f)
        messages.append(
            {
                "role": "user",
                "content": f"For question {number} in: \n\n" + content +
                "\n\nChoose one or more of the following categories for this question: Vectors, Complex Numbers, Proofs, Integration, Mechanics, Inequalities. Each part of the question should only fall under one of these categories. Subtopics from each part of the questions should not be counted. Answer with only a comma separated list."
            }
        )
    try:
        r = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )["choices"][0]["message"]["content"]
    except openai.error.RateLimitError:
        sleep(1)
        r = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )["choices"][0]["message"]["content"]
    return set(r.split(", "))


def questionify(file_name, pages, ext1=True) -> list[Question]:
    questions = []
    next = False
    for i, page in enumerate(pages):
        q_number = number(page)
        if not q_number:
            if next:
                questions[-1].pages.append(page)
                questions[-1].tags.update(classify(page, q_number, ext1))
                next = False
                continue
            else:
                break
        else:
            if (len(questions) > 0 and questions[-1].number == q_number):
                questions[-1].pages.append(page)
                questions[-1].tags.update(classify(page, q_number, ext1))
            else:
                questions.append(
                    Question(
                        paper=file_name,
                        number=q_number,
                        pages=[page],
                        tags=classify(page, q_number, ext1),
                    )
                )
        next = re.search(r"question\W*?(\d(.|\s)?\d|eleven|twelve|thirteen|forteen|fourteen|fifteen)\W*?continues",
                         page.extract_text(), re.IGNORECASE)
        # next = re.search(r"continues", page.extract_text(), re.IGNORECASE)
        # this regex search can replace the one below for certain exams (for example, some exams only have "this exam continues on the next page" and do not have the question number on continued page, etc)
        # check bad examples/2021 Normanhurst Boys High School - X2 - Trial.pdf and bad examples/2022 Sydney Technical High School - X1 - Trial - Questions.pdf
        if next:
            continue  # saves time
        if re.search(r"end\W*?of(.|\s)*?(paper|exam|test|task)", page.extract_text(), re.IGNORECASE):
            break

    for question in questions:
        question.tags.add(f'Q{question.number}')
        # discord only allows max 5 tags per thread, and chatgpt likes to tag trig a lot...
        if "Trig" in question.tags and len(question.tags) > 5:
            question.tags.remove("Trig")
    return questions


NUMBERS = {
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "forteen": 14,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
}


def number(page: PageObject) -> int:
    number = re.search(r'question\W*?(\d\W?\d|eleven|twelve|thirteen|forteen|fourteen|fifteen|sixteen)',
                       page.extract_text(), flags=re.IGNORECASE)
    if not number:
        return

    number = int(NUMBERS[number[1].lower()] if number[1].lower()
                 in NUMBERS else re.sub(r"\D", "", number[1]))
    return number


def main():
    from PyPDF2 import PdfReader
    from pages import page_start
    path = "examples/2022 North Sydney Boys High School - X1 - Trial.pdf"
    pages = PdfReader(path).pages
    start = page_start(pages)
    questions = questionify(path, pages[start:], ext1=False)
    for question in questions:
        print(question)


if __name__ == "__main__":
    main()
