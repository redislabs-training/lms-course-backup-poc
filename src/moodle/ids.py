class IDs:
    section_base = 100
    section = 101
    module_base = 500
    module = 501
    context = 10
    activity = 10
    
    def incr_section_id(self):
        self.section += 1
    
    def incr_module_id(self):
        self.module += 1
    
    def incr_context_id(self):
        self.context += 1
    
    def incr_activity_id(self):
        self.activity += 1