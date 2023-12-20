class LVals:
    previous_text = 'Previous'
    previous_jumpto = '-40'
    next_text = 'Next'
    next_jumpto = '-1'
    end_text = 'End'
    end_jumpto = '-9'

class LAnswer:
    tag = 'answer'
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 0)
        self.jumpto = kwargs.get('jumpto', -1)
        self.grade = kwargs.get('grade', 0)
        self.score = kwargs.get('score', 0)
        self.flags = kwargs.get('flags', 0)
        self.timecreated = kwargs.get('timecreated', 0)
        self.timemodified = kwargs.get('timemodified', 0)
        self.answer_text = kwargs.get('answer_text', '')
        self.response = kwargs.get('response', '$@NULL@$')
        self.answerformat = kwargs.get('answerformat', 0)
        self.responseformat = kwargs.get('responseformat', 0)
        

    def to_dict(self):
        return {
            'id': self.id,
            'jumpto': self.jumpto,
            'grade': self.grade,
            'score': self.score,
            'flags': self.flags,
            'timecreated': self.timecreated,
            'timemodified': self.timemodified,
            'answer_text': self.answer_text,
            'response': self.response,
            'answerformat': self.answerformat,
            'responseformat': self.responseformat,
            'tag': self.tag
        }
    
class LPage:
    tag = 'page'
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 0)
        self.prevpageid = kwargs.get('prevpageid', 0)
        self.nextpageid = kwargs.get('nextpageid', 0)
        self.qtype = kwargs.get('qtype', 20)
        self.qoption = kwargs.get('qoption', 0)
        self.layout = kwargs.get('layout', 1)
        self.display = kwargs.get('display', 1)
        self.timecreated = kwargs.get('timecreated', 0)
        self.timemodified = kwargs.get('timemodified', 0)
        self.title = kwargs.get('title', '')
        self.contents = kwargs.get('contents', '')
        self.contentsformat = kwargs.get('contentsformat', 4)
        self.answers = kwargs.get('answers', [])

    def to_dict(self):
        return {
            'id': self.id,
            'prevpageid': self.prevpageid,
            'nextpageid': self.nextpageid,
            'qtype': self.qtype,
            'qoption': self.qoption,
            'layout': self.layout,
            'display': self.display,
            'timecreated': self.timecreated,
            'timemodified': self.timemodified,
            'title': self.title,
            'contents': self.contents,
            'contentsformat': self.contentsformat,
            'answers': [answer.to_dict() for answer in self.answers],
            'tag': self.tag
        }