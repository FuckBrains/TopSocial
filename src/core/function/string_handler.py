import re


class StringHandler:
    def __init__(self):
        self.regular_expressions = "([\w\.-]+@[\w\.-]+)|(@[\w\.-]+)"

    regular_expressions = ""

    def remove_atsigns(self, text):
        if text is not None:
            text = re.sub(self.regular_expressions,
                          "",
                          text)
        return text

# if __name__ == '__main__':
#     xx = StringHandler()
#     print(xx.remove_atsigns("sdfsd fdf sdf sgd sdg sdfdsf@dfsfsef  sdgsdg sdg sdgs dg"))