from datetime import datetime

class ErrorHandler:
    def __init__(self):
        self.error_log = []
    
    def handle_error(self, error, context):
        """处理错误并记录"""
        error_info = {
            'time': datetime.now(),
            'error': str(error),
            'context': context
        }
        self.error_log.append(error_info)
        self.show_error_dialog(error_info) 