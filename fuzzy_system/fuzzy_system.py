from typing import Any
from fuzzy_system.fuzzy_variable import FuzzyVariable
from .fuzzy_rule import FuzzyRule
from .fuzzy_variable_output import FuzzyVariableOutput
from .fuzzy_variable_input import FuzzyVariableInput
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np


class FuzzySystem:
    """
    A type-1 fuzzy system based on Mamdani inference system
    Reference:
    ----------
    Mamdani, Ebrahim H., and Sedrak Assilian.
    "An experiment in linguistic synthesis with a fuzzy logic controller."
    Readings in Fuzzy Sets for Intelligent Systems. Morgan Kaufmann, 1993. 283-289.
    """
    def __init__(self) -> None:
        """
        Initializes fuzzy system.
        data structures required:
            input variables -- dict, having format {variable_name: FuzzyVariable, ...}
            output variables -- dict, having format {variable_name: FuzzyVariable, ...}
            rules -- list of FuzzyRule
            output_distribution -- dict holding fuzzy output for each variable having format
                                {variable_name: FuzzySet, ...}
        """
        self.input_variables = {}
        self.output_variables = {}
        self.rules = []

    def __str__(self) -> str:
        """
        string representation of the system.
        Returns:
        --------
        str: str, string representation of the system in the form
                Input:
                input_variable_name(set_names)...
                Output:
                output_variable_name(set_names)...
                Rules:
                IF [antecedent clauses] THEN [consequent clauses]
        """
        ret_str = 'Input: \n'
        for n, s in self.input_variables.items():
            ret_str = ret_str + f'{n}: ({s})\n'
        ret_str = ret_str + 'Output: \n'
        for n, s in self.output_variables.items():
            ret_str = ret_str + f'{n}: ({s})\n'
        ret_str = ret_str + 'Rules: \n'
        for rule in self.rules:
            ret_str = ret_str + f'{rule}\n'
        return ret_str

    def add_input_variable(self, variable:FuzzyVariableInput) -> None:
        """
        TODO:
         Add an input variable to the system
        :param variable: the input fuzzy variable
        """
        # Write the code below
        print(variable.name)
        self.input_variables.update({variable.name:variable})
        print(self.input_variables)
        pass

    def add_output_variable(self, variable:FuzzyVariableInput) -> None:
        """
        TODO:
         Add an output variable to the system
        :param variable: the output fuzzy variable
        """
        # Write the code below
        self.output_variables.update({variable.name:variable})
        #print(self.output_variables)
        pass

    def get_input_variable(self, name: str) -> Any:
        """
        TODO:
         Get an input variable given the name
        :param name: name of variable
        """
        # Write your code below
        return self.input_variables[name]
        

    def get_output_variable(self, name: str) -> Any:
        """
        TODO:
         Get an output variable given the name
        :param name: name of variable
        """
        # Write your code below
        return self.output_variables[name]


    def clear_output_distributions(self) -> None:
        """
        Used for each iteration. The fuzzy result is cleared
        """
        map(lambda output_var: output_var.clear_output_distribution(), self.output_variables.values())

    def add_rule(self, antecedent_clauses: dict, consequent_clauses: dict) -> None:
        """
        TODO:
         Adds a new rule to the system.
        :param antecedent_clauses: a dict of clause, having the form {variable_name: set_name, ...}
        :param consequent_clauses: having the form {variable_name: set_name, ...}
        """

        # create a new rule
        new_rule = FuzzyRule()
        # Write your code below
        # add antecedent clauses
       
        for var_name, set_name in antecedent_clauses.items():
            # write your code here
            # get the input variable and corresponding fuzzy set for the antecedent clause
            # and then add the clause to `new_rule`
            varb=self.get_input_variable(var_name)
            #print(type(varb))
        
            fuzzset=varb.get_set(set_name)
            #print(type(fuzzset))
            #print(var_name," ",set_name)

            new_rule.add_antecedent_clause(varb,fuzzset)
           
            


            # add consequent clauses
         
        
        for var_name, set_name in consequent_clauses.items():
                # write your code here
                # get the output variable and corresponding fuzzy set for the consequent clause
                # and then add the clause to `new_rule`
                outvarb=self.get_output_variable(var_name)
                #print(type(outvarb))

                outfuzzset=outvarb.get_set(set_name)
                #print(type(outfuzzset))

                new_rule.add_consequent_clause(outvarb,outfuzzset)
       
        #print(new_rule)

        self.rules.append(new_rule)

                

        # add the new rule
        pass

    def evaluate_output(self, input_values: Any) -> Any:
        """
        Executes the fuzzy inference system for a set of inputs
        :param input_values: a dict containing the inputs to the systems in the form {input_variable_name: value, ...}
        :return: a dict, containing the outputs from the systems in the form {output_variable_name: value, ...}
        """
        # clear the fuzzy consequences as we are evaluating a new set of inputs.
        # can be optimized by comparing if the inputs have changes from the previous
        # iteration.
        self.clear_output_distributions()
        # Fuzzify the inputs. The degree of membership will be stored in each set
        for input_name, input_value in input_values.items():
            #print("1.:",input_name)
            self.input_variables[input_name].fuzzify(input_value)
        # evaluate rules
        #print(self.rules)
        for rule in self.rules:
            #print(rule)
            rule.evaluate()
        # finally, defuzzify all output distributions to get the crisp outputs
        output = {}
        for output_var_name, output_var in self.output_variables.items():
            output[output_var_name] = output_var.get_crisp_output()
        return output

    def evaluate_output_info(self, input_values: Any) -> Any:
        """
        Executes the fuzzy inference system for a set of inputs
        :param input_values: a dict containing the inputs to the systems in the form {input_variable_name: value, ...}
        :return: a dict containing the outputs from the systems in the form {output_variable_name: value, ...}
        """
        info = {}
        # clear the fuzzy consequences as we are evaluating a new set of inputs.
        # can be optimized by comparing if the inputs have changes from the previous
        # iteration.
        self.clear_output_distributions()
        # Fuzzify the inputs. The degree of membership will be stored in
        # each set
        fuzzification_info = []
        for input_name, input_value in input_values.items():
            fuzzification_info.append(self.input_variables[input_name].fuzzify_info(input_value))
        info['fuzzification'] = '\n'.join(fuzzification_info)
        # evaluate rules
        rule_info = []
        for rule in self._rules:
            rule_info.append(rule.evaluate_info())
        info['rules'] = '\n'.join(rule_info)
        # finally, defuzzify all output distributions to get the crisp outputs
        output = {}
        for output_var_name, output_var in self.output_variables.items():
            output[output_var_name], info = output_var.get_crisp_output_info()
        return output, info

    def plot_system(self):
        total_var_count = len(self.input_variables) + len(self.output_variables)
        if total_var_count < 2:
            total_var_count = 2
        fig, axs = plt.subplots(total_var_count, 1)
        fig.tight_layout(pad=1.0)
        for idx, var_name in enumerate(self.input_variables):
            self.input_variables[var_name].plot_variable(ax=axs[idx], show=False)
        for idx, var_name in enumerate(self.output_variables):
            self.output_variables[var_name].plot_variable(ax=axs[len(self.input_variables) + idx], show=False)
        plt.show()
