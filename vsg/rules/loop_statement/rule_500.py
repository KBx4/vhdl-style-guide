
from vsg.rules import token_case as Rule

from vsg import token

lTokens = []
lTokens.append(token.loop_statement.loop_keyword)


class rule_500(Rule):
    '''
    This rule checks the **loop** keyword has proper case.

    Refer to the section `Configuring Uppercase and Lowercase Rules <configuring.html#configuring-uppercase-and-lowercase-rules>`_ for information on changing the default case.

    **Violation**

    .. code-block:: vhdl

       while (condition) LOOP

    **Fix**

    .. code-block:: vhdl

       while (condition) loop
    '''

    def __init__(self):
        Rule.__init__(self, 'loop_statement', '500', lTokens)
        self.groups.append('case::keyword')
