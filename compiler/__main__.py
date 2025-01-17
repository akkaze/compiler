from compiler.utils.libfunction import LibFunction, LIB_PREFIX
from compiler.entity import *
from compiler.parser import *
from compiler.options import *
from compiler.utils import *
from compiler.typ.global_types import *
from compiler.backend import Translator
from compiler.backend import Allocator
from compiler.backend import NaiveAllocator
from compiler.backend import RegisterConfig
from compiler.backend import DataFlowAnalyzer
from compiler.backend import ControlFlowAnalyzer
from compiler.backend import InstructionEmmiter
from compiler.backend import IRBuilder
from compiler.entity.variable_entity import VariableEntity
from compiler.frontend.symbol_resolver import SymbolResolver
from compiler.frontend.ast_builder import ASTBuilder
from antlr4 import *
from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream
import sys
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(message)s')


def get_library():
    ret = []
    ret.append(LibFunction(void_type, 'print', [string_type], 'printf').entity)
    ret.append(LibFunction(void_type, 'println', [string_type],
                           'puts').entity)
    ret.append(LibFunction(string_type, 'getString', None).entity)
    ret.append(LibFunction(integer_type, 'getInt', None).entity)
    ret.append(LibFunction(string_type, 'toString', [integer_type]).entity)
    ret.append(LibFunction(integer_type, LIB_PREFIX + 'printInt',
                           [string_type], LIB_PREFIX + 'printInt').entity)
    ret.append(LibFunction(integer_type, LIB_PREFIX + 'printlnInt',
                           [string_type], LIB_PREFIX + 'printlnInt').entity)
    ret.append(LibFunction(integer_type, LIB_PREFIX + 'malloc',
                           [integer_type],  'malloc').entity)
    ret.append(VariableEntity(None, null_type, 'null', None))
    return ret


def print_instructions(function_entities):
    for function_entity in function_entities:
        logging.info("==== " + function_entity.name + " ====")
        if not function_entity.bbs:
            continue
        for basic_block in function_entity.bbs:
            for ins in basic_block.ins:
                logging.info(str(ins))


def total_num_ins(function_entities):
    num_ins = 0
    for function_entity in function_entities:
        if not function_entity.bbs:
            continue
        for basic_block in function_entity.bbs:
            num_ins += len(basic_block.ins)
    return num_ins


def compile(in_file, out_file):
    global options
    input = InputStream(in_file.read())
    lexer = MalicLexer(input)
    tokens = CommonTokenStream(lexer)
    parser = MalicParser(tokens)
    tree = parser.compilationUnit()
    walker = ParseTreeWalker()
    listener = ASTBuilder()
    walker.walk(listener, tree)
    ast = listener.ast
    ast.load_library(get_library())
    initialize_builtin_type()
    ast.resolve_symbol()
    ast.check_type()
    if options.enable_output_irrelevant_elimination:
        ast.eliminate_output_irrelevant_node()

    if len(ast.scope.all_local_variables()) > 32:
        options.enable_global_register_allocation = False
    ir_builder = IRBuilder(ast)
    ir_builder.generate_ir()
    emmiter = InstructionEmmiter(ir_builder)
    emmiter.emit()
    cfg_builder = ControlFlowAnalyzer(emmiter)
    cfg_builder.build_controlflow()

    dataflow_analyzer = DataFlowAnalyzer(emmiter)
    dataflow_analyzer.optimize()
    if options.print_instruction:
        print_instructions(emmiter.function_entities)
    if total_num_ins(emmiter.function_entities) > 1000:
        options.enable_global_register_allocation = False

    register_config = RegisterConfig()

    allocator = None
    if options.enable_global_register_allocation:
        allocator = Allocator(emmiter, register_config)
    else:
        allocator = NaiveAllocator(emmiter, register_config)
    allocator.allocate()

    translator = Translator(emmiter, register_config)
    asm = translator.translate()

    for s in asm:
        out_file.write(s + '\n')


def print_usage():
    pass


def parse_options(args):
    global options
    assert isinstance(args, list)
    for i in range(len(args)):
        if args[i] == '--print-ins':
            options.print_instruction = True
            break
        elif args[i] == '--print-remove':
            options.print_remove = True
            break
        elif args[i] == '-in':
            if (i + 1 >= len(args)):
                logging.info('invalid argument for input file, \
                                use default setting instead')
            else:
                options.in_file = args[i + 1]
                i = i + 1
        elif args[i] == '-out':
            if (i + 1 >= len(args)):
                logging.info('invalid argument for output file, \
                                use default setting instead')
            else:
                options.out_file = args[i + 1]
                i = i + 1
        elif args[i] == '-help':
            print_usage()

        if options.in_file == None or options.out_file == None:
            print_usage()


def main():
    global options
    parse_options(sys.argv)
    in_file = open(options.in_file, 'r')
    out_file = open(options.out_file, 'w')
    compile(in_file, out_file)
    in_file.close()
    out_file.close()


if __name__ == '__main__':
    main()
