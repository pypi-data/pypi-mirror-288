// Normalization of latin script letters
// Reference: http://www.unicode.org/Public/UCD/latest/ucd/Index.txt

package algo

var normalized = map[rune]rune{
	0x00E1: 'a', //  WITH ACUTE, LATIN SMALL LETTER
	0x0103: 'a', //  WITH BREVE, LATIN SMALL LETTER
	0x01CE: 'a', //  WITH CARON, LATIN SMALL LETTER
	0x00E2: 'a', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x00E4: 'a', //  WITH DIAERESIS, LATIN SMALL LETTER
	0x0227: 'a', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1EA1: 'a', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x0201: 'a', //  WITH DOUBLE GRAVE, LATIN SMALL LETTER
	0x00E0: 'a', //  WITH GRAVE, LATIN SMALL LETTER
	0x1EA3: 'a', //  WITH HOOK ABOVE, LATIN SMALL LETTER
	0x0203: 'a', //  WITH INVERTED BREVE, LATIN SMALL LETTER
	0x0101: 'a', //  WITH MACRON, LATIN SMALL LETTER
	0x0105: 'a', //  WITH OGONEK, LATIN SMALL LETTER
	0x1E9A: 'a', //  WITH RIGHT HALF RING, LATIN SMALL LETTER
	0x00E5: 'a', //  WITH RING ABOVE, LATIN SMALL LETTER
	0x1E01: 'a', //  WITH RING BELOW, LATIN SMALL LETTER
	0x00E3: 'a', //  WITH TILDE, LATIN SMALL LETTER
	0x0363: 'a', // , COMBINING LATIN SMALL LETTER
	0x0250: 'a', // , LATIN SMALL LETTER TURNED
	0x1E03: 'b', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1E05: 'b', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x0253: 'b', //  WITH HOOK, LATIN SMALL LETTER
	0x1E07: 'b', //  WITH LINE BELOW, LATIN SMALL LETTER
	0x0180: 'b', //  WITH STROKE, LATIN SMALL LETTER
	0x0183: 'b', //  WITH TOPBAR, LATIN SMALL LETTER
	0x0107: 'c', //  WITH ACUTE, LATIN SMALL LETTER
	0x010D: 'c', //  WITH CARON, LATIN SMALL LETTER
	0x00E7: 'c', //  WITH CEDILLA, LATIN SMALL LETTER
	0x0109: 'c', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x0255: 'c', //  WITH CURL, LATIN SMALL LETTER
	0x010B: 'c', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x0188: 'c', //  WITH HOOK, LATIN SMALL LETTER
	0x023C: 'c', //  WITH STROKE, LATIN SMALL LETTER
	0x0368: 'c', // , COMBINING LATIN SMALL LETTER
	0x0297: 'c', // , LATIN LETTER STRETCHED
	0x2184: 'c', // , LATIN SMALL LETTER REVERSED
	0x010F: 'd', //  WITH CARON, LATIN SMALL LETTER
	0x1E11: 'd', //  WITH CEDILLA, LATIN SMALL LETTER
	0x1E13: 'd', //  WITH CIRCUMFLEX BELOW, LATIN SMALL LETTER
	0x0221: 'd', //  WITH CURL, LATIN SMALL LETTER
	0x1E0B: 'd', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1E0D: 'd', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x0257: 'd', //  WITH HOOK, LATIN SMALL LETTER
	0x1E0F: 'd', //  WITH LINE BELOW, LATIN SMALL LETTER
	0x0111: 'd', //  WITH STROKE, LATIN SMALL LETTER
	0x0256: 'd', //  WITH TAIL, LATIN SMALL LETTER
	0x018C: 'd', //  WITH TOPBAR, LATIN SMALL LETTER
	0x0369: 'd', // , COMBINING LATIN SMALL LETTER
	0x00E9: 'e', //  WITH ACUTE, LATIN SMALL LETTER
	0x0115: 'e', //  WITH BREVE, LATIN SMALL LETTER
	0x011B: 'e', //  WITH CARON, LATIN SMALL LETTER
	0x0229: 'e', //  WITH CEDILLA, LATIN SMALL LETTER
	0x1E19: 'e', //  WITH CIRCUMFLEX BELOW, LATIN SMALL LETTER
	0x00EA: 'e', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x00EB: 'e', //  WITH DIAERESIS, LATIN SMALL LETTER
	0x0117: 'e', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1EB9: 'e', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x0205: 'e', //  WITH DOUBLE GRAVE, LATIN SMALL LETTER
	0x00E8: 'e', //  WITH GRAVE, LATIN SMALL LETTER
	0x1EBB: 'e', //  WITH HOOK ABOVE, LATIN SMALL LETTER
	0x025D: 'e', //  WITH HOOK, LATIN SMALL LETTER REVERSED OPEN
	0x0207: 'e', //  WITH INVERTED BREVE, LATIN SMALL LETTER
	0x0113: 'e', //  WITH MACRON, LATIN SMALL LETTER
	0x0119: 'e', //  WITH OGONEK, LATIN SMALL LETTER
	0x0247: 'e', //  WITH STROKE, LATIN SMALL LETTER
	0x1E1B: 'e', //  WITH TILDE BELOW, LATIN SMALL LETTER
	0x1EBD: 'e', //  WITH TILDE, LATIN SMALL LETTER
	0x0364: 'e', // , COMBINING LATIN SMALL LETTER
	0x029A: 'e', // , LATIN SMALL LETTER CLOSED OPEN
	0x025E: 'e', // , LATIN SMALL LETTER CLOSED REVERSED OPEN
	0x025B: 'e', // , LATIN SMALL LETTER OPEN
	0x0258: 'e', // , LATIN SMALL LETTER REVERSED
	0x025C: 'e', // , LATIN SMALL LETTER REVERSED OPEN
	0x01DD: 'e', // , LATIN SMALL LETTER TURNED
	0x1D08: 'e', // , LATIN SMALL LETTER TURNED OPEN
	0x1E1F: 'f', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x0192: 'f', //  WITH HOOK, LATIN SMALL LETTER
	0x01F5: 'g', //  WITH ACUTE, LATIN SMALL LETTER
	0x011F: 'g', //  WITH BREVE, LATIN SMALL LETTER
	0x01E7: 'g', //  WITH CARON, LATIN SMALL LETTER
	0x0123: 'g', //  WITH CEDILLA, LATIN SMALL LETTER
	0x011D: 'g', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x0121: 'g', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x0260: 'g', //  WITH HOOK, LATIN SMALL LETTER
	0x1E21: 'g', //  WITH MACRON, LATIN SMALL LETTER
	0x01E5: 'g', //  WITH STROKE, LATIN SMALL LETTER
	0x0261: 'g', // , LATIN SMALL LETTER SCRIPT
	0x1E2B: 'h', //  WITH BREVE BELOW, LATIN SMALL LETTER
	0x021F: 'h', //  WITH CARON, LATIN SMALL LETTER
	0x1E29: 'h', //  WITH CEDILLA, LATIN SMALL LETTER
	0x0125: 'h', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x1E27: 'h', //  WITH DIAERESIS, LATIN SMALL LETTER
	0x1E23: 'h', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1E25: 'h', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x02AE: 'h', //  WITH FISHHOOK, LATIN SMALL LETTER TURNED
	0x0266: 'h', //  WITH HOOK, LATIN SMALL LETTER
	0x1E96: 'h', //  WITH LINE BELOW, LATIN SMALL LETTER
	0x0127: 'h', //  WITH STROKE, LATIN SMALL LETTER
	0x036A: 'h', // , COMBINING LATIN SMALL LETTER
	0x0265: 'h', // , LATIN SMALL LETTER TURNED
	0x2095: 'h', // , LATIN SUBSCRIPT SMALL LETTER
	0x00ED: 'i', //  WITH ACUTE, LATIN SMALL LETTER
	0x012D: 'i', //  WITH BREVE, LATIN SMALL LETTER
	0x01D0: 'i', //  WITH CARON, LATIN SMALL LETTER
	0x00EE: 'i', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x00EF: 'i', //  WITH DIAERESIS, LATIN SMALL LETTER
	0x1ECB: 'i', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x0209: 'i', //  WITH DOUBLE GRAVE, LATIN SMALL LETTER
	0x00EC: 'i', //  WITH GRAVE, LATIN SMALL LETTER
	0x1EC9: 'i', //  WITH HOOK ABOVE, LATIN SMALL LETTER
	0x020B: 'i', //  WITH INVERTED BREVE, LATIN SMALL LETTER
	0x012B: 'i', //  WITH MACRON, LATIN SMALL LETTER
	0x012F: 'i', //  WITH OGONEK, LATIN SMALL LETTER
	0x0268: 'i', //  WITH STROKE, LATIN SMALL LETTER
	0x1E2D: 'i', //  WITH TILDE BELOW, LATIN SMALL LETTER
	0x0129: 'i', //  WITH TILDE, LATIN SMALL LETTER
	0x0365: 'i', // , COMBINING LATIN SMALL LETTER
	0x0131: 'i', // , LATIN SMALL LETTER DOTLESS
	0x1D09: 'i', // , LATIN SMALL LETTER TURNED
	0x1D62: 'i', // , LATIN SUBSCRIPT SMALL LETTER
	0x2071: 'i', // , SUPERSCRIPT LATIN SMALL LETTER
	0x01F0: 'j', //  WITH CARON, LATIN SMALL LETTER
	0x0135: 'j', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x029D: 'j', //  WITH CROSSED-TAIL, LATIN SMALL LETTER
	0x0249: 'j', //  WITH STROKE, LATIN SMALL LETTER
	0x025F: 'j', //  WITH STROKE, LATIN SMALL LETTER DOTLESS
	0x0237: 'j', // , LATIN SMALL LETTER DOTLESS
	0x1E31: 'k', //  WITH ACUTE, LATIN SMALL LETTER
	0x01E9: 'k', //  WITH CARON, LATIN SMALL LETTER
	0x0137: 'k', //  WITH CEDILLA, LATIN SMALL LETTER
	0x1E33: 'k', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x0199: 'k', //  WITH HOOK, LATIN SMALL LETTER
	0x1E35: 'k', //  WITH LINE BELOW, LATIN SMALL LETTER
	0x029E: 'k', // , LATIN SMALL LETTER TURNED
	0x2096: 'k', // , LATIN SUBSCRIPT SMALL LETTER
	0x013A: 'l', //  WITH ACUTE, LATIN SMALL LETTER
	0x019A: 'l', //  WITH BAR, LATIN SMALL LETTER
	0x026C: 'l', //  WITH BELT, LATIN SMALL LETTER
	0x013E: 'l', //  WITH CARON, LATIN SMALL LETTER
	0x013C: 'l', //  WITH CEDILLA, LATIN SMALL LETTER
	0x1E3D: 'l', //  WITH CIRCUMFLEX BELOW, LATIN SMALL LETTER
	0x0234: 'l', //  WITH CURL, LATIN SMALL LETTER
	0x1E37: 'l', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x1E3B: 'l', //  WITH LINE BELOW, LATIN SMALL LETTER
	0x0140: 'l', //  WITH MIDDLE DOT, LATIN SMALL LETTER
	0x026B: 'l', //  WITH MIDDLE TILDE, LATIN SMALL LETTER
	0x026D: 'l', //  WITH RETROFLEX HOOK, LATIN SMALL LETTER
	0x0142: 'l', //  WITH STROKE, LATIN SMALL LETTER
	0x2097: 'l', // , LATIN SUBSCRIPT SMALL LETTER
	0x1E3F: 'm', //  WITH ACUTE, LATIN SMALL LETTER
	0x1E41: 'm', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1E43: 'm', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x0271: 'm', //  WITH HOOK, LATIN SMALL LETTER
	0x0270: 'm', //  WITH LONG LEG, LATIN SMALL LETTER TURNED
	0x036B: 'm', // , COMBINING LATIN SMALL LETTER
	0x1D1F: 'm', // , LATIN SMALL LETTER SIDEWAYS TURNED
	0x026F: 'm', // , LATIN SMALL LETTER TURNED
	0x2098: 'm', // , LATIN SUBSCRIPT SMALL LETTER
	0x0144: 'n', //  WITH ACUTE, LATIN SMALL LETTER
	0x0148: 'n', //  WITH CARON, LATIN SMALL LETTER
	0x0146: 'n', //  WITH CEDILLA, LATIN SMALL LETTER
	0x1E4B: 'n', //  WITH CIRCUMFLEX BELOW, LATIN SMALL LETTER
	0x0235: 'n', //  WITH CURL, LATIN SMALL LETTER
	0x1E45: 'n', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1E47: 'n', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x01F9: 'n', //  WITH GRAVE, LATIN SMALL LETTER
	0x0272: 'n', //  WITH LEFT HOOK, LATIN SMALL LETTER
	0x1E49: 'n', //  WITH LINE BELOW, LATIN SMALL LETTER
	0x019E: 'n', //  WITH LONG RIGHT LEG, LATIN SMALL LETTER
	0x0273: 'n', //  WITH RETROFLEX HOOK, LATIN SMALL LETTER
	0x00F1: 'n', //  WITH TILDE, LATIN SMALL LETTER
	0x2099: 'n', // , LATIN SUBSCRIPT SMALL LETTER
	0x00F3: 'o', //  WITH ACUTE, LATIN SMALL LETTER
	0x014F: 'o', //  WITH BREVE, LATIN SMALL LETTER
	0x01D2: 'o', //  WITH CARON, LATIN SMALL LETTER
	0x00F4: 'o', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x00F6: 'o', //  WITH DIAERESIS, LATIN SMALL LETTER
	0x022F: 'o', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1ECD: 'o', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x0151: 'o', //  WITH DOUBLE ACUTE, LATIN SMALL LETTER
	0x020D: 'o', //  WITH DOUBLE GRAVE, LATIN SMALL LETTER
	0x00F2: 'o', //  WITH GRAVE, LATIN SMALL LETTER
	0x1ECF: 'o', //  WITH HOOK ABOVE, LATIN SMALL LETTER
	0x01A1: 'o', //  WITH HORN, LATIN SMALL LETTER
	0x020F: 'o', //  WITH INVERTED BREVE, LATIN SMALL LETTER
	0x014D: 'o', //  WITH MACRON, LATIN SMALL LETTER
	0x01EB: 'o', //  WITH OGONEK, LATIN SMALL LETTER
	0x00F8: 'o', //  WITH STROKE, LATIN SMALL LETTER
	0x1D13: 'o', //  WITH STROKE, LATIN SMALL LETTER SIDEWAYS
	0x00F5: 'o', //  WITH TILDE, LATIN SMALL LETTER
	0x0366: 'o', // , COMBINING LATIN SMALL LETTER
	0x0275: 'o', // , LATIN SMALL LETTER BARRED
	0x1D17: 'o', // , LATIN SMALL LETTER BOTTOM HALF
	0x0254: 'o', // , LATIN SMALL LETTER OPEN
	0x1D11: 'o', // , LATIN SMALL LETTER SIDEWAYS
	0x1D12: 'o', // , LATIN SMALL LETTER SIDEWAYS OPEN
	0x1D16: 'o', // , LATIN SMALL LETTER TOP HALF
	0x1E55: 'p', //  WITH ACUTE, LATIN SMALL LETTER
	0x1E57: 'p', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x01A5: 'p', //  WITH HOOK, LATIN SMALL LETTER
	0x209A: 'p', // , LATIN SUBSCRIPT SMALL LETTER
	0x024B: 'q', //  WITH HOOK TAIL, LATIN SMALL LETTER
	0x02A0: 'q', //  WITH HOOK, LATIN SMALL LETTER
	0x0155: 'r', //  WITH ACUTE, LATIN SMALL LETTER
	0x0159: 'r', //  WITH CARON, LATIN SMALL LETTER
	0x0157: 'r', //  WITH CEDILLA, LATIN SMALL LETTER
	0x1E59: 'r', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1E5B: 'r', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x0211: 'r', //  WITH DOUBLE GRAVE, LATIN SMALL LETTER
	0x027E: 'r', //  WITH FISHHOOK, LATIN SMALL LETTER
	0x027F: 'r', //  WITH FISHHOOK, LATIN SMALL LETTER REVERSED
	0x027B: 'r', //  WITH HOOK, LATIN SMALL LETTER TURNED
	0x0213: 'r', //  WITH INVERTED BREVE, LATIN SMALL LETTER
	0x1E5F: 'r', //  WITH LINE BELOW, LATIN SMALL LETTER
	0x027C: 'r', //  WITH LONG LEG, LATIN SMALL LETTER
	0x027A: 'r', //  WITH LONG LEG, LATIN SMALL LETTER TURNED
	0x024D: 'r', //  WITH STROKE, LATIN SMALL LETTER
	0x027D: 'r', //  WITH TAIL, LATIN SMALL LETTER
	0x036C: 'r', // , COMBINING LATIN SMALL LETTER
	0x0279: 'r', // , LATIN SMALL LETTER TURNED
	0x1D63: 'r', // , LATIN SUBSCRIPT SMALL LETTER
	0x015B: 's', //  WITH ACUTE, LATIN SMALL LETTER
	0x0161: 's', //  WITH CARON, LATIN SMALL LETTER
	0x015F: 's', //  WITH CEDILLA, LATIN SMALL LETTER
	0x015D: 's', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x0219: 's', //  WITH COMMA BELOW, LATIN SMALL LETTER
	0x1E61: 's', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1E9B: 's', //  WITH DOT ABOVE, LATIN SMALL LETTER LONG
	0x1E63: 's', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x0282: 's', //  WITH HOOK, LATIN SMALL LETTER
	0x023F: 's', //  WITH SWASH TAIL, LATIN SMALL LETTER
	0x017F: 's', // , LATIN SMALL LETTER LONG
	0x00DF: 's', // , LATIN SMALL LETTER SHARP
	0x209B: 's', // , LATIN SUBSCRIPT SMALL LETTER
	0x0165: 't', //  WITH CARON, LATIN SMALL LETTER
	0x0163: 't', //  WITH CEDILLA, LATIN SMALL LETTER
	0x1E71: 't', //  WITH CIRCUMFLEX BELOW, LATIN SMALL LETTER
	0x021B: 't', //  WITH COMMA BELOW, LATIN SMALL LETTER
	0x0236: 't', //  WITH CURL, LATIN SMALL LETTER
	0x1E97: 't', //  WITH DIAERESIS, LATIN SMALL LETTER
	0x1E6B: 't', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1E6D: 't', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x01AD: 't', //  WITH HOOK, LATIN SMALL LETTER
	0x1E6F: 't', //  WITH LINE BELOW, LATIN SMALL LETTER
	0x01AB: 't', //  WITH PALATAL HOOK, LATIN SMALL LETTER
	0x0288: 't', //  WITH RETROFLEX HOOK, LATIN SMALL LETTER
	0x0167: 't', //  WITH STROKE, LATIN SMALL LETTER
	0x036D: 't', // , COMBINING LATIN SMALL LETTER
	0x0287: 't', // , LATIN SMALL LETTER TURNED
	0x209C: 't', // , LATIN SUBSCRIPT SMALL LETTER
	0x0289: 'u', //  BAR, LATIN SMALL LETTER
	0x00FA: 'u', //  WITH ACUTE, LATIN SMALL LETTER
	0x016D: 'u', //  WITH BREVE, LATIN SMALL LETTER
	0x01D4: 'u', //  WITH CARON, LATIN SMALL LETTER
	0x1E77: 'u', //  WITH CIRCUMFLEX BELOW, LATIN SMALL LETTER
	0x00FB: 'u', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x1E73: 'u', //  WITH DIAERESIS BELOW, LATIN SMALL LETTER
	0x00FC: 'u', //  WITH DIAERESIS, LATIN SMALL LETTER
	0x1EE5: 'u', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x0171: 'u', //  WITH DOUBLE ACUTE, LATIN SMALL LETTER
	0x0215: 'u', //  WITH DOUBLE GRAVE, LATIN SMALL LETTER
	0x00F9: 'u', //  WITH GRAVE, LATIN SMALL LETTER
	0x1EE7: 'u', //  WITH HOOK ABOVE, LATIN SMALL LETTER
	0x01B0: 'u', //  WITH HORN, LATIN SMALL LETTER
	0x0217: 'u', //  WITH INVERTED BREVE, LATIN SMALL LETTER
	0x016B: 'u', //  WITH MACRON, LATIN SMALL LETTER
	0x0173: 'u', //  WITH OGONEK, LATIN SMALL LETTER
	0x016F: 'u', //  WITH RING ABOVE, LATIN SMALL LETTER
	0x1E75: 'u', //  WITH TILDE BELOW, LATIN SMALL LETTER
	0x0169: 'u', //  WITH TILDE, LATIN SMALL LETTER
	0x0367: 'u', // , COMBINING LATIN SMALL LETTER
	0x1D1D: 'u', // , LATIN SMALL LETTER SIDEWAYS
	0x1D1E: 'u', // , LATIN SMALL LETTER SIDEWAYS DIAERESIZED
	0x1D64: 'u', // , LATIN SUBSCRIPT SMALL LETTER
	0x1E7F: 'v', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x028B: 'v', //  WITH HOOK, LATIN SMALL LETTER
	0x1E7D: 'v', //  WITH TILDE, LATIN SMALL LETTER
	0x036E: 'v', // , COMBINING LATIN SMALL LETTER
	0x028C: 'v', // , LATIN SMALL LETTER TURNED
	0x1D65: 'v', // , LATIN SUBSCRIPT SMALL LETTER
	0x1E83: 'w', //  WITH ACUTE, LATIN SMALL LETTER
	0x0175: 'w', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x1E85: 'w', //  WITH DIAERESIS, LATIN SMALL LETTER
	0x1E87: 'w', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1E89: 'w', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x1E81: 'w', //  WITH GRAVE, LATIN SMALL LETTER
	0x1E98: 'w', //  WITH RING ABOVE, LATIN SMALL LETTER
	0x028D: 'w', // , LATIN SMALL LETTER TURNED
	0x1E8D: 'x', //  WITH DIAERESIS, LATIN SMALL LETTER
	0x1E8B: 'x', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x036F: 'x', // , COMBINING LATIN SMALL LETTER
	0x00FD: 'y', //  WITH ACUTE, LATIN SMALL LETTER
	0x0177: 'y', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x00FF: 'y', //  WITH DIAERESIS, LATIN SMALL LETTER
	0x1E8F: 'y', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1EF5: 'y', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x1EF3: 'y', //  WITH GRAVE, LATIN SMALL LETTER
	0x1EF7: 'y', //  WITH HOOK ABOVE, LATIN SMALL LETTER
	0x01B4: 'y', //  WITH HOOK, LATIN SMALL LETTER
	0x0233: 'y', //  WITH MACRON, LATIN SMALL LETTER
	0x1E99: 'y', //  WITH RING ABOVE, LATIN SMALL LETTER
	0x024F: 'y', //  WITH STROKE, LATIN SMALL LETTER
	0x1EF9: 'y', //  WITH TILDE, LATIN SMALL LETTER
	0x028E: 'y', // , LATIN SMALL LETTER TURNED
	0x017A: 'z', //  WITH ACUTE, LATIN SMALL LETTER
	0x017E: 'z', //  WITH CARON, LATIN SMALL LETTER
	0x1E91: 'z', //  WITH CIRCUMFLEX, LATIN SMALL LETTER
	0x0291: 'z', //  WITH CURL, LATIN SMALL LETTER
	0x017C: 'z', //  WITH DOT ABOVE, LATIN SMALL LETTER
	0x1E93: 'z', //  WITH DOT BELOW, LATIN SMALL LETTER
	0x0225: 'z', //  WITH HOOK, LATIN SMALL LETTER
	0x1E95: 'z', //  WITH LINE BELOW, LATIN SMALL LETTER
	0x0290: 'z', //  WITH RETROFLEX HOOK, LATIN SMALL LETTER
	0x01B6: 'z', //  WITH STROKE, LATIN SMALL LETTER
	0x0240: 'z', //  WITH SWASH TAIL, LATIN SMALL LETTER
	0x0251: 'a', // , latin small letter script
	0x00C1: 'A', //  WITH ACUTE, LATIN CAPITAL LETTER
	0x00C2: 'A', //  WITH CIRCUMFLEX, LATIN CAPITAL LETTER
	0x00C4: 'A', //  WITH DIAERESIS, LATIN CAPITAL LETTER
	0x00C0: 'A', //  WITH GRAVE, LATIN CAPITAL LETTER
	0x00C5: 'A', //  WITH RING ABOVE, LATIN CAPITAL LETTER
	0x023A: 'A', //  WITH STROKE, LATIN CAPITAL LETTER
	0x00C3: 'A', //  WITH TILDE, LATIN CAPITAL LETTER
	0x1D00: 'A', // , LATIN LETTER SMALL CAPITAL
	0x0181: 'B', //  WITH HOOK, LATIN CAPITAL LETTER
	0x0243: 'B', //  WITH STROKE, LATIN CAPITAL LETTER
	0x0299: 'B', // , LATIN LETTER SMALL CAPITAL
	0x1D03: 'B', // , LATIN LETTER SMALL CAPITAL BARRED
	0x00C7: 'C', //  WITH CEDILLA, LATIN CAPITAL LETTER
	0x023B: 'C', //  WITH STROKE, LATIN CAPITAL LETTER
	0x1D04: 'C', // , LATIN LETTER SMALL CAPITAL
	0x018A: 'D', //  WITH HOOK, LATIN CAPITAL LETTER
	0x0189: 'D', // , LATIN CAPITAL LETTER AFRICAN
	0x1D05: 'D', // , LATIN LETTER SMALL CAPITAL
	0x00C9: 'E', //  WITH ACUTE, LATIN CAPITAL LETTER
	0x00CA: 'E', //  WITH CIRCUMFLEX, LATIN CAPITAL LETTER
	0x00CB: 'E', //  WITH DIAERESIS, LATIN CAPITAL LETTER
	0x00C8: 'E', //  WITH GRAVE, LATIN CAPITAL LETTER
	0x0246: 'E', //  WITH STROKE, LATIN CAPITAL LETTER
	0x0190: 'E', // , LATIN CAPITAL LETTER OPEN
	0x018E: 'E', // , LATIN CAPITAL LETTER REVERSED
	0x1D07: 'E', // , LATIN LETTER SMALL CAPITAL
	0x0193: 'G', //  WITH HOOK, LATIN CAPITAL LETTER
	0x029B: 'G', //  WITH HOOK, LATIN LETTER SMALL CAPITAL
	0x0262: 'G', // , LATIN LETTER SMALL CAPITAL
	0x029C: 'H', // , LATIN LETTER SMALL CAPITAL
	0x00CD: 'I', //  WITH ACUTE, LATIN CAPITAL LETTER
	0x00CE: 'I', //  WITH CIRCUMFLEX, LATIN CAPITAL LETTER
	0x00CF: 'I', //  WITH DIAERESIS, LATIN CAPITAL LETTER
	0x0130: 'I', //  WITH DOT ABOVE, LATIN CAPITAL LETTER
	0x00CC: 'I', //  WITH GRAVE, LATIN CAPITAL LETTER
	0x0197: 'I', //  WITH STROKE, LATIN CAPITAL LETTER
	0x026A: 'I', // , LATIN LETTER SMALL CAPITAL
	0x0248: 'J', //  WITH STROKE, LATIN CAPITAL LETTER
	0x1D0A: 'J', // , LATIN LETTER SMALL CAPITAL
	0x1D0B: 'K', // , LATIN LETTER SMALL CAPITAL
	0x023D: 'L', //  WITH BAR, LATIN CAPITAL LETTER
	0x1D0C: 'L', //  WITH STROKE, LATIN LETTER SMALL CAPITAL
	0x029F: 'L', // , LATIN LETTER SMALL CAPITAL
	0x019C: 'M', // , LATIN CAPITAL LETTER TURNED
	0x1D0D: 'M', // , LATIN LETTER SMALL CAPITAL
	0x019D: 'N', //  WITH LEFT HOOK, LATIN CAPITAL LETTER
	0x0220: 'N', //  WITH LONG RIGHT LEG, LATIN CAPITAL LETTER
	0x00D1: 'N', //  WITH TILDE, LATIN CAPITAL LETTER
	0x0274: 'N', // , LATIN LETTER SMALL CAPITAL
	0x1D0E: 'N', // , LATIN LETTER SMALL CAPITAL REVERSED
	0x00D3: 'O', //  WITH ACUTE, LATIN CAPITAL LETTER
	0x00D4: 'O', //  WITH CIRCUMFLEX, LATIN CAPITAL LETTER
	0x00D6: 'O', //  WITH DIAERESIS, LATIN CAPITAL LETTER
	0x00D2: 'O', //  WITH GRAVE, LATIN CAPITAL LETTER
	0x019F: 'O', //  WITH MIDDLE TILDE, LATIN CAPITAL LETTER
	0x00D8: 'O', //  WITH STROKE, LATIN CAPITAL LETTER
	0x00D5: 'O', //  WITH TILDE, LATIN CAPITAL LETTER
	0x0186: 'O', // , LATIN CAPITAL LETTER OPEN
	0x1D0F: 'O', // , LATIN LETTER SMALL CAPITAL
	0x1D10: 'O', // , LATIN LETTER SMALL CAPITAL OPEN
	0x1D18: 'P', // , LATIN LETTER SMALL CAPITAL
	0x024A: 'Q', //  WITH HOOK TAIL, LATIN CAPITAL LETTER SMALL
	0x024C: 'R', //  WITH STROKE, LATIN CAPITAL LETTER
	0x0280: 'R', // , LATIN LETTER SMALL CAPITAL
	0x0281: 'R', // , LATIN LETTER SMALL CAPITAL INVERTED
	0x1D19: 'R', // , LATIN LETTER SMALL CAPITAL REVERSED
	0x1D1A: 'R', // , LATIN LETTER SMALL CAPITAL TURNED
	0x023E: 'T', //  WITH DIAGONAL STROKE, LATIN CAPITAL LETTER
	0x01AE: 'T', //  WITH RETROFLEX HOOK, LATIN CAPITAL LETTER
	0x1D1B: 'T', // , LATIN LETTER SMALL CAPITAL
	0x0244: 'U', //  BAR, LATIN CAPITAL LETTER
	0x00DA: 'U', //  WITH ACUTE, LATIN CAPITAL LETTER
	0x00DB: 'U', //  WITH CIRCUMFLEX, LATIN CAPITAL LETTER
	0x00DC: 'U', //  WITH DIAERESIS, LATIN CAPITAL LETTER
	0x00D9: 'U', //  WITH GRAVE, LATIN CAPITAL LETTER
	0x1D1C: 'U', // , LATIN LETTER SMALL CAPITAL
	0x01B2: 'V', //  WITH HOOK, LATIN CAPITAL LETTER
	0x0245: 'V', // , LATIN CAPITAL LETTER TURNED
	0x1D20: 'V', // , LATIN LETTER SMALL CAPITAL
	0x1D21: 'W', // , LATIN LETTER SMALL CAPITAL
	0x00DD: 'Y', //  WITH ACUTE, LATIN CAPITAL LETTER
	0x0178: 'Y', //  WITH DIAERESIS, LATIN CAPITAL LETTER
	0x024E: 'Y', //  WITH STROKE, LATIN CAPITAL LETTER
	0x028F: 'Y', // , LATIN LETTER SMALL CAPITAL
	0x1D22: 'Z', // , LATIN LETTER SMALL CAPITAL

	'Ắ': 'A',
	'Ấ': 'A',
	'Ằ': 'A',
	'Ầ': 'A',
	'Ẳ': 'A',
	'Ẩ': 'A',
	'Ẵ': 'A',
	'Ẫ': 'A',
	'Ặ': 'A',
	'Ậ': 'A',

	'ắ': 'a',
	'ấ': 'a',
	'ằ': 'a',
	'ầ': 'a',
	'ẳ': 'a',
	'ẩ': 'a',
	'ẵ': 'a',
	'ẫ': 'a',
	'ặ': 'a',
	'ậ': 'a',

	'Ế': 'E',
	'Ề': 'E',
	'Ể': 'E',
	'Ễ': 'E',
	'Ệ': 'E',

	'ế': 'e',
	'ề': 'e',
	'ể': 'e',
	'ễ': 'e',
	'ệ': 'e',

	'Ố': 'O',
	'Ớ': 'O',
	'Ồ': 'O',
	'Ờ': 'O',
	'Ổ': 'O',
	'Ở': 'O',
	'Ỗ': 'O',
	'Ỡ': 'O',
	'Ộ': 'O',
	'Ợ': 'O',

	'ố': 'o',
	'ớ': 'o',
	'ồ': 'o',
	'ờ': 'o',
	'ổ': 'o',
	'ở': 'o',
	'ỗ': 'o',
	'ỡ': 'o',
	'ộ': 'o',
	'ợ': 'o',

	'Ứ': 'U',
	'Ừ': 'U',
	'Ử': 'U',
	'Ữ': 'U',
	'Ự': 'U',

	'ứ': 'u',
	'ừ': 'u',
	'ử': 'u',
	'ữ': 'u',
	'ự': 'u',
}

// NormalizeRunes normalizes latin script letters
func NormalizeRunes(runes []rune) []rune {
	ret := make([]rune, len(runes))
	copy(ret, runes)
	for idx, r := range runes {
		if r < 0x00C0 || r > 0x2184 {
			continue
		}
		n := normalized[r]
		if n > 0 {
			ret[idx] = normalized[r]
		}
	}
	return ret
}
