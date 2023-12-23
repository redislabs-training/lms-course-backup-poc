import unittest
import yaml
from pathlib import Path
from src.edx.course_dataclasses import Course, ContentItem, Dependency, Visibility, ContentItemType, TopicType, CourseTopic, ContentCourseTopic

class TestCourseData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the YAML file
        course_yaml_path = Path(__file__).parent / "sample-course-source/course.yaml"
        with open(course_yaml_path, 'r') as file:
            cls.course_data = yaml.safe_load(file)
        cls.course = Course(**cls.course_data)

    def test_course_basic_info(self):
        # Test basic course info
        self.assertEqual(self.course.id, "enablement-sample")
        self.assertEqual(self.course.full_name, "Sample Learning Course")
        self.assertEqual(self.course.version, "v1.0.0")

    def test_course_icon(self):
        # Test course icon reference
        self.assertEqual(self.course.icon, "./course-logo.png")

    def test_course_learning_objectives(self):
        # Test learning objectives
        self.assertIn("Sample structure", self.course.learning_objectives)
        self.assertIn("Basic course yaml", self.course.learning_objectives)

    def test_course_topics(self):
        # Test topics count and names
        self.assertEqual(len(self.course.topics), 2)  # Assuming 2 topics in the YAML
        self.assertEqual(self.course.topics[0].name, "Introduction")
        self.assertEqual(self.course.topics[1].name, "Deep")

    def test_content_items_in_topics(self):
        # Test content items within a topic
        intro_topic = self.course.topics[0]
        self.assertEqual(len(intro_topic.content_items), 2)  # Assuming 2 content items in the first topic
        self.assertEqual(intro_topic.content_items[0].name, "Basics")
        self.assertEqual(intro_topic.content_items[0].type, ContentItemType.VIDEO)

    # Additional tests can be written for more specifics, like content item type, ref checks, etc.

if __name__ == '__main__':
    unittest.main()
