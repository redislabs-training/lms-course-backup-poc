import unittest
import yaml
from pathlib import Path
from src.course_entities import Course, CourseModule, ContentItem, Dependency, Visibility, ContentItemType, TopicType, DescriptorType, ContentCourseTopic, ModuleCourseTopic

class TestCourseDataClasses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the course YAML file
        course_yaml_path = Path(__file__).parent / "sample-course-source/course.yaml"
        with open(course_yaml_path, 'r') as file:
            cls.course_data = yaml.safe_load(file)
        cls.course = Course(**cls.course_data)

        module_yaml_path = Path(__file__).parent / "sample-course-source/module/module.yaml"
        with open(module_yaml_path, 'r') as file:
            cls.module_data = yaml.safe_load(file)
        cls.module= CourseModule(**cls.module_data)

    def test_course_class(self):
        self.assertEqual(type(self.course), Course)

    def test_course_descriptor(self):
        self.assertEqual(self.course.type, DescriptorType.COURSE)

    def test_course_id(self):
        self.assertEqual(self.course.id, "enablement-sample")

    def test_course_full_name(self):
        self.assertEqual(self.course.full_name, "Sample Learning Course")

    def test_course_version(self):
        self.assertEqual(self.course.version, "v1.0.0")

    def test_course_dependencies(self):
        self.assertEqual(type(self.course.dependencies[0]), Dependency)

    def test_course_icon(self):
        self.assertEqual(self.course.icon, "./course-logo.png")

    def test_course_learning_objectives(self):
        self.assertIn("Sample structure", self.course.learning_objectives)
        self.assertIn("Basic course yaml", self.course.learning_objectives)

    def test_course_topics(self):
        self.assertEqual(len(self.course.topics), 3)
        
    def test_course_topic_names(self):
        self.assertEqual(self.course.topics[0].name, "Introduction")
        self.assertEqual(self.course.topics[1].name, "Deep")
        self.assertEqual(self.course.topics[2].name, "Uses")

    def test_content_items_in_topics(self):
        intro_topic = self.course.topics[0]
        self.assertEqual(type(intro_topic), ContentCourseTopic)
        self.assertEqual(len(intro_topic.content_items), 2)
        self.assertEqual(type(intro_topic.content_items[0]), ContentItem)
        self.assertEqual(intro_topic.content_items[0].name, "Basics")
        self.assertEqual(intro_topic.content_items[0].type, ContentItemType.VIDEO)

    def test_module_topic(self):
        module_topic = self.course.topics[2]
        self.assertEqual(type(module_topic), ModuleCourseTopic)
        self.assertEqual(module_topic.visibility, Visibility.PUBLIC)
        self.assertEqual(module_topic.type, TopicType.MODULE)
        self.assertEqual(module_topic.module, "mod-sample-uses")
    
    # CourseModule tests

    def test_module_class(self):
        self.assertEqual(type(self.module), CourseModule)

    def test_module_version(self):
        self.assertCountEqual(self.module.version, 'v1.0.0')

    def test_module_id(self):
        self.assertEqual(self.module.id, "mod-sample-uses")

    def test_module_name(self):
        self.assertEqual(self.module.name, "Sample Uses")

    def test_module_descr(self):
        self.assertEqual(self.module.descr, "This module introduces basic concepts in Sample Uses.")

    def test_module_descriptor(self):
        self.assertEqual(self.module.type, DescriptorType.MODULE)

    def test_module_learning_objectives(self):
        self.assertIn("Introduction to statistical methods", self.module.learning_objectives)

    def test_module_topics(self):
        self.assertEqual(len(self.module.topics), 2)
        self.assertEqual(self.module.topics[0].name, "Uses Overview")

    def test_content_items_in_topics(self):
        intro_topic = self.module.topics[0]
        self.assertEqual(type(intro_topic), ContentCourseTopic)
        self.assertEqual(len(intro_topic.content_items), 3)
        self.assertEqual(type(intro_topic.content_items[0]), ContentItem)
        self.assertEqual(intro_topic.content_items[0].name, "What is Data Science?")
        self.assertEqual(intro_topic.content_items[0].type, ContentItemType.VIDEO)

if __name__ == '__main__':
    unittest.main()
