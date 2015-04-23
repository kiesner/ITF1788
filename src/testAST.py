#
#                              ITF1788
#
#   Interval Test Framework for IEEE 1788 Standard for Interval Arithmetic
#
#
#   Copyright 2014
#
#   Marco Nehmeier (nehmeier@informatik.uni-wuerzburg.de)
#   Maximilian Kiesner (maximilian.kiesner@stud-mail.uni-wuerzburg.de)
#
#   Department of Computer Science
#   University of Wuerzburg, Germany
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""This module contains classes to model an AST."""

from string import Template
import importlib
import re

class Node(object):

    """
    Base class of all other nodes.

    Contains an accept method to provide the Visitor pattern functionality.
    See Erich Gamma et al. -- Design Patterns - Elements of Reusable
    Object-Oriented Software.

    A variation of the original design pattern was required because Python does
    not distinguish method parameters by type. Thus an overloaded visit-Method
    is not possible. Instead, e.g. for a Node of type 'LineCommentNode', we
    call the visitors 'visitLineCommentNode' method.
    """

    def accept(self, visitor):
        """
        The accept method for the visitor functionality.

        Arguments:
        visitor -- a visitor object
        """

        #
        # assemble function as 'visitCLASSNAME' where CLASSNAME represents
        # the name of the concrete class of the node, i.e. a subclass of Node
        #
        visitFnc = getattr(visitor, 'visit' + self.__class__.__name__)
        return visitFnc(self)

    def getType(self):
        """
        Return the type name of the node, default is the class's name.
        """
        return self.__class__.__name__


class LineCommentNode(Node):

    """A Node which represents a line comment in the AST."""

    def __init__(self, val):
        """
        Initialize a LineCommentNode with the parsed value of the comment.
        """
        self.val = val


class BlockCommentNode(Node):

    """A Node which represents a block comment in the AST."""

    def __init__(self, val):
        """
        Initialize a BlockCommentNode with the parsed value of the comment.
        """
        self.val = val


class IdentifierNode(Node):

    """A Node which represents an identifier in the AST."""

    def __init__(self, val):
        """
        Initialize an IdentifierNode with the parsed value of the comment.
        """
        self.val = val

class NaNNode(Node):
    '''A Node which represents the NaN value'''
    def __init__(self):
        pass

    def setType(self, t):
        """
        Set the datatype of the node.

        Arguments:
        t -- the type of the node as a string.
        """
        self.dataType = t

    def getType(self):
        """
        Return the type of the node, if it was previously set,
        or None otherwise.
        """
        return self.dataType


class OverlapLiteralNode(Node):

    """A Node which represents an overlap relation in the AST."""

    def __init__(self, val):
        """
        Initialize an OverlapLiteralNode with the value of the overlap.
        """
        self.val = val


class BooleanLiteralNode(Node):

    """A Node which represents a boolean value in the AST."""

    def __init__(self, val):
        """
        Initialize a BooleanLiteralNode with the parsed value of the boolean.
        """
        self.val = val


class StringLiteralNode(Node):

    """A Node which represents a string in the AST."""

    def __init__(self, val):
        """
        Initialize a StringLiteralNode with the parsed value of the string.
        """
        self.val = val

    def getType(self):
        """
        Return 'string' as type of the Node.
        """
        return 'string'


class IntegerLiteralNode(Node):

    """A Node which represents an integer in the AST."""

    def __init__(self, val):
        """
        Initialize an IntegerLiteralNode with the parsed value of the integer.
        """
        self.val = val

    def setType(self, t):
        """
        Set the data type of the node.

        Arguments:
        t -- type of the Node as a string
        """
        self.dataType = t

    def setUnsigned(self, b):
        """
        Declare the node as unsigned or not.

        Arguments:
        b -- boolean value
        """
        self.unsigned = b

    def getType(self):
        """
        Return the type of the node, if it was previously set,
        or None otherwise.
        """
        return self.dataType


class FloatingPointNode(Node):

    """A Node which represents a floating point number in the AST."""

    def __init__(self, val):
        """
        Initialize a FloatingPointNumberLiteral with the parsed value of the
        floating point number.
        """
        self.val = val

    def setType(self, t):
        """
        Set the data type of the node.

        Arguments:
        t -- type of the node as a string.
        """
        self.dataType = t

    def setUnsigned(self, b):
        """
        Declare the node as unsigned or not.

        Arguments:
        b -- boolean value
        """
        self.unsigned = b

    def getType(self):
        """
        Return the type of the node, if it was previously set,
        or None otherwise.
        """
        return self.dataType


class InfinityLiteralNode(Node):

    """A Node which represents positive and negative infinity in the AST."""

    def __init__(self, sign):
        """Initialize an InfinityLiteralNode by sign."""
        self.sign = sign

    def setType(self, t):
        """
        Set the datatype of the node.

        Arguments:
        t -- the type of the node as a string.
        """
        self.dataType = t

    def getType(self):
        """
        Return the type of the node, if it was previously set,
        or None otherwise.
        """
        return self.dataType


class DecorationLiteralNode(Node):

    """A Node which represents a decoration in the AST."""

    def __init__(self, val):
        """
        Initialize a DecorationLiteralNode with the parsed value of the
        decoration.
        """
        self.val = val


class NotAnIntervalNode(Node):

    """A Node which represents NaI in the AST."""

    def setType(self, t):
        """
        Set the datatype of the node.

        Arguments:
        t -- the type of the node as a string.
        """
        self.dataType = t

    def getType(self):
        """Return 'interval<double>' as the type of the node."""
        return self.dataType


class EmptyIntervalNode(Node):

    """A Node which represents an Empty-Interval in the AST."""

    def __init__(self):
        """Initializes an EmptyIntervalNode."""
        self.decoration = None

    def setDecoration(self, dec):
        """
        Set a decoration for the interval.

        Arguments:
        dec -- a DecorationLiteralNode object
        """
        self.decoration = dec

    def setType(self, t):
        """
        Set the datatype of the node.

        Arguments:
        t -- the type of the node as a string.
        """
        self.dataType = t

    def getType(self):
        """Return 'interval<double>' as the type of the node."""
        return self.dataType


class EntireIntervalNode(Node):

    """A Node which represents an Entire-Interval in the AST."""

    def __init__(self):
        """Initialize an EntireIntervalNode."""
        self.decoration = None

    def setDecoration(self, dec):
        """
        Set a decoration for the interval.

        Arguments:
        dec -- a DecorationLiteralNode object
        """
        self.decoration = dec

    def setType(self, t):
        """
        Set the datatype of the node.

        Arguments:
        t -- the type of the node as a string.
        """
        self.dataType = t

    def getType(self):
        """Return 'interval<double>' as the type of the node."""
        return self.dataType


class InfSupIntervalNode(Node):

    """A Node which represents a regular interval in the AST."""

    def __init__(self, inf, sup):
        """
        Initialize an InfSupIntervalNode.

        Arguments:
        inf -- the lower border of the interval
        sup -- the upper border of the interval
        """
        self.inf = inf
        self.sup = sup
        self.decoration = None

        # check if types of inf and sup are the same
        if inf.getType() != sup.getType():
            raise IOError('''can not instantiate infsup interval with two
                different data types''')

    def setDecoration(self, dec):
        """
        Set a decoration of the interval.

        Arguments:
        dec -- a DecorationLiteral object
        """
        self.decoration = dec

    def getType(self):
        """
        Return the type of the interval.
        """
        return 'interval<' + self.inf.getType() + '>'


class ArrayLiteralNode(Node):
    """
    Initialize an ArrayLiteralNode.

    Arguments:
    values -- A list of the array values. If None, an empty
              ArrayLiteralNode is created.
    """
    def __init__(self, values=None):
        self.vals = values

    """
    Return the type of the array.
    """
    def getType(self):
        if not self.vals:
            return 'array<double>'
        return 'array<' + self.vals[0].getType() + '>'

    """
    Return the type of the literals.
    """
    def getLiteralType(self):
        if not self.vals:
            return 'double'
        return self.vals[0].getType()


class AccurateOutputsNode(Node):

    """A Node which represents the accurate output in the AST."""

    def __init__(self, literals):
        """
        Initialize an AccurateOutputsNode.

        Arguments:
        literals -- list of literal nodes which represent the accurate outputs
        """
        self.literals = literals


class TightestOutputsNode(Node):

    """A Node which represents the tightest output in the AST."""

    def __init__(self, literals):
        """
        Initialize a TightestOutputsNode.

        Arguments:
        literals -- list of literal nodes which represent the tightest outputs
        """
        self.literals = literals

class InputsNode(Node):

    """A Node which represents the inputs in the AST."""

    def __init__(self, literals):
        """
        Initialize an InputsNode.

        Arguments:
        literals -- list of literal nodes which represent the inputs
        """
        self.literals = literals


class QualidentNode(Node):

    """A Node which represents a qualified identifier in the AST."""

    def __init__(self, val):
        """
        Initialize a QualidentNode with the value of the first identifier.
        """
        self.val = val

    def appendIdentifier(self, val):
        """
        Append an identifier.

        Arguments:
        val -- value of the identifier
        """
        self.val += '.' + val


class OperationNameNode(Node):

    """A Node which represents the name of an operation in the AST."""

    def __init__(self, ident):
        """
        Initialize an OperationNameNode with an identifier.

        Arguments:
        ident -- the identifier
        """
        self.ident = ident


class TestNode(Node):

    """A Node which represents a test in the AST."""

    def __init__(self, opName, inputs, tightestOutputs, accurateOutputs):
        """
        Initialize a TestNode.

        Arguments:
        opName -- an OperationNameNode object
        inputs -- an InputsNode object
        tightestOutputs -- a TightestOutputsNode object
        accurateOutputs -- a AccurateOutputsNode object
        """
        self.opName = opName
        self.inputs = inputs
        self.tightestOutputs = tightestOutputs
        self.accurateOutputs = accurateOutputs
        self.comments = []

    def appendComment(self, comment):
        """
        Add a comment to the test.

        Arguments:
        comment -- A LineCommentNode object or a BlockCommentNode object
        """
        self.comments = [comment] + self.comments


class TestcaseNode(Node):

    """A Node which represents a testcase in the AST."""

    def __init__(self, name, tests):
        """
        Initialize a TestcaseNode.

        Arguments:
        name -- an IdentifierNode object
        tests -- a list of TestNode objects
        """
        self.name = name
        self.tests = tests
        self.comments = []

    def appendComment(self, comment):
        """
        Add a comment to the testcase.

        Arguments:
        comment -- a LineCommentNode object or a BlockCommentNode object
        """
        self.comments += [comment]


class DSLNode(Node):

    """The root node which represents a complete test suite."""

    def __init__(self, testcases):
        """
        Initialize a DSLNode.

        Arguments:
        testcases -- a list of TestCaseNode objects
        """
        self.testcases = testcases
        self.comments = []

    def appendComment(self, comment):
        """
        Add a global comment to the DSL.

        Arguments:
        comment -- A LineCommentNode object or a BlockCommentNode object
        """
        self.comments += [comment]

    def setFileName(self, fileName):
        """
        Set the name of the file.

        Arguments:
        fileName -- name of the file as a string
        """
        self.fileName = fileName

class ASTVisitor(object):

    """Default visitor class."""

    def __init__(self, outputSpecification, cbPath):
        """
        Initialize the visitor.

        Arguments:
        outputSpecification -- an OutputSpecification object
        cbPath -- path to a callbacks.py module in python notification, i.e.
                  with delimiting dots rather than slashes
        """
        self.out = outputSpecification
        self.cbPath = cbPath
        self.cbs = None
        self.warnings = set()

        # import callback methods if callbacks.py exists
        if cbPath is not None:
            self.cbs = importlib.import_module(cbPath)

    def visitLineCommentNode(self, node):
        """
        Return a line comment specific to the language.

        Replaces the leading double slash by the line comment token of the
        language.

        Arguments:
        node -- a LineCommentNode object
        """
        tmp = self.out.lang_line_comment_token + node.val[2:]
        return tmp

    def visitBlockCommentNode(self, node):
        """
        Return a block comment specific to the language.

        Replaces the leading /* and trailing */ by the block comment start
        and block comment end tokens. Additionally, it inserts the block
        comment intermediate token at the beginning of every line.

        Arguments:
        node -- a BlockCommentNode object
        """
        content = node.val[2:-2].split('\n')

        if not content[-1] or content[-1].isspace():
            content = content[:-1]
        if not content[0] or content[0].isspace():
            content = content[1:]
        tmp = [self.out.lang_block_comment_start]
        tmp.append('\n')
        tmp.append('\n'.join((self.out.lang_block_comment_intermediate +
                   c for c in content)))
        tmp.append('\n')
        tmp.append(self.out.lang_block_comment_end)
        return ''.join(tmp)

    def visitIdentifierNode(self, node):
        """
        Return the parsed value of the identifier.

        Arguments:
        node -- an IdentifierNode object
        """
        return node.val

    def visitNaNNode(self, node):
        """
        Return the translated value of NaN.

        Arguments:
        node -- a NaNNode object
        """
        return getattr(self.out, 'lang_not_a_number_' + node.dataType)

    def visitOverlapLiteralNode(self, node):
        """
        Return the translation of an OverlapLiteralNode.

        Example:
        If o is of type OverlapLiteralNode and o.val is 'meets', then return
        the value of arith_overlap_meets of the output specification.

        Arguments:
        node -- an OverlapLiteralNode object
        """
        return getattr(self.out, 'arith_overlap_' + node.val)

    def visitBooleanLiteralNode(self, node):
        """
        Return the translation of a BooleanLiteralNode.

        Example:
        If o is of type BooleanLiteralNode and o.val is 'true', then return
        the value of lang_boolean_true of the output specification.

        Arguments:
        node -- a BooleanLiteralNode object
        """
        return getattr(self.out, 'lang_boolean_' + node.val)

    def visitStringLiteralNode(self, node):
        """
        Return the value of a string enclosed by the language's string tokens.

        Invokes the callback method cb_string.

        Arguments:
        node -- a StringLiteralNode object
        """
        return self.cb_func('cb_string')(node.val)

    def visitIntegerLiteralNode(self, node):
        """
        Return the value of an IntegerLiteralNode.

        Invokes the callback method cb_int.

        Arguments:
        node -- an IntegerLiteralNode object
        """
        return self.cb_func('cb_int')(node.val)

    def visitFloatingPointNode(self, node):
        """
        Return the value of a FloatingPointNode.

        Invokes the callback method cb_fpNum.

        Arguments:
        node -- a FloatingPointNode object
        """
        return self.cb_func('cb_fpNum')(node.val)

    def visitInfinityLiteralNode(self, node):
        """
        Return the translation of an InfinityLiteralNode.

        Depending on the sign and dataType attributes of the node object,
        return the value arith_infinity_SIGN_DATATYPE where SIGN is either
        'plus' or 'minus' and DATATYPE is either 'double' or 'float'.

        Arguments:
        node -- an InfinityLiteralNode object
        """
        if node.sign == '+':
            return getattr(self.out, 'lang_infinity_plus_' + node.dataType)
        return getattr(self.out, 'lang_infinity_minus_' + node.dataType)

    def visitDecorationLiteralNode(self, node):
        """
        Return the translation of a DecorationLiteralNode.

        Depending on node.val, return the value of arith_decorator_VALUE
        where VALUE = node.val

        Arguments:
        node -- a DecorationLiteralNode object
        """
        return getattr(self.out, 'arith_decorator_' + node.val)

    def visitNotAnIntervalNode(self, node):
        """
        Return the translation of a NotAnIntervalNode.

        Specifically, return the value of the output specification's
        arith_nai_interval attribute.

        Arguments:
        node -- a NotAnIntervalNode object
        """
        # remove 'interval<' at the beginning and '>' at the end
        innerDataType = node.getType()[9:][:-1]

        return getattr(self.out, 'arith_nai_interval_' + innerDataType)

    def visitEmptyIntervalNode(self, node):
        """
        Return the translation of an EmptyIntervalNode object.

        If the node is decorated, replace the 'DEC' template of the
        output specification's arith_decorated_empty_interval
        attribute's value and return the result.
        Else, return the value of the output specification's
        arith_empty_interval value.

        Arguments:
        node -- an EmptyIntervalNode object.
        """
        # remove 'interval<' at the beginning and '>' at the end
        innerDataType = node.getType()[9:][:-1]

        if node.decoration:
            tmpl = getattr(self.out, 'arith_decorated_empty_interval_' + innerDataType)
            return self.replTok(tmpl, 'DEC', node.decoration.accept(self))

        return getattr(self.out, 'arith_empty_interval_' + innerDataType)

    def visitEntireIntervalNode(self, node):
        """
        Return the translation of an EntireIntervalNode object.

        If the node is decorated, replace the 'DEC' template of the
        output specification's arith_decorated_entire_interval attribute's
        value and return the result.
        Else, return the value of the output specification's
        arith_entire_interval value.

        Arguments:
        node -- an EntireIntervalNode object.
        """
        # remove 'interval<' at the beginning and '>' at the end
        innerDataType = node.getType()[9:][:-1]

        if node.decoration:
            tmpl = getattr(self.out,
                           'arith_decorated_entire_interval_' + innerDataType)
            return self.replTok(tmpl, 'DEC', node.decoration.accept(self))
        return getattr(self.out, 'arith_entire_interval_' + innerDataType)

    def visitInfSupIntervalNode(self, node):
        """
        Return the translation of an InfSupIntervalNode.

        If the interval is decorated, we use the decorated_inf_sup_interval_TYPE
        key, else inf_sup_interval_TYPE, where TYPE is either float, double or
        long_double.

        Arguments:
        node -- an InfSupIntervalNode object
        """
        inf = node.inf.accept(self)
        sup = node.sup.accept(self)
        arg_type = node.inf.getType()

        if node.decoration:
            dec = node.decoration.accept(self)
            tmp = getattr(self.out, 'arith_decorated_inf_sup_interval_' +
                          arg_type)
            tmp = self.replTok(tmp, 'ARG1', inf)
            tmp = self.replTok(tmp, 'ARG2', sup)
            return self.replTok(tmp, 'DEC', dec)

        else:
            tmp = getattr(self.out, 'arith_inf_sup_interval_' + arg_type)
            tmp = self.replTok(tmp, 'ARG1', inf)
            return self.replTok(tmp, 'ARG2', sup)

    def visitArrayLiteralNode(self, node):
        if not node.vals:
            return getattr(self.out, 'lang_array_empty')

        arg_type = node.vals[0].getType()
        tmp = getattr(self.out, 'lang_array_' + arg_type)

        arr_sep = getattr(self.out, 'lang_array_arg_separator')
        concat_vals = arr_sep.join([str(v.accept(self)) for v in node.vals])
        tmp = self.replTok(tmp, 'ARGS', concat_vals)

        return tmp


    def visitAccurateOutputsNode(self, node):
        """
        Return the values of the accurate outputs as a list.

        Arguments:
        node -- an AccurateOutputsNode object
        """
        return node.literals

    def visitTightestOutputsNode(self, node):
        """
        Return the values of the tightest outputs as a list.

        Arguments:
        node -- an TightestOutputsNode object
        """
        return node.literals

    def visitInputsNode(self, node):
        """
        Return the values of the inputs as a list.

        Arguments:
        node -- an InputsNode object
        """
        return [n.accept(self) for n in node.literals]

    def visitQualidentNode(self, node):
        """
        Return the parsed value of a QualidentNode.

        Arguments:
        node -- a QualidentNode object
        """
        return self.cb_func('cb_qualident')(node.val)

    def visitOperationNameNode(self, node):
        """
        Return the translation of an OperationNameNode.

        Specifically, it returns the value of the node's ident attribute.

        Arguments:
        node -- an OperationNameNode object.
        """
        return node.ident.accept(self)

    def visitTestNode(self, node):
        """
        Return the translation of a TestNode.

        """

        # Get the value of the operation from the arith.yaml file
        if node.accurateOutputs:
            accurateTypes = ','.join(n.getType()
                                     for n in node.accurateOutputs.literals)

        if node.tightestOutputs:
            tightestTypes = ','.join(n.getType()
                                     for n in node.tightestOutputs.literals)

        if node.accurateOutputs and node.tightestOutputs:
            if accurateTypes != tightestTypes:
                raise IOError('''types of accurate and tightest outputs may not
                               differ''')
        if node.accurateOutputs:
            outputTypes = accurateTypes
        else:
            outputTypes = tightestTypes

        inputTypes = ','.join(n.getType() for n in node.inputs.literals)

        opKey = self.findOp('arith_op_' + node.opName.accept(self),
                            'arith_op_' + node.opName.accept(self) +
                            '<<' + outputTypes + '>>' +
                            '<' + inputTypes + '>')
        if not opKey:
            return ""

        # Special handling if array literals are present
        varInfo, arrayDefSeq = self.handleArrayValues(node)

        opVal = getattr(self.out, opKey)

        # Replace the ARG placeholders
        inputList = node.inputs.accept(self)
        for i in range(0, len(inputList)):
            if node.inputs.literals[i] not in varInfo:
                opVal = self.replTok(opVal, 'ARG' + str(i + 1),
                                     inputList[i])
            else:
                opVal = self.replTok(opVal, 'ARG' + str(i + 1),
                                     varInfo[node.inputs.literals[i]][0])
                opVal = self.replTok(opVal, 'ARG' + str(i + 1) + '_LEN',
                                     varInfo[node.inputs.literals[i]][1])

        # Build a list of lists for the value -- the first level
        # identifies the sections separated by '*** next output' and the
        # second level the multiple lines of every section
        opVals = opVal.split('\n*** next output\n')

        opVals = [list(filter(lambda s: s != "", el.split('\n')))
               for el in opVals]

        # Process outputs
        tstLst = []
        delim = self.out.lang_line_end_token
        opKey = self.findOp('arith_op_decorationPart',
                            'arith_op_decorationPart')
        if opKey:
            decPrt = getattr(self.out, opKey)
        else:
            # Decorations not supported by the arithmetic, disable all
            # testcases with decorated intervals.
            for i in range(0, len(node.inputs.literals)):
                if hasattr(node.inputs.literals[i], 'decoration') and node.inputs.literals[i].decoration is not None:
                    return ""
            decPrt = None
        subset = getattr(self.out, self.findOp('arith_op_subset',
                                                'arith_op_subset'))
        assertEq = self.out.test_assert_equals
        assertTrue = self.out.test_assert_true
        assertWarn = self.out.test_assert_equals_warning
        lessEq = self.out.arith_decorator_less_equals
        greaterEq = self.out.arith_decorator_greater_equals
        andConj = self.out.lang_logical_and
        isNaNFnc = self.out.lang_op_isNaN

        if node.tightestOutputs:
            tghtLst = node.tightestOutputs.accept(self)
        if node.accurateOutputs:
            accLst = node.accurateOutputs.accept(self)

        # Translation of "op A B = C" where "op" is an arbitrary
        # operation and A, B, C are intervals
        # Result will be:
        #
        # assert_eq (op(A, B), C)
        # if decorated:
        #  assert_eq (dec(op(A,B)), dec(C))
        if node.accurateOutputs is None:
            for sec in range(0, len(tghtLst)):
                # true if any input or output literal is an array
                containsArr = bool(arrayDefSeq.strip())
                if containsArr:
                    # add array definitions
                    tstLst += [arrayDefSeq]

                if tghtLst[sec] in varInfo:
                    # use the previously assigned variable name instead
                    # of the literal value
                    outp = varInfo[tghtLst[sec]][0]
                else:
                    outp = tghtLst[sec].accept(self)

                # translation with isNaN function
                if type(tghtLst[sec]) is NaNNode:
                    for line in range(0, len(opVals[sec])):
                        tst = self.replTok(assertTrue, 'ARG1', isNaNFnc)
                        tst = self.replTok(tst, 'ARG1', opVals[sec][line])
                        tstLst += [tst + delim]
                    
                else:
                    # translation with assertEquals
                    for line in range(0, len(opVals[sec])):
                        tst = self.replTok(assertEq, 'ARG2', outp)
                        tst = self.replTok(tst, 'ARG1', opVals[sec][line])
                        tstLst += [tst + delim]

                        if hasattr(tghtLst[sec], 'decoration') and tghtLst[sec].decoration is not None:
                            dec = tghtLst[sec].decoration.accept(self)
                            outpDec = self.replTok(decPrt, 'ARG1', outp)
                            inpDec = self.replTok(decPrt, 'ARG1', opVals[sec][line])
                            tst = self.replTok(assertEq, 'ARG2', outpDec)
                            tst = self.replTok(tst, 'ARG1', inpDec)
                            tstLst += [tst + delim]

        # Translation of "op A B <= D" where "op" is an arbitrary
        # operation and A, B, D are intervals
        # Result will be:
        #
        # assert_true op(A, B) is subset of D
        # if decorated:
        #  assert_eq (dec(op(A,B)), dec(D))
        elif node.tightestOutputs is None:

            for sec in range(0, len(accLst)):
                # NaN literals not allowed as outputs
                if type(accLst[sec]) is NaNNode:
                    raise IOError('NaN literals not supported as accurate outputs')
                outp = accLst[sec].accept(self)

                for line in range(0, len(opVals[sec])):
                    tst = self.replTok(subset, 'ARG1', opVals[sec][line])
                    tst = self.replTok(tst, 'ARG2', outp)
                    tst = self.replTok(assertTrue, 'ARG1', tst)
                    tstLst += [tst + delim]

                    if hasattr(accLst[sec], 'decoration') and accLst[sec].decoration is not None:
                        dec = accLst[sec].decoration.accept(self)
                        outpDec = self.replTok(decPrt, 'ARG1', outp)
                        inpDec = self.replTok(decPrt, 'ARG1', opVals[sec][line])
                        tst = self.replTok(assertEq, 'ARG2', outpDec)
                        tst = self.replTok(tst, 'ARG1', inpDec)
                        tstLst += [tst + delim]

        # Translation of "op A B = C <= D", where "op" is an arbitrary
        # operation and A, B, C, D are intervals
        # Result will be:
        #
        # assert_warn op(A, B) = C
        # assert_true C is subset of op(A,B)
        # assert_true op(A,B) is subset of D
        # if decorated:
        #  assert_true dec(C) <= dec(op(A,B)) and dec(D) >= dec(op(A,B))
        else:

            # equals warning check
            for sec in range(0, len(tghtLst)):
                # NaN literals not allowed as outputs
                if type(tghtLst[sec]) is NaNNode:
                    raise IOError('NaN literals not supported in combination with accurate outputs')
                outp = tghtLst[sec].accept(self)
                for line in range(0, len(opVals[sec])):
                    tst = self.replTok(assertWarn, 'ARG2', outp)
                    tst = self.replTok(tst, 'ARG1', opVals[sec][line])
                    tstLst += [tst + delim]

            # first subset check
            for sec in range(0, len(tghtLst)):
                outp = tghtLst[sec].accept(self)
                for line in range(0, len(opVals[sec])):
                    tst = self.replTok(subset, 'ARG2', opVals[sec][line])
                    tst = self.replTok(tst, 'ARG1', outp)
                    tst = self.replTok(assertTrue, 'ARG1', tst)
                    tstLst += [tst + delim]

            # second subset check
            for sec in range(0, len(accLst)):
                # NaN literals not allowed as outputs
                if type(accLst[sec]) is NaNNode:
                    raise IOError('NaN literals not supported as accurate outputs')
                outp = accLst[sec].accept(self)
                for line in range(0, len(opVals[sec])):
                    tst = self.replTok(subset, 'ARG1', opVals[sec][line])
                    tst = self.replTok(tst, 'ARG2', outp)
                    tst = self.replTok(assertTrue, 'ARG1', tst)
                    tstLst += [tst + delim]

            # check decorations
            for sec in range(0, len(tghtLst)):
                valid = (hasattr(tghtLst[sec], 'decoration') and
                         hasattr(accLst[sec], 'decoration') and
                         tghtLst[sec].decoration is not None and
                         accLst[sec].decoration is not None)
                if not valid:
                        continue


                tOutp = tghtLst[sec].accept(self)
                aOutp = accLst[sec].accept(self)
                tOutpDec = tghtLst[sec].decoration.accept(self)
                aOutpDec = accLst[sec].decoration.accept(self)
                for line in range(0, len(opVals[sec])):
                    if tOutpDec != aOutpDec:
                        raise IOError("either both or none of the outputs can be decorated")

                    if tOutpDec:
                        decLB = self.replTok(decPrt, 'ARG1', tOutp)
                        decUB = self.replTok(decPrt, 'ARG1', aOutp)
                        decInp = self.replTok(decPrt, 'ARG1', opVals[sec][line])

                        tstLB = self.replTok(lessEq, 'ARG1', decLB)
                        tstLB = self.replTok(tstLB, 'ARG2', decInp)
                        tstUB = self.replTok(greaterEq, 'ARG1', decUB)
                        tstUB = self.replTok(tstUB, 'ARG2', decInp)
                        tstBoth = self.replTok(andConj, 'ARG1', tstLB)
                        tstBoth = self.replTok(tstBoth, 'ARG2', tstUB)
                        tstBoth = self.replTok(assertTrue, 'ARG1', tstBoth)
                        tstLst += [tstBoth + delim]


        # Format text

        tstTxts = '\n'.join(tstLst)
        commentTxt = '\n'.join([c.accept(self) for c in node.comments])
        txt = self.replTok(self.out.test_test_seq.strip(), 'COMMENTS',
                                 commentTxt).strip()
        txt = self.replTok(txt, 'ASSERTS', tstTxts) + '\n'

        return txt

    def handleArrayValues(self, node):
        """
        Check if there are any arrays involved in the current test,
        and if so prepares the array definitions and a mapping of the
        definitions to variable names.

        Returns a dictionary which maps a input or output literal to a
        tuple t, where t[0] is the name of the variable the literal is
        stored in and t[1] is the length of the array.
        """

        # check if anything to do
        containsArr = False
        for i in node.inputs.literals:
            if type(i) is ArrayLiteralNode:
                containsArr = True
                break

        if not containsArr and node.tightestOutputs:
            for i in node.tightestOutputs.literals:
                if type(i) is ArrayLiteralNode:
                    containsArr = True
                    break

        if node.accurateOutputs:
            for i in node.accurateOutputs.literals:
                if type(i) is ArrayLiteralNode:
                    raise IOError("""Arrays not permitted for accurate
                                     outputs""")

        if not containsArr:
            return dict(), ''

        # Now  at least one array is present
        varInfo = dict()
        defLst = []
        inpNameGen = InpVarNameGenerator(self)
        outpNameGen = OutpVarNameGenerator(self)
        for i in node.inputs.literals:
            if type(i) is ArrayLiteralNode:
                litType = i.getLiteralType()
                name = inpNameGen.next()
                val = i.accept(self)
                length = len(i.vals) if i.vals else 0

                tmp = getattr(self.out, 'lang_array_def')
                tmp = self.replTok(tmp, 'TYPE', litType)
                tmp = self.replTok(tmp, 'NAME', name)
                tmp = self.replTok(tmp, 'VAL', val)

                defLst += [tmp]
                varInfo[i] = (name, length)

        for i in node.tightestOutputs.literals:
            if type(i) is ArrayLiteralNode:
                litType = i.getLiteralType()
                name = outpNameGen.next()
                val = i.accept(self)
                length = len(i.vals) if i.vals else 0

                tmp = getattr(self.out, 'lang_array_def')
                tmp = self.replTok(tmp, 'TYPE', litType)
                tmp = self.replTok(tmp, 'NAME', name)
                tmp = self.replTok(tmp, 'VAL', val)

                defLst += [tmp]
                varInfo[i] = (name, length)

        inpNameGen.next_section()
        outpNameGen.next_section()

        arrayDefSeq = '\n'.join(defLst)

        return varInfo, arrayDefSeq

    def visitTestcaseNode(self, node):
        """
        Return the translation of a TestcaseNode.

        Replaces the 'COMMENTS' and 'TC_NAME' and 'TESTS' tokens of the value
        of the output specification's test_testcase_seq attribute and returns
        the result.

        Arguments:
        node -- a TestCaseNode object
        """

        tmp = self.out.test_testcase_seq
        tmp = self.replTokList(tmp, 'COMMENTS', [n.accept(self) for
                                                      n in node.comments])
        tmp = self.replTok(tmp, 'TC_NAME', node.name)
        if self.out.lang_indent_tests:
            rplList = [self.indent(n.accept(self).strip(),
                                   self.out.lang_spaces_indent) for n in
                       node.tests]
        else:
            rplList = [n.accept(self).strip() for n in node.tests]

        rplList = list(filter(lambda x: not x.isspace(), rplList))

        tmp = self.replTokList(tmp, 'TESTS', rplList)
        return tmp

    def visitDSLNode(self, node):
        """
        Return the translation of a DSLNode.

        Replaces the 'LANGUAGE_IMPORTS', 'TESTLIB_IMPORTS', 'ARITHLIB_IMPORTS',
        'NAME' and 'TESTCASES' tokens of the value of the output
        specification's test_testfile_seq attribute.

        Arguments:
        node -- a DSLNode object
        """
        tmp = self.out.test_testfile_seq

        tmp = self.replTokList(tmp, 'COMMENTS', [n.accept(self) for
                                                      n in node.comments])

        # imports
        languageImportComment = self.out.lang_line_comment_token + \
            "Language imports"
        testlibImportComment = self.out.lang_line_comment_token + \
            "Test library imports"
        arithlibImportComment = self.out.lang_line_comment_token + \
            "Arithmetic library imports"
        preambleComment = self.out.lang_line_comment_token + "Preamble"

        tmp = self.replTok(tmp, 'LANGUAGE_IMPORTS',
                                (languageImportComment + '\n' +
                                    self.out.lang_imports).strip() + '\n')

        tmp = self.replTok(tmp, 'TESTLIB_IMPORTS',
                                (testlibImportComment + '\n' +
                                    self.out.test_imports).strip() + '\n')

        tmp = self.replTok(tmp, 'ARITHLIB_IMPORTS',
                                (arithlibImportComment + '\n' +
                                    self.out.arith_imports).strip() + '\n')

        tmp = self.replTok(tmp, 'PREAMBLE',
                                (preambleComment + '\n' +
                                    self.out.arith_preamble).strip() + '\n')

        tmp = self.replTok(tmp, 'NAME',
                                node.fileName.split('.')[0].title())
        if self.out.lang_indent_testcases:
            rplList = [self.indent(n.accept(self), self.out.lang_spaces_indent)
                       for n in node.testcases]
        else:
            rplList = [n.accept(self).strip() for n in node.testcases]

        # reset variable generator numbers
        InpVarNameGenerator(self).reset()
        OutpVarNameGenerator(self).reset()

        # testcasesComment = self.out.lang_line_comment_token + \
        #                        "Testcases"
        # rplList.insert(0, testcasesComment)

        tmp = self.replTokList(tmp, 'TESTCASES', rplList, delim="\n\n")

        return (tmp, self.warnings)

    def replTok(self, text, token, replacement):
        """
        Replace a token in a template string.

        Specifically, it replaces the string '$token' in 'text' with either
        'replacement.accept(self)', if replacement is of type node, or with
        just 'replacement' otherwise.

        Arguments:
        text -- the text which contains a token
        token -- the string identifiying the token to be replaced
        replacement -- the replacement for the token
        """
        tmp = Template(text)
        if not isinstance(replacement, Node):
            tmp = tmp.safe_substitute({token: replacement})
        else:
            tmp = tmp.safe_substitute({token: replacement.accept(self)})
        return tmp

    def replTokList(self, text, token, repl_list, delim='\n'):
        """
        Replace a token, similar to the replTok method but with a list
        of replacements.

        Arguments:
        text -- the text which contains a token
        token -- the string identifiying the token to be replaced
        repl_list -- a list of replacements for the token
        delim -- a delimiting string which concatenates the values of repl_list
        """
        if len(repl_list) == 0:
            return self.replTok(text, token, '')

        tmp = text
        for i in range(0, len(repl_list) - 1):
            if not isinstance(repl_list[i], Node):
                sub = repl_list[i] + delim + '$' + token
            else:
                sub = repl_list[i].accept(self) + delim + '$' + token
            tmp = self.replTok(tmp, token, sub)
        tmp = self.replTok(tmp, token, repl_list[-1])
        return str(tmp)

    def containsToken(self, text, token):
        """
        Return true if 'text' contains the token 'token'.

        Arguments:
        text -- a string
        token -- a string identifying a token in terms of template strings
        """
        tok1 = '$' + token
        tok2 = '${' + token + '}'

        return tok1 in text or tok2 in text

    def indent(self, text, numSpaces):
        """
        Add 'numSpaces' spaces in front of every line of 'text'

        Arguments:
        text -- a string
        numSpaces -- an integral value
        """
        lst = [(numSpaces*' ' + e) for e in text.split('\n')]
        return '\n'.join(lst)

    def present(self, cb_method):
        """
        Return true if 'cb_method' is a defined callback method.

        Arguments:
        cb_method -- the name of a callback method
        """
        if self.cbs:
            return hasattr(self.cbs, cb_method)

    def cb_func(self, name):
        """
        Returns the callback function to be used.

        If no such function is defined, it returns the identity function.

        Arguments:
        name -- a string denoting the name of the callback method
        """
        if self.present(name):
            return getattr(self.cbs, name)
        return self.identity_func

    def identity_func(self, val):
        """
        Return val.

        Arguments:
        val -- an object
        """
        return val

    def findOp(self, opPrefix, opName):
        """
        Return the closest match for a function.

        Specifically, return the function with the longest name which starts
        with 'opPrefix' and continues with a string which matches 'opName'.
        This continuation may contain wildcard characters which are used as an
        abbreviation of the regex expression '.*' here.
        Prints a warning to the console if no matching operation was found.

        Arguments:
        opPrefix -- the prefix of the operation which must be matched exactly
        opName -- the continuation which may contain wildcard characters.
        """
        lst = [op for op in dir(self.out) if op.startswith(opPrefix)]
        lst.sort(key=len, reverse=True)

        for el in lst:
            if re.match(el.replace('*', '.*'), opName):
                return el

        self.warnings.add('WARNING: no matching operation found for operation '+
                          opName + ', language ' + self.out.lang_name)
        return None


class InpVarNameGenerator(object):
    _instance = None
    inner_count = 0
    section_count = 1
    ast_visitor = None
    def __new__(cls, ast_visitor):
        if not cls._instance:
            cls._instance = super(InpVarNameGenerator, cls).__new__(
                                cls)
            cls.ast_visitor = ast_visitor
        return cls._instance

    def next(cls):
        cls._instance.inner_count += 1
        var_name = 'in_' + str(cls._instance.section_count) + '_' + \
               str(cls._instance.inner_count)
        return cls.ast_visitor.cb_func('cb_inp_var_name')(var_name)

    def next_section(cls):
        cls._instance.section_count += 1
        cls._instance.inner_count = 0

    def reset(cls):
        cls.section_count = 1
        cls.inner_count = 0

class OutpVarNameGenerator(object):
    _instance = None
    inner_count = 0
    section_count = 1
    ast_visitor = None
    def __new__(cls, ast_visitor):
        if not cls._instance:
            cls._instance = super(OutpVarNameGenerator, cls).__new__(
                                cls)
            cls.ast_visitor = ast_visitor
        return cls._instance

    def next(cls):
        cls._instance.inner_count += 1
        var_name = 'out_' + str(cls._instance.section_count) + '_' + \
               str(cls._instance.inner_count)
        return cls.ast_visitor.cb_func('cb_outp_var_name')(var_name)

    def next_section(cls):
        cls._instance.section_count += 1
        cls._instance.inner_count = 0

    def reset(cls):
        cls.section_count = 1
        cls.inner_count = 0


