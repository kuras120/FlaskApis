import time
import shlex
import logging
import subprocess


def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


def run_algorithm(algorithm_path, file_path):
    try:
        logging.getLogger('logger').info('Processing started')
        data = subprocess.Popen(shlex.split('python ' + algorithm_path + ' ' + file_path),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        solution = ''
        while True:
            output = data.stdout.readline().decode('utf-8').strip()
            if output == '' and data.poll() is not None:
                break
            if output:
                if 'Name' in output or 'Processing time' in output or 'Output' in output:
                    solution += output + '<br>'
                    logging.getLogger('logger').info(output)
                print(output)

        if data.returncode == 0:
            logging.getLogger('logger').info('Processing completed')
            return solution
        else:
            logging.getLogger('error_logger').error(data.stderr.read().decode('utf-8'))
            return data.returncode
    except Exception as e:
        logging.getLogger('error_logger').exception(e)
        raise Exception(e)
