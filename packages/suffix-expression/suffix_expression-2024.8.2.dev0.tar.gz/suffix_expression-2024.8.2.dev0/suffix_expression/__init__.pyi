__all__ = ['Expression','Suffix_expression','Se','E']
class Expression(object):
    def __init__(self,expression:str)->None:
        self.expression = expression
    def __str__(self)->str:...
class SuffixExpressionError(Exception):
    def __init__(self,m:str):
        self.m = m
    def __str__(self):...
class Suffix_expression(object):

    @staticmethod
    def generating(expression:str|bytes|Expression)->Expression:...
    @staticmethod
    def count(expression:str|bytes|Expression)->int:...
Se = Suffix_expression
E = Expression