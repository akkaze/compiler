class Options(object):
    # constants
    REG_SIZE = 8
    STACK_VAR_ALIGNMENT_SIZE = 4
    CLASS_MEMBER_ALIGNMENT_SIZE = 4
    FRAME_ALIGNMENT_SIZE = 16
    
    # io
    in_file = None
    out_file = None
    
    # debug
    print_remove_info = True
    print_inline_info = True
    print_irrelevant_mark_info = False
    print_instruction = True
    print_basic_blocks = False
    
    print_naive_allocator_info = True
    print_global_allocation_info = False
    
    # optimization
    enable_global_register_allocation = True
    
    
    enable_cjump_optimization = True
    enable_controlflow_optimization = True
    # ast_ir level
    enable_function_inline = False
    enable_self_inline = False
    enable_instruction_selection = False
    enable_print_expanding = True 
    enable_leaf_function_optimization = False
    enable_common_assign_elimination = False
    enable_common_expression_elimination = False
    enable_constant_propagation = False
    enable_deadcode_elimination = False
    #
    enable_output_irrelevant_elimination = False
    print_irrelevant_mark_info = False
options = Options()
