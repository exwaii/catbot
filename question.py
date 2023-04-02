from PyPDF2 import PageObject
class Question:
    def __init__(self, paper: str, number: int, pages: list[PageObject], tags=set()) -> None:
        """Question Object

        Args:
            paper (str): name of paper the question is from
            number (int): question number
            pages (list[PageObject]): list of PageObjects that make up the question
            tags (set, optional): set of tags of the questions, should include q number at the end. Defaults to set().
        """
        self.paper = paper
        self.number = number
        self.tags = tags
        self.pages = pages
            
    def __repr__(self) -> str:
        return f"{self.paper} - {self.number} - {self.tags}"

    def __str__(self) -> str:
        return f"{self.paper} - {self.number} - {self.tags}"

def main():
    pass



if __name__ == "__main__":
    main()