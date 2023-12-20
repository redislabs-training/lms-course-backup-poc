import logging

class IDs:
    course = 10
    section_base = 100
    section = 101
    module_base = 500
    module = 501
    context = 10
    activity = 10
    lesson_page = 100
    lesson_answer = 150
    
    def incr_section(self):
        self.section += 1
    
    def incr_module(self):
        self.module += 1
    
    def incr_context(self):
        self.context += 1
    
    def incr_activity(self):
        self.activity += 1
    
    def incr_lesson_page(self):
        self.lesson_page += 1

    def incr_lesson_answer(self):
        self.lesson_answer += 1