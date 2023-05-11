import angr
import sys
import struct
import claripy

main_addr = 0x4011a9
find_addr = 0x401371
avoid_addr = 0x40134d

proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})
init_state = proj.factory.blank_state(addr=main_addr)

class my_scanf(angr.SimProcedure):
    def run(self, fmt, n):
        scanf = claripy.BVS('scanf', 32)

        scanf_addr = n
        self.state.memory.store(scanf_addr, scanf, endness=proj.arch.memory_endness)

        try:
            self.state.globals['solutions'].append(scanf)
        except:
            self.state.globals['solutions'] = []
            self.state.globals['solutions'].append(scanf)

        return 1

proj.hook_symbol('__isoc99_scanf', my_scanf(), replace=True)
simgr = proj.factory.simulation_manager(init_state)
simgr.explore(find=find_addr, avoid=avoid_addr)

if simgr.found:
    solution_state = simgr.found[0]
    ans = solution_state.posix.dumps(sys.stdin.fileno())

    stored_solutions = solution_state.globals['solutions']
    solution = ' '.join(map(str, map(solution_state.solver.eval, stored_solutions)))
    print(solution)
    
    with open('./solve_input', 'w') as f:
        print(solution, file=f)
    
else:
    print('Failed')