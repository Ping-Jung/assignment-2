from typing import Any
from numpy.typing import NDArray
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


class FuzzySet:
    precision: int = 3

    def __init__(self, name: str, domain_min: float, domain_max: float, res: float) -> None:
        """
        Initialize the fuzzy set
        :param name: name of the set
        :param domain_min: the minimum of the set
        :param domain_max: the maximum of the set
        :param res: the number of steps between the minimum and maximum value
        """
        self.domain_min = domain_min
        self.domain_max = domain_max
        self.res = res
        # initialize the domain values
        self.domain = np.linspace(domain_min, domain_max, res)
        # initialize the degree-of-membership values
        self.dom = np.zeros(self.domain.shape)

        self.name = name
        self._last_dom_value = 0

    def __getitem__(self, x_val):
        return self.dom[np.abs(self.domain - x_val).argmin()]

    def __setitem__(self, x_val, dom):
        self.dom[np.abs(self.domain - x_val).argmin()] = round(dom, self.precision)

    def __str__(self) -> str:
        """
        :return: string of pair degree-of-membership and corresponding domain value
        """
        return ' + '.join([str(a) + '/' + str(b) for a, b in zip(self.dom, self.domain)])

    def __get_last_dom_value(self):
        return self._last_dom_value

    def __set_last_dom_value(self, d):
        self._last_dom_value = d

    last_dom_value = property(__get_last_dom_value, __set_last_dom_value)

    @property
    def empty(self) -> bool:
        return np.all(self.dom == 0)

    @classmethod
    def create_trapezoidal(cls,
                           name: str,
                           domain_min: float,
                           domain_max: float,
                           res: float,
                           a: float,
                           b: float,
                           c: float,
                           d: float) -> Any:
        """
        TODO:
         Implement trapezoidal membership function, following the formula
        :param name: name of the trapezoidal function
        :param domain_min: the minimum value of the trapezoidal function
        :param domain_max: the maximum value of the trapezoidal function
        :param res: the number of steps between the minimum and maximum value
        :param a: the special input
        :param b: the special input
        :param c: the special input
        :param d: the special input
        :return: trapezoidal membership function
        """
        # initialize the result
        t1fs = cls(name, domain_min, domain_max, res)
        # retrieve the degree-of-membership of the inputs
        a = t1fs.adjust_domain_val(a)
        b = t1fs.adjust_domain_val(b)
        c = t1fs.adjust_domain_val(c)
        d = t1fs.adjust_domain_val(d)
        #
        #t1fs.dom = None
        # Write your code below
    
        for i in range(len(t1fs.domain)):
            nox=t1fs.domain[i]
            if nox<a or nox>d:
                t1fs.dom[i]=0
            elif nox>=a and nox<=b:
                t1fs.dom[i]=(nox-a)/(b-a)
            elif nox>=c and nox<=d:
                t1fs.dom[i]=(d-nox)/(d-c) 
            else:
                t1fs.dom[i]=1           
              
        return t1fs

    @classmethod
    def create_triangular(cls,
                          name: str,
                          domain_min: float,
                          domain_max: float,
                          res: float,
                          a: float,
                          m: float,
                          b: float) -> Any:
        """
        TODO:
         Implement triangle membership function, following the formula
        :param name: name of the trapezoidal function
        :param domain_min: the minimum value of the trapezoidal function
        :param domain_max: the maximum value of the trapezoidal function
        :param res: the number of steps between the minimum and maximum value
        :param a: the special input
        :param m: the special input
        :param b: the special input
        :return: the triangle membership function
        """
        # initialize the result
        t1fs = cls(name, domain_min, domain_max, res)
        # retrieve the degree-of-membership of the inputs
        a = t1fs.adjust_domain_val(a)
        m = t1fs.adjust_domain_val(m)
        b = t1fs.adjust_domain_val(b)
        #
        #t1fs.dom = None
        # write your code below

        for i in range(len(t1fs.domain)):
            nox=t1fs.domain[i]
            if  nox<a:
                t1fs.dom[i]=0
            elif nox>=a and nox<=m:
                t1fs.dom[i]=(nox-a)/(m-a)
            elif nox>m and nox<b:
                t1fs.dom[i]=(b-nox)/(b-m)
            else:
                t1fs.dom[i]=0            

        return t1fs

    def adjust_domain_val(self, x: float) -> NDArray:
        """
        Retrieve degree-of-membership value in the domain array from the input
        :param x: the input
        :return: degree-of-membership value
        """
        return self.domain[np.abs(self.domain - x).argmin()]

    def clear_set(self) -> None:
        """
        Clear the set (membership function)
        """
        self.dom.fill(0)

    def min_scalar(self, x: float) -> Any:
        """
        Minimum operator between the fuzzy set and the scalar
        :param x: the scalar
        :return: the scalar minimum of current fuzzy set and x
        """
        # initialize the result
        result = FuzzySet(f'({self.name}) min ({x})', self.domain_min, self.domain_max, self.res)
        result.dom = np.minimum(self.dom, x)
        return result

    def union(self, f_set: Any) -> Any:
        """
        TODO:
         Implement the Union operator of fuzzy set.
         It is calculated by maximizing values of the current fuzzy set (self) and f_set.
        :param f_set: the other fuzzy set to unite with
        :return: the union of current fuzzy set and f_set
        """
        # initialize result
        result = FuzzySet(name=f'({self.name}) union ({f_set.name})',
                          domain_min=self.domain_min,
                          domain_max=self.domain_max,
                          res=self.res)
        result.dom = None
        # Write your code below
        result.dom=np.zeros(self.domain.shape)
        for i in range(len(self.domain)):
            result.dom[i]=max(self.dom[i],f_set.dom[i])


        return result

    def intersection(self, f_set: Any) -> Any:
        """
        TODO:
         Implement the Intersection operator of fuzzy set.
         It is calculated by minimizing values of the current fuzzy set (self) and f_set.
        :param f_set: the other fuzzy set to intersect with
        :return: the intersection of current fuzzy set and f_set
        """
        # initialize result
        result = FuzzySet(name=f'({self.name}) intersection ({f_set.name})',
                          domain_min=self.domain_min,
                          domain_max=self.domain_max,
                          res=self.res)
        result.dom = None
        # Write your code below

        result.dom=np.zeros(self.domain.shape)
        for i in range(len(self.domain)-1):
            result.dom[i]=min(self.dom[i],f_set.dom[i])
            
        return result

    def complement(self) -> Any:
        """
        TODO:
         Implement the Completion operator of fuzzy set.
         It is calculated by subtract the degree of membership value from 1.
        :return: the complement of current fuzzy set (self)
        """
        # initialize result
        result = FuzzySet(name=f'not ({self.name})',
                          domain_min=self.domain_min,
                          domain_max=self.domain_max,
                          res=self.res)
        result.dom = None
        # Write your code below
        result.dom=np.zeros(self.domain.shape)
        for i in range(len(self.domain)-1):
            result.dom[i]=1-self.dom[i]

        return result

    def defuzzify_cog(self) -> Any:
        """
        TODO:
         Implement the defuzzification using center-of-area or center-of-gravity
        :return: crisp quantities
        """
        result = None
        # write your code below
        area_sum=0
        areatimesx_sum=0
        

        #cog method
        for i in  range(len(self.domain)):
            #print(self.dom[i]," ",self.domain[i])
            print(i)
            area_sum=area_sum+self.dom[i]
            areatimesx_sum=areatimesx_sum+self.domain[i]*self.dom[i]
         
        result=areatimesx_sum/area_sum
        
        '''
        # try a  new way of defuzzification (Max-Membership Principle)
        biggest_x=0
        biggest_value=0
       
        for i in range(len(self.domain)):
             print(self.domain[i]," ",self.dom[i])
             if self.dom[i]>biggest_value:
                 biggest_value=self.dom[i]
                 biggest_x=self.domain[i]

        result=biggest_x
        

        

        # try a new way of defuzzification (Max-Membership Principle)
        biggest_x1=0
        biggest_x2=0
        biggest_value=0

        for i in range(len(self.domain)):
             print(self.domain[i]," ",self.dom[i])
             if self.dom[i]>biggest_value:
                 biggest_value=self.dom[i]
                 biggest_x1=self.domain[i]
             if self.dom[i-1]==biggest_value and self.dom[i]<biggest_value:
                 biggest_x2=self.domain[i]


        result=0.5*(biggest_x1+biggest_x2)
        plt.scatter(self.domain,self.dom)
        plt.xticks(np.arange(min(self.domain), max(self.domain)+1, 5))
        plt.xlabel('output.domain')
        plt.ylabel('output.dom')
        plt.show()

        '''
        return result
 

    def get_domain_elements(self) -> NDArray:
        """
        :return: array of domain values
        """
        return self.domain

    def get_dom_elements(self) -> NDArray:
        """
        :return: array of degree-of-membership values
        """
        return self.dom

    def plot_set(self, ax: Any, col: str = '') -> None:
        """
        Visualize the fuzzy set
        """
        ax.plot(self.domain, self.dom, col)
        ax.set_ylim([-0.1, 1.1])
        ax.set_title(self.name)
        ax.grid(True, which='both', alpha=0.4)
        ax.set(xlabel='x', ylabel='$\mu(x)$')
