# An implementation of hello-gbdx.py using the GbdxTaskInterface

'''
This script creates an instance of the HelloGbdxTask class, which inherits from the
GBDXTaskInterface class, and runs its invoke() function.  You can think of
GBDXTaskInterface as a GBDX task python template. It contains pre-built functions to
read the values of the task ports and clean-down code to record the status of the task
('success' or 'fail') when the 'with' statement goes out of scope. The invoke()
function implements the task functionality. In this case, invoke():
- reads the values of the 'data' and 'message' ports ('data' is a directory and
    'message' is a string , which are the only acceptable GBDX types at the time
    of this writing
- writes the contents of 'data' and a message in out.txt, which is saved in
    output_dir.
'''

import os
from gbdx_task_interface import GbdxTaskInterface

class HelloGbdxTask(GbdxTaskInterface):

    def invoke(self):

        # Get inputs
        input_dir = self.get_input_data_port('data_in')
        message = self.get_input_string_port('message', default='No message!')

        # Get output
        output_dir = self.get_output_data_port('data_out')
        os.makedirs(output_dir)

        # Write message to file
        with open(os.path.join(output_dir, 'out.txt'), 'w') as f:
            input_contents = ','.join(os.listdir(input_dir))
            f.write(input_contents + '\n')
            f.write(message)


if __name__ == "__main__":
    with HelloGbdxTask() as task:
        task.invoke()
