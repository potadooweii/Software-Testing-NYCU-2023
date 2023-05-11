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
    def run(self,fmt,n):
        simfd = self.state.posix.get_fd(sys.stdin.fileno()) 
        data, real_size = simfd.read_data(4)
        self.state.memory.store(n,data) 
        return 1

proj.hook_symbol('__isoc99_scanf', my_scanf(), replace=True)
simgr = proj.factory.simulation_manager(init_state)
simgr.explore(find=find_addr, avoid=avoid_addr)

if simgr.found:
    solution_state = simgr.found[0]
    ans = solution_state.posix.dumps(sys.stdin.fileno())

    int_vals = [
        int.from_bytes(ans[i*4:i*4+4], "little", signed=True)
        for i in range(15)
    ]
    
    with open('./solve_input', 'w') as f:
        for val in int_vals:
            print(val, file=f)
    
else:
    print('Failed')