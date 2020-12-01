
import bisect
import pprint


class New():

    def __init__(self, dMap):
        self.dMap = dMap

    def get_token_indexes(self, oToken):
        lReturn = []
        sBase, sSub = extract_unique_id(oToken)
        try:
            return self.dMap[sBase][sSub]
        except KeyError:
            return []

    def get_token_indexes_between_indexes(self, oToken, iStart, iEnd):
        lReturn = []
        lIndexes = self.get_token_indexes(oToken)
        for iIndex in lIndexes:
            if iIndex > iStart and iIndex < iEnd:
                lReturn.append(iIndex)
        return lReturn

    def get_line_number_of_index(self, iIndex):
        iLine = bisect.bisect_left(self.dMap['parser']['carriage_return'], iIndex) + 1
        return iLine

    def get_index_of_carriage_return_after_index(self, iIndex):
        iTemp = bisect.bisect_right(self.dMap['parser']['carriage_return'], iIndex)
        return self.dMap['parser']['carriage_return'][iTemp]

    def get_index_of_token_after_index(self, oToken, iIndex):
        sBase, sSub = extract_unique_id(oToken)
        try:
            iTemp = bisect.bisect_right(self.dMap[sBase][sSub], iIndex)
            return self.dMap[sBase][sSub][iTemp]
        except IndexError:
            return None
        except KeyError:
            return None

    def get_token_pair_indexes(self, oStart, oEnd):
        lStartIndexes = self.get_token_indexes(oStart)
        lEndIndexes = []
        for iIndex in lStartIndexes:
            lEndIndexes.append(self.get_index_of_token_after_index(oEnd, iIndex))
        return lStartIndexes, lEndIndexes

    def get_index_of_next_non_whitespace_token(self, iIndex):
        iStartIndex = iIndex + 1
        lTokens = [None, None, None, None]
        lBaseKeys = list(self.dMap.keys())
        for sBaseKey in lBaseKeys:
            lSubKeys = list(self.dMap[sBaseKey].keys())
            if sBaseKey == 'parser':
                lSubKeys.remove('whitespace')
                lSubKeys.remove('carriage_return')
                lSubKeys.remove('blank_line')
            for sSubKey in lSubKeys:
                for iIdx in range(0, 4):
                    iSearchIdx = iStartIndex + iIdx
                    if iSearchIdx in self.dMap['parser'][sSubKey]:
                        lTokens[iIdx] = iSearchIdx
                        continue

        for iToken in lTokens:
            if iToken is not None:
                return iToken
        return None

    def is_token_at_index(self, oToken, iIndex):
        sBase, sSub = extract_unique_id(oToken)
        if iIndex in self.dMap[sBase][sSub]:
            return True
        return False

    def pretty_print(self):
        pp=pprint.PrettyPrinter(indent=4)
        pp.pprint(self.dMap)


def extract_unique_id(oToken):
    sBase = None
    sSub = None
    lDoc = oToken.__doc__.split()
    for iDoc, sDoc in enumerate(lDoc):
        if sDoc == 'unique_id':
            return lDoc[iDoc + 2], lDoc[iDoc + 4]
    return None, None


def process_tokens(lTokens):
    iLibIndex = 0
    dMap = build_default_map()
    for iToken, oToken in enumerate(lTokens):
        sBase, sSub = oToken.get_unique_id()
        if sBase is not None:
           try:
               dMap[sBase][sSub].append(iToken)
           except KeyError:
               try:
                   dMap[sBase][sSub] = []
                   dMap[sBase][sSub].append(iToken)
               except KeyError:
                   dMap[sBase] = {}
                   dMap[sBase][sSub] = []
                   dMap[sBase][sSub].append(iToken)
        if sBase == 'logical_operator':
            try:
                dMap[sBase][sBase].append(iToken)
            except KeyError:
                try:
                    dMap[sBase][sBase] = []
                    dMap[sBase][sBase].append(iToken)
                except KeyError:
                    dMap[sBase] = {}
                    dMap[sBase][sBase] = []
                    dMap[sBase][sBase].append(iToken)
            continue
        if sSub == 'comma':
            try:
                if iToken not in dMap['parser']['comma']:
                    dMap['parser']['comma'].append(iToken)
            except KeyError:
                try:
                    dMap['parser']['comma'] = []
                    dMap['parser']['comma'].append(iToken)
                except KeyError:
                    dMap['parser'] = {}
                    dMap['parser']['comma'] = []
                    dMap['parser']['comma'].append(iToken)
            continue
        if sSub == 'open_parenthesis':
            try:
                if iToken not in dMap['parser']['open_parenthesis']:
                    dMap['parser']['open_parenthesis'].append(iToken)
            except KeyError:
                try:
                    dMap['parser']['open_parenthesis'] = []
                    dMap['parser']['open_parenthesis'].append(iToken)
                except KeyError:
                    dMap['parser'] = {}
                    dMap['parser']['open_parenthesis'] = []
                    dMap['parser']['open_parenthesis'].append(iToken)
            continue

    return New(dMap)


def build_default_map():
    dMap = {}
    return dMap
