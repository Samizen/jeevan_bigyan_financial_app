# screens/calculator_screen.py

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from decimal import Decimal, InvalidOperation

Builder.load_file('screens/calculator_screen.kv')

class CalculatorScreen(Screen):
    display_text = StringProperty('0')
    history_text = StringProperty('')  # New property for history
    calculation_string = ""
    nepali_to_english = {
        '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
        '५': '5', '६': '6', '७': '7', '८': '8', '९': '9',
        '+': '+', '-': '-', '*': '*', '/': '/', '.': '.', '%': '%'
    }
    english_to_nepali = {v: k for k, v in nepali_to_english.items()}

    def to_nepali(self, text):
        return ''.join([self.english_to_nepali.get(c, c) for c in text])

    def to_english(self, text):
        return ''.join([self.nepali_to_english.get(c, c) for c in text])

    def on_button_press(self, button_text):
        if button_text == 'C':
            self.calculation_string = ""
            self.display_text = '०'
            self.history_text = ''
            return
        
        if button_text == '⌫':
            self.calculation_string = self.calculation_string[:-1]
            if not self.calculation_string:
                self.display_text = '०'
            else:
                self.display_text = self.to_nepali(self.calculation_string)
            return

        if button_text in ['+', '-', '*', '/', '%']:
            if not self.calculation_string or self.calculation_string[-1] in ['+', '-', '*', '/']:
                # Prevent multiple operators or starting with an operator
                self.calculation_string = self.calculation_string[:-1] + self.to_english(button_text)
            else:
                self.calculation_string += self.to_english(button_text)
        elif button_text == '=':
            self.calculate()
            return
        elif button_text == '+/-':
            if self.calculation_string and self.calculation_string != "0":
                if self.calculation_string[0] == '-':
                    self.calculation_string = self.calculation_string[1:]
                else:
                    self.calculation_string = '-' + self.calculation_string
        else:
            if self.display_text == '०' and button_text != '.':
                self.calculation_string = self.to_english(button_text)
            else:
                self.calculation_string += self.to_english(button_text)

        self.display_text = self.to_nepali(self.calculation_string)

    def calculate(self):
        try:
            if not self.calculation_string:
                self.display_text = '०'
                return

            # Replace % with /100 for evaluation
            eval_string = self.calculation_string.replace('%', '/100')
            
            # Use Decimal for precision
            result = str(Decimal(eval(eval_string)))
            
            self.history_text = self.to_nepali(self.calculation_string + '=')
            self.display_text = self.to_nepali(result)
            self.calculation_string = result
        except (ZeroDivisionError, InvalidOperation, SyntaxError):
            self.display_text = "त्रुटि"  # Error
            self.history_text = ""
            self.calculation_string = ""