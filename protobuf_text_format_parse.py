from pyparsing import pyparsing_common as ppc
import pyparsing as pp

LBRACE = pp.Suppress("{")
RBRACE = pp.Suppress("}")
COLON = pp.Suppress(":")

identifier = ppc.identifier

STRING = pp.dblQuotedString().setParseAction(pp.removeQuotes)
NUMBER = ppc.number().setName("ProtoNumber")

PROTO_OBJECT = pp.Forward().setName("ProtoObject")
PROTO_MEMBER = pp.Forward().setName("ProtoMember")
PROTO_PAIR = pp.Forward().setName("ProtoPair")
PROTO_VALUE = pp.Forward().setName("ProtoValue")
PROTO_ROOT_OBJECT = pp.Forward().setName("ProtoRootObject")

PROTO_VALUE << (STRING | NUMBER)
PROTO_PAIR << (identifier + COLON + PROTO_VALUE)
PROTO_MEMBER << pp.Group(PROTO_PAIR | PROTO_OBJECT, aslist=True)
PROTO_MEMBERS = pp.delimitedList(PROTO_MEMBER, delim=pp.empty)
PROTO_OBJECT << (identifier + LBRACE + PROTO_MEMBERS + RBRACE) 
PROTO_ROOT_OBJECT << (identifier + LBRACE + PROTO_MEMBERS + RBRACE) 
PROTO = pp.delimitedList(PROTO_ROOT_OBJECT, delim=pp.empty)

sample = """
money { currency: "usd" amount { integer_part: "1" fractional_part: "20"} style: 1 }
measure { decimal { integer_part: "100" } units: "kilometer per hour" }
"""

result = PROTO.parse_string(sample)
print(result.as_list())