import sympy as sp
import random
from sympy import symbols, solve, simplify, pretty
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor, split_symbols
import FreeSimpleGUI as sg

## The resources that we used to help with the code was:
## https://www.datacamp.com/tutorial/sympy
## https://realpython.com/pysimplegui-python/
## https://github.com/outerovitch-maths/Maths-Exercises-Generator/tree/master/math_exercise_generator
## https://www.sympy.org/en/index.html
## We used SymPy Documentation, which was important in figuring out how to work SymPy. It helped
## with figuring out solve(), simplify(), expand(), pretty() and Eq(). It
## also helped us figure out how to parse the user input for correct comparison.
## We used DataCamp SymPy Tutorial, which gave us a starting point for SymPy as well, and showed us how to 
## set up equations using symbols() and Eq(). We used Real python to learn and how to build the GUI. 
## It helped with layouts, windows and events. We used FreeSimpleGUI instead of PySimpleGUi since PySimpleGUI
## is no longer free, but FreeSimpleGUI has the same documentation.
## The open source project gave us inspiration for how to design our project as well as it helped us think through problem categories 
## As well as we used GitHub Copilot Chat extension in vs code for debugging. It helped with doing the range 1 to 10 and then fliping the sign 
## randomly so we would not get a zero for some of the coefficients. As well with the GUI it helped with some small mistakes,
## such as misspelling.

sg.theme('DarkBlue3')
FONT       = ("Courier New", 13)
FONT_BOLD  = ("Courier New", 13, "bold")
FONT_TITLE = ("Courier New", 24, "bold")
FONT_EQ    = ("Courier New", 15)

class AlgebraPractice:
    def __init__ (self):
        self.x, self.y = symbols('x y')

    def single_variable_problem(self):
        variable = random.choice([self.x, self.y])
        problem = random.choice(["linear","quadratic", "rational","combined","linear_quadratic", "proportion"])

        if problem == "linear":
            a = random.randint(1,10)
            if random.choice([True, False]):
                a =-a
            b = random.randint(-10,10)
            c = random.randint(-10,10)
            equation = sp.Eq(a*variable + b,c)
        
        elif problem == "quadratic":
            a= random.randint(1,5)
            b= random.randint(-10,10)
            c= random.randint(-10,10)
            equation = sp.Eq(a*variable**2 + b*variable + c, 0)

        elif problem == "rational":
            a= random.randint(1,10)
            b= random.randint(1,5)
            c= random.randint(1,10)
            equation = sp.Eq(a/variable + b, c)

        elif problem == "combined":
            a = random.randint(1,3)
            b = random.randint(-8,8)
            c = random.randint(-8,8)
            d = random.randint(-10,10)
            equation = sp.Eq(a*variable**2 + b*variable + d,0)

        elif problem == "linear_quadratic":
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
            equation = sp.Eq(a*variable + b, variable**2)
        
        else:
            a = random.randint(2,10)
            b = random.randint(2,10)
            c = random.randint(2,10)
            equation = sp.Eq(a/variable, sp.Rational(b,c))
        
        answer = solve(equation, variable)
        return equation, variable, answer, "single", problem
    

    def two_variable_problem(self):
        vars_list = [(self.x, self.y)]
        variable1, variable2 = vars_list[random.randint(0, len(vars_list)-1)]

        solving = variable2

        problem = random.choice(["linearTwo", "rationalTwo", "linearfraction"])

        if problem == "linearTwo":
            a = random.randint(1, 5)
            if random.choice([True, False]):
                a = -a
            b = random.randint(1, 5)
            c = random.randint(-10, 10)
            equation = sp.Eq(a*variable1 + b*variable2, c)

        elif problem == "rationalTwo":
            a = random.randint(1, 3)
            b = random.randint(-5, 5)
            c = random.randint(-10, 10)
            if b == 0:
                b += 1
            equation = sp.Eq(a*variable1**2 + b*variable1*variable2, c)

        else:
            a = random.randint(1,5)
            b = random.randint(1,5)
            c = random.randint(-10,10)
            equation = sp.Eq(a*variable1/variable2 + b, c)
        
        answer = solve(equation,solving)
        return equation, solving, answer, "two", problem
    

    def random_type_of_problem(self):
        problem = random.choice(["single", "two"])

        if problem == "single":
            return self.single_variable_problem()
        else:
            return self.two_variable_problem()
        

    def answer_checker(self, user_answer, correct, variable):
        try:
            transformations = standard_transformations + (implicit_multiplication_application, convert_xor, split_symbols)

            user_answers = []
            user_expressions = []
            local_dict = {"x": self.x, "y": self.y, "i": sp.I, str(variable): variable,}

            for a in user_answer.split(","):
                user_answers.append(a.strip())

            for answer in user_answers:
                if "=" in answer:
                    part = answer.split("=")
                    if len(part) == 2:
                        lhs = parse_expr(part[0].strip(),transformations=transformations,local_dict=local_dict)
                        rhs = parse_expr(part[1].strip(),transformations=transformations,local_dict=local_dict)

                        if lhs == variable:
                            user_expressions.append(rhs)
                        elif rhs == variable:
                            user_expressions.append(lhs)
                        else:
                            return False
                    else:
                        return False
                else: 
                    user_expressions.append(parse_expr(answer, transformations=transformations,local_dict=local_dict))
          
            for user_expr in user_expressions:
                for solution in correct:
                    try:
                        if simplify(user_expr - solution) == 0:
                            return True
                        if simplify(sp.expand(user_expr) - sp.expand(solution)) == 0:
                            return True 
                        if simplify(sp.cancel(user_expr - solution)) == 0:
                            return True
                    except:
                        continue 
            return False
        except Exception as e:
            print(f"Parsing problems")
            return False

    def display_problem(self, equation, variable, problem_type):
        if problem_type == "single":
            print(f"\nSolve for {variable}:")
        else:
            print(f"\nSolve for {variable} in terms of other variables:")
        pretty_str = pretty(equation, use_unicode=True)
        print(pretty_str)

    def solution_guide(self, equation, variable, solutions, problem, sub_problem):
        steps= []
        lhs = equation.lhs
        rhs = equation.rhs

        if problem == "single":
            if sub_problem == "linear":
                coefficient = lhs.coeff(variable)
                constant = lhs - coefficient * variable
        
                steps.append("Step 1: Move constant to the other side")
                if constant != 0:
                    new_rhs = rhs - constant
                    steps.append(f"{pretty(sp.Eq(coefficient*variable, new_rhs))}\n")
                else:
                    new_rhs = rhs
                    steps.append("No constant to move\n")
                
                steps.append("Step 2: Divide both sides by the coefficient")
                if coefficient != 1:
                    steps.append(f"{variable} = {simplify(new_rhs/coefficient)}\n")
                else:
                    steps.append(f"Coefficient is 1, already solved\n")


            elif sub_problem in ["quadratic", "combined", "linear_quadratic"]:
                expanded = (lhs - rhs).expand()
                a = expanded.coeff(variable, 2)
                b = expanded.coeff(variable, 1) if expanded.coeff(variable, 1) is not None else 0
                c = expanded.as_coeff_add(variable)[0]
            
                steps.append("Step 1: Write in standard form ax² + bx + c = 0")
                steps.append(pretty(sp.Eq(expanded, 0)))
                steps.append(f"a = {a}, b = {b}, c = {c}\n")
            
                steps.append("Step 2: Use the quadratic formula")
                steps.append(f"{variable} = (-b ± √(b² - 4ac)) / (2a)\n")
            
                discriminant = b**2 - 4*a*c
                steps.append("Step 3: Calculate the discriminant")
                steps.append(f"({b})² - 4({a})({c})= {discriminant}\n")
            
                if discriminant >= 0:
                    steps.append("Step 4: Plug values into the formula")
                    steps.append(f"{variable} = ({-b} ± √{discriminant}) / {2*a}")
                    sqrt_disc = sp.sqrt(discriminant)
                    steps.append(f"{variable} = ({-b} ± {sqrt_disc}) / {2*a}\n")
                
                    if len(solutions) == 2:
                        steps.append("Step 5: Calculate both solutions")
                        steps.append(f"{variable} = ({-b} + {sqrt_disc}) / {2*a} = {simplify(solutions[0])}")
                        steps.append(f"{variable} = ({-b} - {sqrt_disc}) / {2*a} = {simplify(solutions[1])}\n")
                    else:
                        steps.append("Step 5: Calculate the solution")
                        steps.append(f"{variable} = {simplify(solutions[0])}\n")
                else: 
                    steps.append("Discriminant is negative - no real solutions!\n")
        

            elif sub_problem == "rational":
                frac_term, constant = sp.Add.make_args(lhs)
                denom = frac_term.as_numer_denom()[1]

                steps.append("Step 1: Move the constant to the other side")
                new_rhs = sp.simplify(rhs - constant)
                steps.append(pretty(sp.Eq(frac_term, new_rhs)) + "\n")

                steps.append("Step 2: Multiply the denomator on both sides")
                new_lhs = sp.simplify(frac_term * denom)
                new_2rhs = sp.simplify(new_rhs * denom)
                steps.append(pretty(sp.Eq(new_lhs, new_2rhs)) +"\n")

                steps.append(f"Step 3: Divide both sides to solve for the {variable}")
                coefficient = sp.simplify(new_2rhs.coeff(variable))
                steps.append(pretty(sp.Eq(variable, sp.simplify(new_lhs / coefficient))) + "\n")

        
            elif sub_problem == "proportion":
                steps.append("Step 1: Cross multiply")
            
                cross_multiply = simplify(lhs * variable * rhs.as_numer_denom()[1])
                steps.append(pretty(sp.Eq(cross_multiply, rhs.as_numer_denom()[0] * variable))+"\n")
            
                steps.append("Step 2: Divide to isolate the variable")
                steps.append(f"{variable} = {simplify(solutions[0])}\n")
        
        else:
            if sub_problem == "linearTwo":
                if variable == self.x:
                    other_variable = self.y
                else:
                    other_variable = self.x
    
                coefficient_variable = lhs.coeff(variable)
                coefficient_other_variable = lhs.coeff(other_variable)

                steps.append(f"Step 1: Move coefficient {coefficient_other_variable} and variable {other_variable} to the other side")
                new_rhs = sp.simplify(rhs-coefficient_other_variable*other_variable)
                steps.append(pretty(sp.Eq(coefficient_variable*variable, new_rhs)) + "\n")

                steps.append(f"Step 2: Divide both sides by {coefficient_variable}")
                steps.append(pretty(sp.Eq(variable, sp.simplify(new_rhs/coefficient_variable))) + "\n")

            
            elif sub_problem == "rationalTwo":
                coefficient = lhs.coeff(variable)
                terms_without_v = sp.simplify(lhs-coefficient*variable)
                
                steps.append(f"Step 1: Move terms that don't contain {variable} to the other side")
                new_rhs = sp.simplify(rhs-terms_without_v)
                steps.append(pretty(sp.Eq(coefficient*variable, new_rhs)) + "\n")

                steps.append(f"Step 2: Divide both sides by {coefficient}")
                steps.append(pretty(sp.Eq(variable, sp.simplify(new_rhs/coefficient))) + "\n")


            elif sub_problem == "linearfraction":
                frac_coefficient = lhs.coeff(1/variable)
                constant = sp.simplify(lhs - frac_coefficient*(1/variable))
                
                steps.append("Step 1: Move the constant to the other side")
                new_rhs = sp.simplify(rhs - constant)
                steps.append(pretty(sp.Eq(frac_coefficient/variable, new_rhs)) + "\n")

                steps.append(f"Step 2: Multiply both sides by {variable}")
                steps.append(pretty(sp.Eq(frac_coefficient, sp.simplify(new_rhs * variable))) + "\n")

                steps.append(f"Step 3: Divide both sides by {new_rhs}")
                steps.append(pretty(sp.Eq(variable, sp.simplify(frac_coefficient / new_rhs))) + "\n")
                
        
        steps.append("------------------")
        steps.append("Final Answer:")

        if not solutions:
            steps.append("No real solutions")
        else:
            for sol in solutions:
                steps.append(pretty(sp.Eq(variable, sp.simplify(sol))))

        steps.append("------------------\n")
       
        return "\n".join(steps)

    def run(self):
        home_layout = [
            [sg.VPush()],
            [sg.Push(), sg.Text("Algebra Homework Practice", font=FONT_TITLE, text_color="SteelBlue1"), sg.Push()],
            [sg.Push(),
             sg.Button("▶ Play", key="play", font=FONT_BOLD, size=(14, 2), button_color=("white", "SteelBlue3")),
             sg.Button("✕ Quit", key="quit", font=FONT_BOLD, size=(14, 2), button_color=("white", "brown3")),
             sg.Push()],
            [sg.VPush()],
        ]

        home = sg.Window("Algebra Homework Practice", home_layout, size=(650, 320), finalize=True)

        while True:
            event, i = home.read()
            if event in (sg.WIN_CLOSED, "quit"):
                home.close()
                return
            if event == "play":
                home.close()
                break

        game_layout = [
            [sg.Push(), sg.Text("Algebra Homework Practice", font=FONT_TITLE, text_color="SteelBlue1"), sg.Push()],
            [sg.HorizontalSeparator()],

            [sg.Push(), sg.Text("", key="label", font=FONT, text_color="gray70"), sg.Push()],

            [sg.Push(),
             sg.Multiline("", key="eq", size=(60, 9), font=FONT_EQ, disabled=True,
                          background_color="gray15", text_color="white", no_scrollbar=True),
             sg.Push()],

            [sg.HorizontalSeparator()],

            [sg.Push(), sg.Text("", key="feedback", font=FONT_BOLD, text_color="green3", size=(50, 1)), sg.Push()],

            [sg.Push(),
             sg.Text("Your answer:", font=FONT),
             sg.Input("", key="answer", font=FONT_EQ, size=(25, 1),
                      background_color="gray15", text_color="white"),
             sg.Button("Submit", key="submit", font=FONT_BOLD, button_color=("white", "SteelBlue3"), bind_return_key=True),
             sg.Push()],

            [sg.Push(),
             sg.Button("See Solution", key="solution", font=FONT_BOLD, button_color=("white", "goldenrod3"), visible=False),
             sg.Button("Next", key="next", font=FONT_BOLD, button_color=("white", "green4"), visible=False),
             sg.Button("Quit", key="quit", font=FONT_BOLD, button_color=("white", "brown3"), visible=False),
             sg.Push()],
        ]

        game = sg.Window("Algebra Homework Practice", game_layout, size=(700, 430), finalize=True)

        def load_problem():
            while True:
                eq, var, sols, ptype, sub = self.random_type_of_problem()
                if sols:
                    break
            label = f"Solve for {var}:" if ptype == "single" else f"Solve for {var} in terms of other variables:"
            game["label"].update(label)
            game["eq"].update(pretty(eq, use_unicode=True))
            game["answer"].update("")
            game["feedback"].update("")
            game["solution"].update(visible=False)
            game["next"].update(visible=False)
            game["quit"].update(visible=False)
            game["submit"].update(visible=True)
            return eq, var, sols, ptype, sub

        eq, var, sols, ptype, sub = load_problem()

        while True:
            event, values = game.read()

            if event in (sg.WIN_CLOSED, "quit"):
                break

            elif event == "submit":
                answer = values["answer"].strip()
                if not answer:
                    continue
                if self.answer_checker(answer, sols, var):
                    game["feedback"].update("Correct! Loading next problem...", text_color="green3")
                    game.refresh()
                    import time; time.sleep(1.2)
                    eq, var, sols, ptype, sub = load_problem()
                else:
                    game["feedback"].update("Wrong answer! What would you like to do?", text_color="red3")
                    game["solution"].update(visible=True)
                    game["next"].update(visible=True)
                    game["quit"].update(visible=True)
                    game["submit"].update(visible=False)

            elif event == "next":
                eq, var, sols, ptype, sub = load_problem()

            elif event == "solution":
                steps = self.solution_guide(eq, var, sols, ptype, sub)
                game["label"].update("")
                game["eq"].update(steps)
                game["feedback"].update("")
                game["solution"].update(visible=False)
                game["submit"].update(visible=False)
               
        game.close()

if __name__ == "__main__":
    practice = AlgebraPractice()
    practice.run()
